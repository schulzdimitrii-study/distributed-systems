import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    client.delete("/api/v1/alunos/")

@pytest.fixture
def populate_db():
    students_data = [
        {"name": "Alice GES", "email": "alice@ges.inatel.br", "course": "GES"},
        {"name": "Bob GES", "email": "bob@ges.inatel.br", "course": "GES"},
        {"name": "Charlie GES", "email": "charlie@ges.inatel.br", "course": "GES"},
        {"name": "Dave GEC", "email": "dave@gec.inatel.br", "course": "GEC"},
        {"name": "Eve GEC", "email": "eve@gec.inatel.br", "course": "GEC"},
        {"name": "Frank GEC", "email": "frank@gec.inatel.br", "course": "GEC"}
    ]
    for data in students_data:
        client.post("/api/v1/alunos/", json=data)

def test_add_students():
    r1 = client.post("/api/v1/alunos/", json={"name": "Alice GES", "email": "alice@ges.inatel.br", "course": "GES"})
    assert r1.status_code == 201
    assert r1.json()["id"] == "GES1"
    
    r2 = client.post("/api/v1/alunos/", json={"name": "Dave GEC", "email": "dave@gec.inatel.br", "course": "GEC"})
    assert r2.status_code == 201
    assert r2.json()["id"] == "GEC1"

def test_list_students(populate_db):
    response = client.get("/api/v1/alunos/")
    assert response.status_code == 200
    assert len(response.json()) == 6

def test_get_student_by_id(populate_db):
    response = client.get("/api/v1/alunos/GES2")
    assert response.status_code == 200
    assert response.json()["name"] == "Bob GES"
    assert response.json()["email"] == "bob@ges.inatel.br"

def test_update_student(populate_db):
    response = client.patch("/api/v1/alunos/GES1", json={"name": "Alice Updated", "email": "alice_updated@ges.inatel.br"})
    assert response.status_code == 200
    assert response.json()["name"] == "Alice Updated"
    assert response.json()["email"] == "alice_updated@ges.inatel.br"
    assert response.json()["id"] == "GES1"

def test_remove_student(populate_db):
    response = client.delete("/api/v1/alunos/GEC3")
    assert response.status_code == 204
    
    response_list = client.get("/api/v1/alunos/")
    assert len(response_list.json()) == 5
    
    response_get = client.get("/api/v1/alunos/GEC3")
    assert response_get.status_code == 404

def test_reset_students(populate_db):
    assert len(client.get("/api/v1/alunos/").json()) == 6
    
    response = client.delete("/api/v1/alunos/")
    assert response.status_code == 204
    
    assert len(client.get("/api/v1/alunos/").json()) == 0