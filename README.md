# project_OZdiary

---
### 팀

- Organization: Danbam - ( OZ Main BE 16th Team 5 )

- Project Name: project_OZdiary
---
Daily Diary System

🌙 Danbam
— 당신의 하루의 끝이 달콤하기를.

Danbam은 하루의 끝에서 스스로를 돌아보는 일기 + 명언 + 질문 기반 자기성찰 서비스입니다.

Danbam은 사용자가 하루에 하나의 질문을 받고,
그 질문을 바탕으로 일기를 작성하며 의미 있는 하루를 기록할 수 있도록 돕는 서비스입니다.

1. 하루 한 번 제공되는 자기성찰 질문

2. 자유롭게 작성하는 개인 일기

3. 랜덤 명언 제공 및 북마크 기능

4. JWT 기반 인증으로 안전한 사용자 관리

---
### API Endpoints (주요 기능)

- Auth: 회원가입(/auth/register), 로그인(/auth/login), 로그아웃 기능 제공

- Diary: 일기 생성, 조회, 수정, 삭제(CRUD)

- Quotes: 스크레이핑된 데이터 기반 랜덤 명언 제공 및 북마크

- Questions: 자기성찰을 위한 랜덤 질문 제공

---

### 기술 스택

- Backend: FastAPI (Python 3.12+)
- Database: PostgreSQL 18.1
- ORM: Tortoise ORM (Asynchronous ORM)
- Authentication: JWT (JSON Web Token) based Auth & Token Blacklist
- Environment Manager: uv (Fast & Modern Package Manager)
- Documentation: Swagger UI (provided by FastAPI)


---
Directory Structure (폴더 구조)
```Plaintext
project_OZdiary/
├── app/
│   ├── api/v1/       # 엔드포인트 라우터 (auth, diary, quote 등)
│   ├── core/         # 설정 및 보안 (config, security)
│   ├── db/           # 데이터베이스 연결 및 초기화
│   ├── models/       # Tortoise ORM 데이터 모델
│   ├── schemas/      # Pydantic 데이터 검증 스키마
│   ├── services/     # 비즈니스 로직 처리
│   ├── scraping/     # 명언 수집 스크레이퍼
│   └── main.py       # 애플리케이션 진입점
├── static/           # 프론트엔드 정적 파일 (index.html)
├── .env              # 환경 변수 설정
└── pyproject.toml    # uv 패키지 관리 파일
```

---


---


### ERD Diagram

![img.png](img.png)

사용자가 받은 질문, 작성한 일기, 북마크한 명언을 명확하게 추적할 수 있도록 관계를 구성했습니다.

users : token_blacklist = 1 : N

- 한명의 회원이 만료된 여러 토큰을 가질 수 있습니다.

users : diaries = 1 : N

- 한명의 회원이 여러 일기를 작성할 수 있습니다.

users : user_questions  = 1 : N

- 한명의 회원이 여러 자기성찰 질문을 받을 수 있습니다.

users : bookmarks = 1 : N

- 한명의 회원이 여러 명언 북마크를 할 수 있습니다.

user_questions : questions = 1 : 1

- 하나의 자기성찰 질문은 오직 하나의 스크래핑 질문과 연결됩니다.

bookmarks : quotes = 1 : 1

- 하나의 북마크는 오직 하나의 스크래핑 명언과 연결됩니다.

---

### Installation & Setup (설치 및 실행)

이 프로젝트는 uv를 사용하여 환경을 관리합니다.

Repository Clone

```Bash
git clone https://github.com/oz-main-be-16-team5/project_OZdiary.git
cd project_OZdiary
```

Environment Setup .env 파일을 루트 디렉토리에 생성하고 아래 정보를 입력하세요.

```코드 스니펫
DATABASE_URL="postgres://username:password@localhost:5432/diary_db"
JWT_SECRET_KEY="your_secret_key"
JWT_ALGORITHM="HS256"
```

Dependency Install
```Bash
uv sync
```

Run Server
```Bash
uv run uvicorn app.main:app --reload
```
