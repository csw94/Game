from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Player:
    name: str
    level: int = 1
    hp: int = 30
    max_hp: int = 30
    attack: int = 7
    defense: int = 2
    xp: int = 0
    gold: int = 0
    potions: int = 2
    location: str = "초보자의 숲"
    enemies_defeated: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Player":
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: data[key] for key in allowed if key in data})


@dataclass(frozen=True)
class Enemy:
    name: str
    hp: int
    attack: int
    defense: int
    xp_reward: int
    gold_reward: int
