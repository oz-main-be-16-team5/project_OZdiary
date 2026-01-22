import asyncio
import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise
from app.main import app


# (0) Windows pytest-asyncio event loop
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# (1) 테스트 DB 세팅: SQLite in-memory
TEST_DATABASE_URL = "sqlite://:memory:"


# (2) 테스트마다 스키마 초기화(create / drop 대체)
@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_test_db():
    await Tortoise.init(
        db_url=TEST_DATABASE_URL,
        modules={
            "models": [
                "app.models.user",
                "app.models.quote",
                "app.models.bookmark",
                "app.models.diary",
                "app.models.question",
                "app.models.user_question",
            ]
        },
    )
    await Tortoise.generate_schemas()

    yield

    # in-memory라서 종료하면 사실상 drop과 동일 효과
    await Tortoise.close_connections()


# (3) httpx AsyncClient
@pytest_asyncio.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac

@pytest_asyncio.fixture
async def user_payload():
    u = uuid.uuid4().hex[:8]
    return {
        "email": f"test_{u}@test.com",
        "username": f"tester_{u}",          # username 필수
        "password": "password1234",         # 8자 이상
    }

@pytest_asyncio.fixture
async def auth_header(client, user_payload):
    # 1) 회원가입
    r_signup = await client.post("/auth/register", json=user_payload)
    assert r_signup.status_code in (200, 201), r_signup.text

    # 2) 로그인
    r_login = await client.post(
        "/auth/login",
        json={"email": user_payload["email"], "password": user_payload["password"]},
    )
    assert r_login.status_code == 200, r_login.text

    data = r_login.json()
    token = data.get("access_token") or data.get("token")
    assert token, f"토큰 키 확인 필요: {data}"

    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def token(auth_header):
    return auth_header["Authorization"].split(" ", 1)[1]

@pytest_asyncio.fixture
async def user_id():
    return 1