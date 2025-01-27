from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.future import select
from sqlalchemy import MetaData, Table, Column, Integer, String, inspect
from fastapi import HTTPException, status
from app.models.user import User
from app.auth.utils import hash_password
from app.schemas.user import UserCreate


async def create_user(user_data: UserCreate, db: AsyncSession):

    result = await db.execute(
        select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


