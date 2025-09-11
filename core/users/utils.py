import secrets
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(plain_password: str) -> str:
    """Hashes the given password using bcrypt."""
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies the given password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def generate_token(length: int = 32) -> str:
    """Generate a secure random token as a string"""
    return secrets.token_hex(length)
