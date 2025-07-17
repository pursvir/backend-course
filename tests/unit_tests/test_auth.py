from src.services.auth import CryptoService


def test_create_access_token():
    data = {"user_id": 1}
    token = CryptoService().create_access_token(data)
    assert token
    assert isinstance(token, str)
