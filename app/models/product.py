from sqlalchemy import String, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    stock: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    orders: Mapped[list["Order"]] = relationship(back_populates="product")