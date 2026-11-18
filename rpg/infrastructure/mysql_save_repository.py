from __future__ import annotations

import json
from mysql.connector import connect
from mysql.connector.errors import Error
from rpg.domain.models import Player


class MySQLSaveRepository:
    def __init__(self, settings: dict[str, object]):
        self.settings = settings

    def _connect(self):
        return connect(**self.settings, connection_timeout=5)

    def ensure_schema(self) -> None:
        try:
            with self._connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""CREATE TABLE IF NOT EXISTS save_slots (
                        slot_id TINYINT UNSIGNED NOT NULL PRIMARY KEY,
                        player_name VARCHAR(40) NOT NULL,
                        level SMALLINT UNSIGNED NOT NULL,
                        location VARCHAR(80) NOT NULL,
                        state_json JSON NOT NULL,
                        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        CONSTRAINT chk_save_slot_id CHECK (slot_id BETWEEN 1 AND 3)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
        except Error as exc:
            raise RuntimeError(f"MySQL 연결 또는 테이블 준비에 실패했습니다: {exc}") from exc

    def list_slots(self) -> dict[int, tuple[str, int, str] | None]:
        result = {1: None, 2: None, 3: None}
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT slot_id, player_name, level, location FROM save_slots ORDER BY slot_id")
                for slot, name, level, location in cursor.fetchall():
                    result[int(slot)] = (name, int(level), location)
        return result

    def save(self, slot: int, player: Player) -> None:
        self._validate_slot(slot)
        state = json.dumps(player.to_dict(), ensure_ascii=False)
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO save_slots (slot_id, player_name, level, location, state_json)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE player_name=VALUES(player_name), level=VALUES(level),
                    location=VALUES(location), state_json=VALUES(state_json)""",
                    (slot, player.name, player.level, player.location, state))

    def load(self, slot: int) -> Player | None:
        self._validate_slot(slot)
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT state_json FROM save_slots WHERE slot_id=%s", (slot,))
                row = cursor.fetchone()
        if row is None:
            return None
        payload = row[0]
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")
        if isinstance(payload, str):
            payload = json.loads(payload)
        return Player.from_dict(payload)

    @staticmethod
    def _validate_slot(slot: int) -> None:
        if slot not in (1, 2, 3):
            raise ValueError("세이브 슬롯은 1~3만 사용할 수 있습니다.")
