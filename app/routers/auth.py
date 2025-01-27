from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.jwt import create_access_token, create_refresh_token
from app.schemas.auth import TokenResponse
from app.schemas.user import UserLogin, UserCreate, UserOut
from app.models.user import User
from app.services.user import create_user
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from app.auth.utils import verify_password
from sqlalchemy.future import select

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()
    print("db-------------------", db_user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_data = {"sub": user.username}
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_user(user_data, db)