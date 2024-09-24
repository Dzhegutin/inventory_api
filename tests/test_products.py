import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(ac: AsyncClient):
    response = await ac.post("/products/", json={
        "name": "Test Product",
        "description": "A product for testing",
        "price": 10.99,
        "quantity": 100
    })
    assert response.status_code == 201, f"Response: {response.text}"
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["quantity"] == 100


@pytest.mark.asyncio
async def test_get_products(ac: AsyncClient):
    response = await ac.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_product_not_found(ac: AsyncClient):
    response = await ac.get("/products/9999")
    assert response.status_code == 404
