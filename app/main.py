from fastapi import FastAPI
from .routers import products, orders
from .database import engine
from .models import Base

app = FastAPI(title="Inventory Management API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(products.router)
app.include_router(orders.router)
