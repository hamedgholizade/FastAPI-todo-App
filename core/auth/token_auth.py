from fastapi import (
    Depends,
    HTTPException,
    status
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from users.models import Tokenmodel


security = HTTPBearer(scheme_name="Token")


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token_obj = db.query(Tokenmodel).filter_by(token=credentials.credentials).one_or_none()
    if not token_obj:
        raise HTTPException(
            detail="Authenticattion failed",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )  
    # logic owner
    
    return token_obj.user
