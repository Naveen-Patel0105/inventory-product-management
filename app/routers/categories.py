from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas
from services import categories_crud
from db import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
async def create_category(category_in: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await categories_crud.create_category(db, category_in.name)

@router.get("/", response_model=List[schemas.Category])
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await categories_crud.list_categories(db)

@router.get("/{category_id}", response_model=schemas.Category)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await categories_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
