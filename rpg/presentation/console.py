from __future__ import annotations

from rpg.domain.models import Enemy, Player


class ConsoleGame:
    def __init__(self, game):
        self.game = game

    def run(self) -> None:
        print("=== TEXT RPG: 잊힌 대륙 ===")
        while True:
            print("\n1. 새 모험  2. 불러오기  3. 종료")
            choice = input("> ").strip()
            if choice == "1":
                player = self.game.new_player(input("모험가 이름: "))
                self.play(player)
            elif choice == "2":
                player = self.choose_load()
                if player:
                    self.play(player)
            elif choice == "3":
                print("모험을 종료합니다.")
                return
            else:
                print("1~3 중에서 선택해 주세요.")

    def choose_load(self):
        self.show_slots()
        slot = self.ask_slot()
        try:
            player = self.game.load(slot)
        except Exception as exc:
            print(f"불러오기에 실패했습니다: {exc}")
            return None
        if player is None:
            print("비어 있는 슬롯입니다.")
        return player

    def play(self, player: Player) -> None:
        print(f"\n{player.name}, 모험을 시작합니다!")
        while player.hp > 0:
            self.show_status(player)
            print("1. 탐험  2. 저장  3. 메인 메뉴")
            action = input("> ").strip()
            if action == "1":
                message, enemy = self.game.explore(player)
                print(message)
                if enemy:
                    self.battle(player, enemy)
                    if player.hp <= 0:
                        print("쓰러졌습니다. 메인 메뉴로 돌아갑니다.")
                        break
            elif action == "2":
                self.save(player)
            elif action == "3":
                return
            else:
                print("1~3 중에서 선택해 주세요.")

    def battle(self, player: Player, enemy: Enemy) -> None:
        enemy_hp = enemy.hp
        print(f"전투 시작! {enemy.name} (HP {enemy_hp})")
        while enemy_hp > 0 and player.hp > 0:
            print(f"\n내 HP {player.hp}/{player.max_hp} | {enemy.name} HP {enemy_hp}")
            print("1. 공격  2. 포션 사용  3. 도망")
            action = input("> ").strip()
            if action == "1":
                enemy_hp, _, result = self.game.attack(player, enemy, enemy_hp)
                print(result)
            elif action == "2":
                print(self.game.use_potion(player))
            elif action == "3":
                print("전투에서 도망쳤습니다.")
                return
            else:
                print("1~3 중에서 선택해 주세요.")

    def save(self, player: Player) -> None:
        self.show_slots()
        slot = self.ask_slot()
        try:
            self.game.save(slot, player)
            print(f"슬롯 {slot}에 저장했습니다.")
        except Exception as exc:
            print(f"저장에 실패했습니다: {exc}")

    def show_slots(self) -> None:
        try:
            slots = self.game.slots()
        except Exception as exc:
            print(f"세이브 목록을 읽지 못했습니다: {exc}")
            return
        print("\n--- 세이브 슬롯 ---")
        for slot, summary in slots.items():
            if summary:
                name, level, location = summary
                print(f"{slot}. {name} | Lv.{level} | {location}")
            else:
                print(f"{slot}. 비어 있음")

    @staticmethod
    def ask_slot() -> int:
        while True:
            try:
                slot = int(input("슬롯 번호 (1~3): ").strip())
                if slot in (1, 2, 3):
                    return slot
            except ValueError:
                pass
            print("1, 2, 3 중 하나를 입력해 주세요.")

    @staticmethod
    def show_status(player: Player) -> None:
        print(f"\n[{player.name} | Lv.{player.level} | {player.location}] "
              f"HP {player.hp}/{player.max_hp} | 공격 {player.attack} | 방어 {player.defense} "
              f"| XP {player.xp} | 골드 {player.gold} | 포션 {player.potions}")
