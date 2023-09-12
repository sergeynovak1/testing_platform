from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.user.models import User
from src.auth import schemas
from src.database import get_async_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = await db.execute(select(User).filter(User.id == token.id))
    return user.scalar_one_or_none()
