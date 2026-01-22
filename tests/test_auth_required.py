import pytest

@pytest.mark.asyncio
async def test_diary_requires_token(client):
    """
    토큰 없이 보호된 엔드포인트 접근 시 실패해야 한다
    """
    r = await client.get("/v1/diary/")
    assert r.status_code == 422
