from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.order import OrderCreated, OrderResponse
from app.services.order import order_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/user/{user_id}", response_model=list[OrderResponse])
async def get_user_order(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await order_service.get_by_user(db, user_id)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    order = await order_service.get_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

@router.post("/user/{user_id}", response_model=OrderResponse, status_code=201)
async def create_order(
    user_id: int,
    body: OrderCreated,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await order_service.create(db, user_id, body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


