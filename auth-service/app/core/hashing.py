# app/core/hashing.py
from passlib.context import CryptContext

# Use only bcrypt, avoids the deprecated crypt backend
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Generate a bcrypt hash for the given password."""
    # Passlib.hash returns Any, but we know it's str
    return str(pwd_context.hash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches the hashed password."""
    # Passlib.verify returns Any, but we know it's bool
    return bool(pwd_context.verify(plain_password, hashed_password))
