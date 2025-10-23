from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas
from services import product_crud
from db import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    return await product_crud.create_product(db, product_in)

@router.get("/", response_model=List[schemas.Product])
async def list_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await product_crud.list_products(db, skip, limit)

@router.get("/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.Product)
async def update_product(product_id: int, product_update: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await product_crud.update_product(db, product_id, product_update)

@router.patch("/{product_id}/stock", response_model=schemas.Product)
async def adjust_stock(product_id: int, adj: schemas.StockAdjustment, db: AsyncSession = Depends(get_db)):
    return await product_crud.adjust_stock(db, product_id, adj.adjustment)
