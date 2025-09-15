import time
import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from core.config import settings
from users.models import UserModel


security = HTTPBearer(scheme_name="Token", auto_error=False)


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    # Check if credentials are not provided
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed, token not provided",
        )
    token = credentials.credentials
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms="HS256",
        )
        user_id = decoded_token.get("user_id", None)
        expired_time = decoded_token.get("exp", None)
        if user_id is None or isinstance(user_id, int) is False:
            raise HTTPException(
                detail="Invalid user_id in payload.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        if expired_time is None or isinstance(expired_time, int) is False:
            raise HTTPException(
                detail="Invalid expiration time in payload.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        if decoded_token.get("type", None) != "access":
            raise HTTPException(
                detail="Invalid token type.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        if time.time() > expired_time:
            raise HTTPException(
                detail="Token expired.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        user_obj = db.query(UserModel).filter_by(id=user_id).one_or_none()
        if user_obj is None:
            raise HTTPException(
                detail="Invalid user_id in payload.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return user_obj
    except InvalidSignatureError:
        raise HTTPException(
            detail="Authentication failed, Invalid signature.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except DecodeError:
        raise HTTPException(
            detail="Authentication failed, Decode failed.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Authentication failed, {e}",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
