import pytest
from app.routes.user import fake_db
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_fake_db():
    fake_db.clear()


def test_post_user():
    response = client.post("/users/",
                           json={
                               "name": "John Doe",
                               "email": "johnDoe@gmail.com"
                            })
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "John Doe", "email": "johnDoe@gmail.com"}


def test_get_user():
    client.post("/users/", json={"name": "John Doe", "email": "johnDoe@gmail.com"})
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "email": "johnDoe@gmail.com"}
    

def test_list_users():
    client.post("/users/", json={"name": "John Doe", "email": "johnDoe@gmail.com"})
    client.post("/users/", json={"name": "Jane Doe", "email": "janeDoe@hotmail.com"})
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "John Doe", "email": "johnDoe@gmail.com"},
        {"id": 2, "name": "Jane Doe", "email": "janeDoe@hotmail.com"}
    ]
    
def test_update_user():
    client.post("/users/", json={"name": "John Doe", "email": "janeDoe@hotmail.com"})
    response = client.put("/users/1", json={"name": "John Doe", "email": "johnDoe@gmail.com"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "email": "johnDoe@gmail.com"}
    
def test_delete_user():
    client.post("/users/", json={"name": "John Doe", "email": "johnDoe@gmail.com"})
    response = client.delete("/users/1")
    
    assert response.status_code == 204
    assert response.content == b""
    response = client.get("/users/1")
    assert response.status_code == 404