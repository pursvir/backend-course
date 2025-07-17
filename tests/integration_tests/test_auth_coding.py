from src.services.auth import CryptoService


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    token = CryptoService().create_access_token(data)
    assert token
    assert isinstance(token, str)

    payload = CryptoService().decode_token(token)
    assert payload
    assert payload["user_id"] == data["user_id"]
