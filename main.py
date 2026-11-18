from rpg.application.game_service import GameService
from rpg.config import load_settings
from rpg.infrastructure.mysql_save_repository import MySQLSaveRepository
from rpg.presentation.console import ConsoleGame


def main() -> None:
    try:
        repository = MySQLSaveRepository(load_settings())
        repository.ensure_schema()
    except Exception as exc:
        print("MySQL에 연결할 수 없습니다.")
        print("MySQL 서버 실행 여부와 .env 접속 정보를 확인하세요.")
        print(f"상세 오류: {exc}")
        input("Enter 키를 누르면 종료합니다.")
        return
    ConsoleGame(GameService(repository)).run()


if __name__ == "__main__":
    main()
