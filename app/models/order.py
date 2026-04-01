from sqlalchemy import Integer, ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
        )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
    total_price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0
        )
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now()
    )

    # relationship: User and Product
    user: Mapped["User"] = relationship(back_populates="orders")
    product: Mapped["Product"] = relationship(back_populates="orders")