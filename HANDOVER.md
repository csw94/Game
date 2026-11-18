# 인수인계

- Python 콘솔 TextRPG 프로젝트입니다.
- 계층: `domain`, `application`, `infrastructure`, `presentation`
- 세이브/로드는 SQLite 저장소를 사용합니다. MySQL 및 `.env` 설정은 실행에 필요하지 않습니다.
- Windows 사용자별 세이브 경로: `%LOCALAPPDATA%\TextRPG\saves.sqlite3`
- SQLite 테이블은 첫 실행 때 자동 생성됩니다.
- Windows EXE 빌드: `python -m PyInstaller --clean --noconfirm --onefile --console --name TextRPG main.py`
- 결과물: `dist\TextRPG.exe`; GitHub 배포 시 EXE만 ZIP으로 묶어 Releases에 첨부합니다.
