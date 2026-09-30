from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Banking Customer Portal is running" in response.data


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "UP"


def test_register_customer():
    client = app.test_client()

    response = client.post(
        "/customers",
        json={
            "name": "John Doe",
            "email": "john@example.com"
        }
    )

    assert response.status_code == 201
    assert response.json["name"] == "John Doe"
    assert response.json["email"] == "john@example.com"


def test_get_customer():
    client = app.test_client()

    response = client.get("/customers/1")

    assert response.status_code == 200