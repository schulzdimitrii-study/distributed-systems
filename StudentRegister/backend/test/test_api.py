def test_add_students(client):
    r = client.post("/api/v1/alunos/", json={
        "name": "Dimitri GES",
        "email": "dimitri@ges.inatel.br",
        "course": "GES"
    })
    assert r.status_code == 201
    assert r.json()["id"] == "GES1"
    assert r.json()["name"] == "Dimitri GES"
    assert r.json()["email"] == "dimitri@ges.inatel.br"
    assert r.json()["course"] == "GES"
    assert r.json()["mat"] == 1


def test_list_students(client, populate_db):
    response = client.get("/api/v1/alunos/")
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_get_student_by_id(client, populate_db):
    response = client.get("/api/v1/alunos/GES2")
    assert response.status_code == 200
    assert response.json()["id"] == "GES2"
    assert response.json()["name"] == "Bob GES"
    assert response.json()["email"] == "bob@ges.inatel.br"
    assert response.json()["mat"] == 2


def test_update_student(client, populate_db):
    response = client.patch("/api/v1/alunos/GES1", json={
        "name": "Alice Updated",
        "email": "alice_updated@ges.inatel.br"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Alice Updated"
    assert response.json()["email"] == "alice_updated@ges.inatel.br"
    assert response.json()["id"] == "GES1"


def test_remove_student(client, populate_db):
    response = client.delete("/api/v1/alunos/GEC3")
    assert response.status_code == 204

    response_list = client.get("/api/v1/alunos/")
    assert len(response_list.json()) == 5

    response_get = client.get("/api/v1/alunos/GEC3")
    assert response_get.status_code == 404


def test_reset_students(client, populate_db):
    assert len(client.get("/api/v1/alunos/").json()) == 6

    response = client.delete("/api/v1/alunos/")
    assert response.status_code == 204

    assert len(client.get("/api/v1/alunos/").json()) == 0