import pytest

@pytest.mark.asyncio
async def test_signup_and_login(client):
    email = "a@test.com"
    pw = "password1234"

    r1 = await client.post("/auth/register", json={
        "email": email,
        "username": "aa",
        "password": pw,
    })
    assert r1.status_code in (200, 201), r1.text

    r2 = await client.post("/auth/login", json={
        "email": email,
        "password": pw
    })
    assert r2.status_code == 200, r2.text
    assert ("access_token" in r2.json()) or ("token" in r2.json())