import pytest

@pytest.mark.asyncio
async def test_quote_random(client):
    r = await client.get("/quote/random")
    assert r.status_code in (200, 404)  # 데이터 없으면 404도 허용(초기 상태)
