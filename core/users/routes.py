from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    Path,
    status,
    HTTPException,
    Depends,
    Query
)

from users.schemas import (
    UserLoginSchema,
    UserRegisterSchema
)
from users.utils import (
    get_password_hash,
    verify_password,
    generate_token
)
from users.models import (
    UserModel,
    Tokenmodel
)
from core.database import get_db


router = APIRouter(tags=["users"], prefix="/users")

@router.post("/login")
async def user_login(
    request: UserLoginSchema,
    db: Session = Depends(get_db)
    ):
    user_obj = db.query(UserModel).filter_by(username=request.username).first()
    if not user_obj:
        raise HTTPException(
            detail="User doesn't exist",
            status_code=status.HTTP_404_NOT_FOUND
        )
    if not verify_password(request.password, user_obj.password):
        raise HTTPException(
            detail="Password is invalid",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    token_obj = Tokenmodel(user_id=user_obj.id, token=generate_token())
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)
    return JSONResponse(
        content={
            "detail": "User logged in successfully",
            "token": token_obj.token
            },
        status_code=status.HTTP_202_ACCEPTED
    )

@router.post("/register")
async def user_register(
    request: UserRegisterSchema,
    db: Session = Depends(get_db)
    ):
    if db.query(UserModel).filter_by(username=request.username).first():
        raise HTTPException(
            detail="Username already exists",
            status_code=status.HTTP_409_CONFLICT
        )
    user_obj = UserModel(
        username=request.username.lower(),
        password=get_password_hash(request.password)
        )
    db.add(user_obj)
    db.commit()
    return JSONResponse(
        content={"detail": "User registered successfully"},
        status_code=status.HTTP_201_CREATED
    )
