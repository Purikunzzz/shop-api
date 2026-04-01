from pydantic import BaseModel, field_validator
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str | None
    price: float
    stock: int = 0

    @field_validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be more than 0")
        return v
    

    @field_validator("stock")
    def stock_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Stock can't be negative")
        return v

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock:int
    created_at: datetime

    model_config = {"from_attributes": True}
