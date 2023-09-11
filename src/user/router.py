from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from src.database import get_async_session
from src.user.models import User
from src.user.schemas import UserOut

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/", response_model=List[UserOut])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).options(selectinload(User.role)))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(User).filter(User.id == user_id).options(selectinload(User.role))
    )
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user
