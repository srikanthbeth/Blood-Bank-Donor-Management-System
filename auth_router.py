from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import models
import schemas

from auth import verify_password, create_access_token
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=schemas.UserResponse
)
def register(
    user: schemas.UserRegister,
    db: Session = Depends(get_db)
):

    existing = crud.get_user_by_email(db, user.email)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return crud.create_user(db, user)


@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_email(
        db,
        user_credentials.username
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    if not verify_password(
        user_credentials.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }