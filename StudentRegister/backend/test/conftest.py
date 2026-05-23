import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from app.routes.student import service as student_service

_db: list[dict] = []


def _make_fake_conn():
    conn = MagicMock()

    async def execute(query: str, *args):
        q = query.strip().upper()

        if q.startswith("INSERT INTO STUDENTS"):
            name, email, course, mat = args
            _db.append({"name": name, "email": email, "course": course, "mat": mat})
            return "INSERT 1"

        if q.startswith("UPDATE STUDENTS"):
            name, email, course, filter_course, mat = args
            for row in _db:
                if row["course"] == filter_course and row["mat"] == mat:
                    row.update({"name": name, "email": email, "course": course})
            return "UPDATE 1"

        if q.startswith("DELETE FROM STUDENTS"):
            filter_course, mat = args
            before = len(_db)
            _db[:] = [r for r in _db if not (r["course"] == filter_course and r["mat"] == mat)]
            return f"DELETE {before - len(_db)}"

        if q.startswith("TRUNCATE"):
            _db.clear()
            return None

    async def fetch(query: str, *args):
        return [dict(r) for r in _db]

    async def fetchrow(query: str, *args):
        if len(args) == 2:
            course, mat = args
            for row in _db:
                if row["course"] == course and row["mat"] == mat:
                    return dict(row)
        return None

    async def close():
        pass

    conn.execute = execute
    conn.fetch = fetch
    conn.fetchrow = fetchrow
    conn.close = close
    return conn


async def _fake_get_connection():
    return _make_fake_conn()


@pytest.fixture(autouse=True)
def reset_state():
    _db.clear()
    student_service.course_sequences.clear()
    yield
    _db.clear()
    student_service.course_sequences.clear()


@pytest.fixture(autouse=True)
def mock_connection(reset_state):
    with patch("app.services.student_service.get_connection", new=_fake_get_connection):
        yield


@pytest.fixture
def client(mock_connection):
    return TestClient(app)


@pytest.fixture
def populate_db(client):
    students_data = [
        {"name": "Alice GES", "email": "alice@ges.inatel.br", "course": "GES"},
        {"name": "Bob GES", "email": "bob@ges.inatel.br", "course": "GES"},
        {"name": "Charlie GES", "email": "charlie@ges.inatel.br", "course": "GES"},
        {"name": "Dave GEC", "email": "dave@gec.inatel.br", "course": "GEC"},
        {"name": "Eve GEC", "email": "eve@gec.inatel.br", "course": "GEC"},
        {"name": "Frank GEC", "email": "frank@gec.inatel.br", "course": "GEC"},
    ]
    for data in students_data:
        client.post("/api/v1/alunos/", json=data)
