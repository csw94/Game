from rpg.application.game_service import GameService
from rpg.infrastructure.sqlite_save_repository import SQLiteSaveRepository
from rpg.presentation.console import ConsoleGame


def main() -> None:
    try:
        repository = SQLiteSaveRepository()
        repository.ensure_schema()
    except Exception as exc:
        print("로컬 저장 데이터베이스를 준비할 수 없습니다.")
        print(f"상세 오류: {exc}")
        input("Enter 키를 누르면 종료합니다.")
        return
    print(f"세이브 파일: {repository.database_path}")
    ConsoleGame(GameService(repository)).run()


if __name__ == "__main__":
    main()
