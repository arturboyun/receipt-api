import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.api.v1.receipt.utils import create_random_receipt
from tests.utils.tokens import get_access_token_headers


@pytest.mark.asyncio
async def test_create_receipt(client: TestClient, session: AsyncSession) -> None:
    auth_headers = await get_access_token_headers()

    receipt = {
        "payment": {"type": "cash", "amount": 1000},
        "products": [
            {"name": "test1", "price": 123.0, "quantity": 2, "total": 246.0},
            {"name": "asdf", "price": 21.0, "quantity": 6, "total": 126.0},
        ],
    }
    response = client.post("/api/v1/receipt", json=receipt, headers=auth_headers)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["payment"]["type"] == receipt["payment"]["type"]
    assert response_data["payment"]["amount"] == receipt["payment"]["amount"]
    assert response_data["products"] == [
        {"name": "test1", "price": 123.0, "quantity": 2, "total": 246.0},
        {"name": "asdf", "price": 21.0, "quantity": 6, "total": 126.0},
    ]


@pytest.mark.asyncio
async def test_get_receipt(client: TestClient, session: AsyncSession) -> None:
    auth_headers = await get_access_token_headers()
    receipt = await create_random_receipt(session, "cash")
    print(receipt.id)

    response = client.get(f"/api/v1/receipt/{receipt.id}", headers=auth_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == receipt.id
    assert response_data["payment"]["type"] == receipt.payment.type.value
    assert response_data["payment"]["amount"] == receipt.payment.amount
    assert response_data["products"] == [
        {"name": "test1", "price": 123.0, "quantity": 2, "total": 246.0},
        {"name": "asdf", "price": 21.0, "quantity": 6, "total": 126.0},
    ]


@pytest.mark.asyncio
async def test_get_receipts(client: TestClient, session: AsyncSession) -> None:
    auth_headers = await get_access_token_headers()
    receipt = await create_random_receipt(session, "cash")

    response = client.get("/api/v1/receipt", headers=auth_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['total'] == 1
    assert response_data['items'][0]["id"] == receipt.id
    assert response_data['items'][0]["payment"]["type"] == receipt.payment.type.value
    assert response_data['items'][0]["payment"]["amount"] == receipt.payment.amount
    assert response_data['items'][0]["products"] == [
        {"name": "test1", "price": 123.0, "quantity": 2, "total": 246.0},
        {"name": "asdf", "price": 21.0, "quantity": 6, "total": 126.0},
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("payment_type", ["cash", "card"])
async def test_get_receipts_filter_by_payment_type(client: TestClient, session: AsyncSession, payment_type) -> None:
    auth_headers = await get_access_token_headers()
    await create_random_receipt(session, "cash")
    await create_random_receipt(session, "cash")
    await create_random_receipt(session, "cash")
    await create_random_receipt(session, "card")
    await create_random_receipt(session, "card")

    response = client.get(f"/api/v1/receipt?payment__type={payment_type}", headers=auth_headers)
    response_data = response.json()
    assert response.status_code == 200
    if payment_type == "cash":
        assert response_data['total'] == 3
    if payment_type == "card":
        assert response_data['total'] == 2
    for item in response_data['items']:
        assert item["payment"]["type"] == payment_type


@pytest.mark.asyncio
async def test_get_receipts_filter_by_created_at(client: TestClient, session: AsyncSession) -> None:
    auth_headers = await get_access_token_headers()
    await create_random_receipt(session, "cash")
    await create_random_receipt(session, "cash")
    await create_random_receipt(session, "cash")
    await create_random_receipt(session, "card")
    await create_random_receipt(session, "card")

    response = client.get("/api/v1/receipt?created_at__gte=2022-01-01T00:00:00&created_at__lt=2022-01-02T00:00:00",
                          headers=auth_headers)
