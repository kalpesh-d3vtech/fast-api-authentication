from fastapi import APIRouter
from .user import router as user_router
from .auth import router as auth_router
from .token import router as token_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(token_router, prefix="/refresh-token", tags=["Refresh Token"])
