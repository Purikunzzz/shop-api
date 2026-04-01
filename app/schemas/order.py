from pydantic import BaseModel, field_validator
from datetime import datetime

class OrderCreated(BaseModel):
    product_id: int
    quantity: int = 1

    @field_validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be more than 0")

        return v
    
class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}

