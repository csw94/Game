# 인수인계

- 새 Python 프로젝트: `C:\Users\dongb\IdeaProjects\TextRPG`
- 계층형 구조 선택 완료: domain / application / infrastructure / presentation
- 구현 범위: 콘솔 전투·탐험 RPG, MySQL 세이브/로드 슬롯 1~3
- `.env.example`, `sql/schema.sql`, `requirements.txt`, README 작성
- `Main.java`가 있는 Java 프로젝트는 별도로 유지
- 현재 환경에서 Python 실행은 Windows Store alias 접근 거부로 실패했으며, Git 실행 파일도 PATH/일반 설치 경로에서 찾지 못함
- MySQL client 8.0.46은 확인됨
- 다음 작업: Python 설치 경로 확인 후 의존성 설치, 실행 확인, Windows EXE 빌드, Git 설치/연결 확인
- EXE가 MySQL 서버나 비밀정보를 포함하지 않음. 플레이 PC에는 DB 서버 연결과 별도 `.env` 설정이 필요
