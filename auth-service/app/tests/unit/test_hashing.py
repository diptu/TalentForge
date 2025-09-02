# app/tests/unit/test_hashing.py
from app.core.hashing import hash_password, verify_password


def test_hash_and_verify_password() -> None:
    password = "supersecret"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)
