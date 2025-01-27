from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.jwt import (
    create_access_token,
    decode_token,
)
from app.schemas.auth import RefreshTokenRequest, AccessTokenResponse
from app.config import settings

router = APIRouter()



@router.post("/", response_model=AccessTokenResponse)
async def refresh_token(refresh_token_request: RefreshTokenRequest):

    try:
        payload = decode_token(
            refresh_token_request.refresh_token, settings.JWT_SECRET_KEY
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    access_token = create_access_token({"sub": username})
    return {"access_token": access_token}