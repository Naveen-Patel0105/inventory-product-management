from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from typing import List, Optional
from app import models, schemas

# --------- CATEGORIES ---------
async def create_category(db: AsyncSession, name: str) -> models.Category:
    category = models.Category(name=name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

async def list_categories(db: AsyncSession) -> List[models.Category]:
    result = await db.execute(select(models.Category))
    return result.scalars().all()

async def get_category(db: AsyncSession, category_id: int) -> Optional[models.Category]:
    return await db.get(models.Category, category_id)