from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password ต้องมีอย่างน้อย 8 ตัว")
        return v
    
class UserUpdate(BaseModel):
    name: str | None = None
    balance: float | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    balance: float
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}