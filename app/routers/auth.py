from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.user import user_service
from app.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    # find user from email
    user = await user_service.get_by_email(db, body.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email หรือ Password ไม่ถูกต้อง"
        )
    # check password
    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email หรือ Password ไม่ถูกต้อง"
        )
    
    # check is_active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ถูก deactivate แล้ว"
        )
    # create token
    token = create_access_token(user.id)
    return TokenResponse(access_token=token
                         )