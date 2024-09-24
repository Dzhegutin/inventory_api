from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum
from datetime import datetime


class OrderStatus(str, Enum):
    in_progress = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]


class ProductOut(ProductBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdateStatus(BaseModel):
    status: OrderStatus


class OrderOut(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItemOut]

    class Config:
        model_config = ConfigDict(from_attributes=True)