import pytest

@pytest.mark.asyncio
async def test_bookmark_list(client, user_id):
    r = await client.get("/quote/bookmark", params={"user_id": user_id})
    assert r.status_code in (200, 404)