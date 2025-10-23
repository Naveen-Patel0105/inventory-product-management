from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from typing import List, Optional
from app import models, schemas

# --------- PRODUCTS ---------
async def create_product(db: AsyncSession, product_in: schemas.ProductCreate) -> models.Product:
    product = models.Product(**product_in.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

async def get_product(db: AsyncSession, product_id: int) -> Optional[models.Product]:
    return await db.get(models.Product, product_id)

async def list_products(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Product]:
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    return result.scalars().all()

async def update_product(db: AsyncSession, product_id: int, patch: schemas.ProductUpdate) -> models.Product:
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in patch.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

async def adjust_stock(db: AsyncSession, product_id: int, adjustment: int) -> models.Product:
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    new_qty = product.quantity + adjustment
    if new_qty < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot go below zero")
    product.quantity = new_qty
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

