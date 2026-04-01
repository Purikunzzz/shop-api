from sqlalchemy import String, Integer, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    balance: Mapped[float] = mapped_column(
        Numeric(12, 2), default=0
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now()
    )

    # relationship = บอกว่า user มีหลาย order
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user"
    )