from src.services.auth import AuthService

def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    token = AuthService().create_access_token(data)
    assert token
    assert isinstance(token, str)

    payload = AuthService().decode_token(token)
    assert payload
    assert payload["user_id"] == data["user_id"]
