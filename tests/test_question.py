import pytest

@pytest.mark.asyncio
async def test_question_list(client, auth_header):
    r = await client.get("/question/random", headers=auth_header)
    assert r.status_code in (200, 404)
