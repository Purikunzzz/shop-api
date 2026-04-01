from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user import user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_service.get_all(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.create(db, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    body: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await user_service.update(db, user_id, body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    
@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        await user_service.delete(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

