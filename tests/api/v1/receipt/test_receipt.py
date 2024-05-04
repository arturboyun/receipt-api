import datetime

import pytest
from faker import Faker
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
    assert response_data["total"] == 1
    assert response_data["items"][0]["id"] == receipt.id
    assert response_data["items"][0]["payment"]["type"] == receipt.payment.type.value
    assert response_data["items"][0]["payment"]["amount"] == receipt.payment.amount
    assert response_data["items"][0]["products"] == [
        {"name": "test1", "price": 123.0, "quantity": 2, "total": 246.0},
        {"name": "asdf", "price": 21.0, "quantity": 6, "total": 126.0},
    ]


@pytest.mark.asyncio
async def test_get_receipts_pagination(client: TestClient, session: AsyncSession) -> None:
    auth_headers = await get_access_token_headers()
    for _ in range(10):
        await create_random_receipt(session, "cash")
    for _ in range(10):
        await create_random_receipt(session, "card")

    response = client.get("/api/v1/receipt?limit=10", headers=auth_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert "total" in response_data
    assert "items" in response_data
    assert "limit" in response_data
    assert "offset" in response_data
    assert isinstance(response_data["total"], int)
    assert isinstance(response_data["items"], list)
    assert isinstance(response_data["limit"], int)
    assert isinstance(response_data["offset"], int)
    assert response_data["total"] == 20
    assert len(response_data["items"]) == 10


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
        assert response_data["total"] == 3
    if payment_type == "card":
        assert response_data["total"] == 2
    for item in response_data["items"]:
        assert item["payment"]["type"] == payment_type


@pytest.mark.asyncio
async def test_get_receipts_filter_by_created_at(client: TestClient, session: AsyncSession, faker: Faker) -> None:
    auth_headers = await get_access_token_headers()
    date_from = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=30)
    out_of_range_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=100)
    date_to = datetime.datetime.now(datetime.UTC)

    for _ in range(6):
        created_at = faker.date_time_between(start_date=date_from, end_date=date_to)
        await create_random_receipt(session, "cash", created_at=created_at)

    await create_random_receipt(session, "cash", created_at=out_of_range_date)
    await create_random_receipt(session, "cash", created_at=out_of_range_date)
    await create_random_receipt(session, "cash", created_at=out_of_range_date)
    await create_random_receipt(session, "card", created_at=out_of_range_date)
    await create_random_receipt(session, "card", created_at=out_of_range_date)

    search_date_from = date_from.strftime("%Y-%m-%d %H:%M:%S")
    search_date_to = date_to.strftime("%Y-%m-%d %H:%M:%S")
    response = client.get(
        f"/api/v1/receipt?created_at__gte={search_date_from}&created_at__lte={search_date_to}",
        headers=auth_headers,
    )
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
    assert response_data["total"] == 6
    for item in response_data["items"]:
        assert date_from <= datetime.datetime.fromisoformat(item["created_at"]) <= date_to


@pytest.mark.asyncio
async def test_get_receipts_filter_by_total(client: TestClient, session: AsyncSession) -> None:
    auth_headers = await get_access_token_headers()
    await create_random_receipt(session, "cash", total=100)
    await create_random_receipt(session, "cash", total=100)
    await create_random_receipt(session, "cash", total=100)

    await create_random_receipt(session, "cash", total=200)
    await create_random_receipt(session, "cash", total=200)

    await create_random_receipt(session, "cash", total=300)
    await create_random_receipt(session, "cash", total=300)

    response = client.get("/api/v1/receipt?total=100", headers=auth_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["total"] == 3
    for item in response_data["items"]:
        assert item["total"] == 100

    response = client.get("/api/v1/receipt?total=200", headers=auth_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["total"] == 2
    for item in response_data["items"]:
        assert item["total"] == 200

    response = client.get("/api/v1/receipt?total__gt=100", headers=auth_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["total"] == 4
    for item in response_data["items"]:
        assert item["total"] > 100


@pytest.mark.asyncio
async def test_get_receipt_raw(client: TestClient, session: AsyncSession) -> None:
    auth_headers = await get_access_token_headers()
    receipt = await create_random_receipt(session, "cash")

    response = client.get(f"/api/v1/receipt/raw/{receipt.id}", headers=auth_headers)
    response_data = response.text
    assert response.status_code == 200
    assert receipt.user.name in response_data

    response = client.get(f"/api/v1/receipt/raw/{receipt.id + 1}", headers=auth_headers)
    assert response.status_code == 404
