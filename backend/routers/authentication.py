from backend.routers.security import create_access_token
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from backend.schemas import UserCreate, UserLogin
from backend.db_manager import (
    is_email_available,
    create_user,
    get_user_by_email,
)

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/citizencreate")
def register_user(user: UserCreate):
    if not is_email_available(user.email):
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return create_user(
        username=user.username,
        email=user.email,
        password=pwd_context.hash(user.password)
    )


@router.post("/citizenlogin")
def login_user(user: UserLogin):
    stored_user = get_user_by_email(user.email)

    if stored_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(user.password, stored_user[2]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": "citizen"}
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }
    
