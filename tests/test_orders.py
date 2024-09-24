import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_order(ac: AsyncClient):
    product_response = await ac.post("/products/", json={
        "name": "Order Test Product",
        "description": "Product for order testing",
        "price": 20.0,
        "quantity": 50
    })
    assert product_response.status_code == 201
    product = product_response.json()

    order_response = await ac.post("/orders/", json={
        "items": [
            {
                "product_id": product["id"],
                "quantity": 5
            }
        ]
    })
    assert order_response.status_code == 201
    order = order_response.json()
    assert order["status"] == "в процессе"
    assert len(order["items"]) == 1
    assert order["items"][0]["quantity"] == 5

    updated_product_response = await ac.get(f"/products/{product['id']}")
    updated_product = updated_product_response.json()
    assert updated_product["quantity"] == 45


@pytest.mark.asyncio
async def test_create_order_insufficient_stock(ac: AsyncClient):
    product_response = await ac.post("/products/", json={
        "name": "Limited Product",
        "description": "Limited stock",
        "price": 15.0,
        "quantity": 2
    })
    assert product_response.status_code == 201
    product = product_response.json()

    order_response = await ac.post("/orders/", json={
        "items": [
            {
                "product_id": product["id"],
                "quantity": 5
            }
        ]
    })
    assert order_response.status_code == 400
    assert "Insufficient stock" in order_response.json()["detail"]
