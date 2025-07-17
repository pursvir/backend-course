import pytest
from httpx import AsyncClient
from vars import auth_credentials


@pytest.mark.parametrize(
    "email, password, register_status_code, login_status_code",
    [
        (auth_credentials["email"], auth_credentials["password"], 409, None),
        ("thisisdefinitelyaninvalidemailaddress", "1", 422, None),
        ("ivan-petrov@yandex.ru", "Qwerty123", 200, 200),
    ],
)
async def test_auth_flow(
    email: str,
    password: str,
    register_status_code: int,
    login_status_code: int,
    ac: AsyncClient,
):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == register_status_code
    if response.status_code == 200:
        response = await ac.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )
        assert response.status_code == login_status_code
        assert response.cookies
        assert response.cookies[
            "access_token"
        ]  # Можно было ещё проверить содержимое этого токена, но мне лень)

        response = await ac.get("/auth/me")
        assert response.status_code == 200
        res = response.json()
        assert res
        assert isinstance(res, dict)
        assert res["email"] == email
        assert res["id"]  # Не хочу проверять id)
        assert "password" not in res
        assert "hashed_password" not in res

        response = await ac.post("/auth/logout")
        assert response.status_code == 200
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert not response.cookies

        response = await ac.get("/auth/me")
        assert response.status_code == 401
