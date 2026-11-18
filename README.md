# TextRPG

Windows 콘솔에서 실행하는 전투·탐험 RPG입니다. 세이브는 SQLite 파일로 각 Windows 사용자 계정의 PC에 저장되며, MySQL 서버나 네트워크 연결이 필요하지 않습니다.

## 요구 환경

- Windows 10/11
- 개발 및 EXE 빌드: Python 3.11 이상
- 실행: 빌드된 `TextRPG.exe`만 있으면 됩니다.

## 개발 실행

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

PowerShell 실행 정책 때문에 가상환경 활성화가 막히면 활성화 명령 대신 아래처럼 가상환경 Python을 직접 실행할 수 있습니다.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

첫 실행 때 저장 파일과 테이블을 자동으로 준비합니다. Windows 세이브 파일 위치는 `%LOCALAPPDATA%\TextRPG\saves.sqlite3`입니다. 같은 Windows 사용자 계정으로 실행하는 게임은 세이브 슬롯 1~3을 함께 사용합니다.

## Windows EXE 빌드

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm --onefile --console --name TextRPG main.py
```

산출물은 `dist\TextRPG.exe`입니다. 배포할 때는 이 EXE를 전달하면 됩니다. 별도의 `.env`, SQL 스크립트, MySQL 설치가 필요하지 않습니다. Windows용 EXE는 Windows에서 빌드해야 합니다.

새 컴퓨터로 세이브를 옮기려면 게임을 종료한 뒤 기존 PC의 `%LOCALAPPDATA%\TextRPG\saves.sqlite3` 파일을 새 PC의 같은 위치로 복사하세요. 기존 세이브 파일을 덮어쓸 수 있으니 백업 후 옮기세요.

## GitHub 배포

Windows에서 EXE를 빌드한 뒤 `dist\TextRPG.exe`를 ZIP으로 묶어 GitHub 저장소의 **Releases**에 첨부하세요. `dist`, `.venv`, 개인 세이브 파일은 Git 저장소에 커밋하지 않습니다.
