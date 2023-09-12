from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_async_session
from src.auth.schemas import UserCreate, UserOut
from src.user.models import User
from src.auth import utils

from src.auth import oauth2

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def registration(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    base_data = {
        "is_active": True,
        "registered_at": datetime.utcnow(),
        "last_login_at": datetime.utcnow(),
        "role_id": 1,
    }

    new_user = User(**user.dict(), **base_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    stmt = select(User).where(User.email == user_credentials.username)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
