from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.schemas import UserCreate, UserOut
from src.user.models import User
from src.auth import utils

router = APIRouter(
    tags=["Authentication"]
)


# @router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=UserOut)
# async def registration(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password
#
#     new_user = User(**user.dict())
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)
#
#     return new_user


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
