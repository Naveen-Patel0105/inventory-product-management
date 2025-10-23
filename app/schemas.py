from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(..., example="Electronics")

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., example="Battery Pack")
    sku: str = Field(..., example="BAT-001")
    category_id: Optional[int] = None
    unit_price: float = Field(..., ge=0)

class ProductCreate(ProductBase):
    quantity: int = Field(0, ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category_id: Optional[int] = None
    unit_price: Optional[float] = None
    quantity: Optional[int] = None

class Product(ProductBase):
    id: int
    quantity: int
    category: Optional[Category] = None
    class Config:
        from_attributes = True

class StockAdjustment(BaseModel):
    adjustment: int = Field(..., example=-5)
    reason: Optional[str] = Field(None, example="damaged item")
