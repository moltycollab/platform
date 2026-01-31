import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "version" in response.json()

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "MoltyCollab"

def test_list_moltys():
    response = client.get("/api/v1/moltys/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_proyectos():
    response = client.get("/api/v1/proyectos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_proyecto_validation():
    """Test que validación rechaza datos incompletos"""
    response = client.post("/api/v1/proyectos/", json={
        "nombre": "A",  # Too short
        "descripcion": "test"
    })
    assert response.status_code == 422  # Validation error
