import secrets
import time
import jwt
from fastapi import HTTPException, status
from jwt.exceptions import(
    DecodeError,
    InvalidSignatureError
)
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

def decode_refresh_token(token):
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms="HS256"
            )
        user_id = decoded_token.get("user_id", None)
        expired_time = decoded_token.get("exp", None)
        if user_id is None or isinstance(user_id, int)==False:
            raise HTTPException(
            detail="Invalid user_id in payload.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        if expired_time is None or isinstance(expired_time, int)==False:
            raise HTTPException(
            detail="Invalid expiration time in payload.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        if decoded_token.get("type", None) != "refresh":
            raise HTTPException(
            detail="Invalid token type.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        if time.time() > expired_time:
            raise HTTPException(
            detail="Token expired.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        return user_id
        
    except InvalidSignatureError:
        raise HTTPException(
            detail="Authentication failed, Invalid signature.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except DecodeError:
        raise HTTPException(
            detail="Authentication failed, Decode failed.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Authentication failed, {e}",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
