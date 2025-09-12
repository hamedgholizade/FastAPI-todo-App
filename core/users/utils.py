import secrets
import time
import jwt
from passlib.context import CryptContext

from core.config import settings


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

def generate_access_token(user_id: int, expired_in: int = 60*5) -> str:
    now = int(time.time())
    payload = {
        'type': 'access',
        'user_id': user_id,
        'iat': now,
        'exp': now + expired_in
    }
    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm="HS256"
        )

def generate_refresh_token(user_id: int, expired_in: int = 60*60*24) -> str:
    now = int(time.time())
    payload = {
        'type': 'refresh',
        'user_id': user_id,
        'iat': now,
        'exp': now + expired_in
    }
    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm="HS256"
        )
