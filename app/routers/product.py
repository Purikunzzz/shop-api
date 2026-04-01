from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductResponse])
async def get_all_products(
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_all(db)

@router.get("/{product_id}", response_model= ProductResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    product = await product_service.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    body: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await product_service.create(db, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    body: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await product_service.update(db, product_id, body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    try: 
        return await product_service.delete(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
