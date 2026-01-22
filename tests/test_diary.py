import pytest

@pytest.mark.asyncio
async def test_diary_list(client, token):
    r = await client.get("/v1/diary/", params={"token": token})
    assert r.status_code in (200, 404)