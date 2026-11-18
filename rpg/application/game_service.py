from __future__ import annotations

from random import choice, randint, random
from rpg.domain.models import Enemy, Player


AREAS = ("초보자의 숲", "잊힌 폐허", "안개 계곡")
ENEMIES = ("슬라임", "고블린", "숲 늑대", "폐허의 해골")


class GameService:
    def __init__(self, saves):
        self.saves = saves

    def new_player(self, name: str) -> Player:
        clean_name = name.strip()[:40] or "모험가"
        return Player(name=clean_name)

    def explore(self, player: Player) -> tuple[str, Enemy | None]:
        player.location = choice(AREAS)
        if random() < 0.7:
            scale = max(0, player.level - 1)
            enemy = Enemy(choice(ENEMIES), 12 + scale * 4, 4 + scale * 2, 1 + scale,
                          10 + scale * 4, randint(5, 12) + scale * 2)
            return f"{player.location}을 탐험하다 {enemy.name}을(를) 만났습니다!", enemy
        reward = randint(4, 10) + player.level
        player.gold += reward
        found = "포션을 발견했습니다!" if random() < 0.35 else f"골드 {reward}개를 발견했습니다!"
        if "포션" in found:
            player.potions += 1
        return f"{player.location}을 탐험했습니다. {found}", None

    def attack(self, player: Player, enemy: Enemy, enemy_hp: int) -> tuple[int, int, str]:
        damage = max(1, player.attack + randint(-2, 2) - enemy.defense)
        enemy_hp = max(0, enemy_hp - damage)
        if enemy_hp == 0:
            player.xp += enemy.xp_reward
            player.gold += enemy.gold_reward
            player.enemies_defeated += 1
            level_message = self._level_up(player)
            return enemy_hp, 0, f"{enemy.name}에게 {damage} 피해를 주고 쓰러뜨렸습니다. 경험치 +{enemy.xp_reward}, 골드 +{enemy.gold_reward}.{level_message}"
        incoming = max(1, enemy.attack + randint(-1, 2) - player.defense)
        player.hp = max(0, player.hp - incoming)
        return enemy_hp, incoming, f"{enemy.name}에게 {damage} 피해! 반격으로 체력 {incoming}을 잃었습니다."

    def use_potion(self, player: Player) -> str:
        if player.potions <= 0:
            return "포션이 없습니다."
        if player.hp >= player.max_hp:
            return "체력이 이미 가득 찼습니다."
        healed = min(15, player.max_hp - player.hp)
        player.hp += healed
        player.potions -= 1
        return f"포션을 사용해 체력 {healed}을 회복했습니다."

    def save(self, slot: int, player: Player) -> None:
        self.saves.save(slot, player)

    def load(self, slot: int) -> Player | None:
        return self.saves.load(slot)

    def slots(self):
        return self.saves.list_slots()

    @staticmethod
    def _level_up(player: Player) -> str:
        needed = player.level * 25
        if player.xp < needed:
            return ""
        player.xp -= needed
        player.level += 1
        player.max_hp += 8
        player.hp = player.max_hp
        player.attack += 2
        player.defense += 1
        return f" 레벨 업! Lv.{player.level}이 되었습니다."
