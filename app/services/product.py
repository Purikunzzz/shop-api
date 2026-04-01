from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

class ProductService:

    async def get_by_id(
            self, db: AsyncSession, product_id: int
    ) -> Product | None:
        result = await db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
            self, db: AsyncSession
    ) -> list[Product]:
        result = await db.execute(select(Product))
        return list(result.scalars().all())

    async def create(
            self, db: AsyncSession, data: ProductCreate
    ) -> Product:
        product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            stock=data.stock
        )
        db.add(product)
        await db.flush()
        return product
    
    async def update(
            self, db: AsyncSession, product_id: int, data: ProductUpdate
    ) -> Product:
        product = await self.get_by_id(db, product_id)
        if not product:
            raise ValueError(f"{product_id} is not found")

        update_data = data.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        return product

    async def delete(
            self, db: AsyncSession, product_id: int
    ) -> None:
        product = await self.get_by_id(db, product_id)
        if not product:
            raise ValueError(f"{product_id} is not found")
        await db.delete(product)

product_service = ProductService()
