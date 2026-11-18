from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from rpg.domain.models import Player


def default_database_path() -> Path:
    """Return a writable, per-user location that survives app upgrades."""
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / "TextRPG" / "saves.sqlite3"
    return Path.home() / ".local" / "share" / "TextRPG" / "saves.sqlite3"


class SQLiteSaveRepository:
    def __init__(self, database_path: str | Path | None = None):
        self.database_path = Path(database_path) if database_path else default_database_path()
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path, timeout=5)
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def ensure_schema(self) -> None:
        with self._connect() as connection:
            connection.execute("""CREATE TABLE IF NOT EXISTS save_slots (
                slot_id INTEGER PRIMARY KEY CHECK (slot_id BETWEEN 1 AND 3),
                player_name TEXT NOT NULL,
                level INTEGER NOT NULL,
                location TEXT NOT NULL,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )""")

    def list_slots(self) -> dict[int, tuple[str, int, str] | None]:
        result = {1: None, 2: None, 3: None}
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT slot_id, player_name, level, location FROM save_slots ORDER BY slot_id"
            ).fetchall()
        for slot, name, level, location in rows:
            result[int(slot)] = (str(name), int(level), str(location))
        return result

    def save(self, slot: int, player: Player) -> None:
        self._validate_slot(slot)
        state = json.dumps(player.to_dict(), ensure_ascii=False)
        with self._connect() as connection:
            connection.execute("""INSERT INTO save_slots
                (slot_id, player_name, level, location, state_json)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(slot_id) DO UPDATE SET
                    player_name=excluded.player_name,
                    level=excluded.level,
                    location=excluded.location,
                    state_json=excluded.state_json,
                    updated_at=CURRENT_TIMESTAMP""",
                (slot, player.name, player.level, player.location, state))

    def load(self, slot: int) -> Player | None:
        self._validate_slot(slot)
        with self._connect() as connection:
            row = connection.execute(
                "SELECT state_json FROM save_slots WHERE slot_id = ?", (slot,)
            ).fetchone()
        if row is None:
            return None
        return Player.from_dict(json.loads(row[0]))

    @staticmethod
    def _validate_slot(slot: int) -> None:
        if slot not in (1, 2, 3):
            raise ValueError("세이브 슬롯은 1~3만 사용할 수 있습니다.")
