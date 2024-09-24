from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud, database

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.post("/", response_model=schemas.OrderOut, status_code=201)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(database.get_async_session)):
    return await crud.create_order(db, order)


@router.get("/", response_model=List[schemas.OrderOut])
async def read_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_async_session)):
    orders = await crud.get_orders(db, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=schemas.OrderOut)
async def read_order(order_id: int, db: AsyncSession = Depends(database.get_async_session)):
    return await crud.get_order(db, order_id)


@router.patch("/{order_id}/status", response_model=schemas.OrderOut)
async def update_order_status(order_id: int, status: schemas.OrderUpdateStatus,
                              db: AsyncSession = Depends(database.get_async_session)):
    return await crud.update_order_status(db, order_id, status)
