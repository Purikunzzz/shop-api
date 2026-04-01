from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order
from app.schemas.order import OrderCreated, OrderResponse

class OrderService:

    async def get_by_id(
            self, db: AsyncSession, order_id: int
    ) -> Order | None:
        result = await db.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    async def get_by_user(
            self, db: AsyncSession, user_id: int
    ) -> list[Order]:
        result = await db.execute(select(Order).where(Order.user_id == user_id))
        return list(result.scalars().all())

    async def create(
            self, db: AsyncSession, user_id: int, data: OrderCreated
    ) -> Order:
        from app.services.product import product_service

        # check product
        product = await product_service.get_by_id(db, data.product_id)
        if not product:
            raise ValueError(f"{data.product_id} is not found")
        
        # check stock
        if product.stock < data.quantity:
            raise ValueError(f"Stock ไม่พอ มีแค่{product.stock}")

        # total price
        total_price = product.price * data.quantity

        # ลด stock
        product.stock -= data.quantity

        # create order
        order = Order(
            user_id = user_id,
            product_id = data.product_id,
            quantity = data.quantity,
            total_price = float(total_price)
        )
        db.add(order)
        await db.flush()
        return order
    
order_service = OrderService()