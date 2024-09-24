from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud, database

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("/", response_model=schemas.ProductOut, status_code=201)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(database.get_async_session)):
    return await crud.create_product(db, product)


@router.get("/", response_model=List[schemas.ProductOut])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_async_session)):
    products = await crud.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=schemas.ProductOut)
async def read_product(product_id: int, db: AsyncSession = Depends(database.get_async_session)):
    return await crud.get_product(db, product_id)


@router.put("/{product_id}", response_model=schemas.ProductOut)
async def update_product(product_id: int, product: schemas.ProductUpdate,
                         db: AsyncSession = Depends(database.get_async_session)):
    return await crud.update_product(db, product_id, product)


@router.delete("/{product_id}", response_model=schemas.ProductOut)
async def delete_product(product_id: int, db: AsyncSession = Depends(database.get_async_session)):
    return await crud.delete_product(db, product_id)
