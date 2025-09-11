from fastapi import (
    Depends,
    HTTPException,
    status
    )
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from users.models import UserModel
from users.utils import verify_password


security = HTTPBasic()


def get_authenticated_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user_obj = db.query(UserModel).filter_by(username=credentials.username).one_or_none()
    if not user_obj:
        raise HTTPException(
            detail="User doesn't exist",
            status_code=status.HTTP_404_NOT_FOUND
        )  
    if not verify_password(credentials.password, user_obj.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# @app.get("/private")
# def private_route(user: UserModel = Depends(get_authenticated_user)):
#     print(user)
#     return {"detail": "This is the private route"}
