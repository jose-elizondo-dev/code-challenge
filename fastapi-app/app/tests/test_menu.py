from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

TOKEN = os.getenv("API_TOKEN", "123456")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


def test_create_item():
    payload = {
        "name": "Iced Tea",
        "category": "drink",
        "price": 6.50,
        "isAvailable": True,
    }

    response = client.post(
        "/api/menu",
        json=payload,
        headers=HEADERS,
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Iced Tea"
    assert data["category"] == "drink"
    assert data["price"] == 6.50
    assert data["isAvailable"] is True
    assert "id" in data


def test_create_item_without_token():
    payload = {
        "name": "No Auth",
        "category": "drink",
        "price": 5.0,
    }

    response = client.post("/api/menu", json=payload)

    assert response.status_code == 403 or response.status_code == 401


def test_list_menu_with_filters():
    response = client.get(
        "/api/menu",
        params={
            "search": "e",
            "category": "drink",
            "sort": "price",
            "order": "asc",
            "page": 1,
            "pageSize": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


def test_update_item_price():
    # Create item first
    create_res = client.post(
        "/api/menu",
        json={
            "name": "Update Test",
            "category": "drink",
            "price": 5.0,
        },
        headers=HEADERS,
    )

    item_id = create_res.json()["id"]

    # Update
    update_res = client.patch(
        f"/api/menu/{item_id}",
        json={"price": 7.0},
        headers=HEADERS,
    )

    assert update_res.status_code == 200
    assert update_res.json()["price"] == 7.0


def test_soft_delete_item():
    create_res = client.post(
        "/api/menu",
        json={
            "name": "Delete Test",
            "category": "drink",
            "price": 4.0,
        },
        headers=HEADERS,
    )

    item_id = create_res.json()["id"]

    delete_res = client.delete(
        f"/api/menu/{item_id}",
        headers=HEADERS,
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["isDeleted"] is True


def test_deleted_item_not_listed():
    response = client.get("/api/menu", params={"search": "Delete Test"})

    assert response.status_code == 200
    assert response.json()["total"] == 0
