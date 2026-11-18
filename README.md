# TextRPG

Python 콘솔 기반 전투·탐험 RPG의 첫 실행 버전입니다. 전투와 탐험 상태는 애플리케이션 계층에서 관리하고 MySQL 저장소가 세이브 슬롯 3개를 보관합니다.

## 요구 환경

- Windows 10/11
- Python 3.11 이상 (개발·빌드 시)
- MySQL Server 8.0 이상과 접속 가능한 계정

MySQL Connector/Python을 사용하므로 DB 서버는 게임 실행 파일에 포함되지 않습니다. 플레이하는 PC에서 MySQL 서버에 연결할 수 있어야 합니다.

## DB 준비

MySQL에 접속해 `sql/schema.sql`의 `change-me`를 사용할 비밀번호로 바꾼 뒤 실행하세요. 같은 비밀번호를 `.env.example`에서 `.env`를 만들 때 `MYSQL_PASSWORD`에 설정합니다. SQL 스크립트는 데이터베이스와 전용 계정, 세이브 테이블을 준비합니다. `.env`는 비밀번호가 들어갈 수 있어 Git에 올리지 않습니다.

## 개발 실행

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Windows EXE 빌드

```powershell
.\.venv\Scripts\Activate.ps1
python -m PyInstaller --clean --noconfirm --onefile --console --name TextRPG main.py
```

산출물은 `dist\TextRPG.exe`입니다. `.env.example`을 `.env`로 복사해 EXE 옆에 배치하세요. 콘솔에서 실행하는 게임이므로 `--console` 옵션을 씁니다. PyInstaller 빌드는 대상 운영체제에서 실행해야 하므로 Windows용 EXE는 Windows에서 빌드합니다.

## Git 배포 흐름

```powershell
git init
git add .
git commit -m "Build playable TextRPG MVP"
git tag v0.1.0
```

빌드 결과물과 비밀정보는 Git에 포함하지 않습니다. `dist\TextRPG.exe`와 별도의 `.env`를 배포하세요. 배포 환경마다 MySQL 호스트·계정·DB를 설정해야 합니다.

