from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from . import models, schemas
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    return result.scalars().all()


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, product_id: int, product: schemas.ProductUpdate):
    stmt = update(models.Product).where(models.Product.id == product_id).values(
        **product.dict(exclude_unset=True)).returning(models.Product)
    result = await db.execute(stmt)
    updated_product = result.scalar_one_or_none()
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.commit()
    return updated_product


async def delete_product(db: AsyncSession, product_id: int):
    stmt = delete(models.Product).where(models.Product.id == product_id).returning(models.Product)
    result = await db.execute(stmt)
    deleted_product = result.scalar_one_or_none()
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.commit()
    return deleted_product


async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(models.Order).where(models.Order.id == order_id).options(selectinload(models.Order.items)))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.items))
        .offset(skip)
        .limit(limit)
    )
    orders = result.scalars().all()
    return orders


async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    for item in order.items:
        product = await get_product(db, item.product_id)
        if product.quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")

    db_order = models.Order(status=models.OrderStatus.in_progress)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    for item in order.items:
        db_item = models.OrderItem(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(db_item)
        product = await get_product(db, item.product_id)
        product.quantity -= item.quantity
        db.add(product)

    await db.commit()
    await db.refresh(db_order, attribute_names=["items"])
    return db_order


async def update_order_status(db: AsyncSession, order_id: int, status: schemas.OrderUpdateStatus):
    stmt = update(models.Order).where(models.Order.id == order_id).values(status=status.status).returning(
        models.Order).options(selectinload(models.Order.items))
    result = await db.execute(stmt)
    updated_order = result.scalar_one_or_none()
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    await db.commit()
    return updated_order
