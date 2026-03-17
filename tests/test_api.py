import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test 1: Verificar creación de zona (Requisito previo)
def test_create_zone():
    response = client.post("/zones/", json={
        "nombre": "Centro", "codigo_postal": "28001", "limite_velocidad": 30
    })
    assert response.status_code == 200

# Test 2: Crear patinete vinculado a zona [cite: 54]
def test_create_scooter():
    response = client.post("/scooters/", json={
        "numero_serie": "ABC-123", "modelo": "Xiaomi Pro", 
        "bateria": 50, "estado": "disponible", "zona_id": 1
    })
    assert response.status_code == 200
    assert response.json()["zona_id"] == 1

# Test 3: Validación de batería > 100 (Error 422) [cite: 55]
def test_battery_validation_high():
    response = client.post("/scooters/", json={
        "numero_serie": "ERR-1", "modelo": "X", 
        "bateria": 150, "estado": "disponible", "zona_id": 1
    })
    assert response.status_code == 422

# Test 4: Validación de batería < 0 (Error 422) [cite: 48]
def test_battery_validation_low():
    response = client.post("/scooters/", json={
        "numero_serie": "ERR-2", "modelo": "X", 
        "bateria": -10, "estado": "disponible", "zona_id": 1
    })
    assert response.status_code == 422

# Test 5: Lógica de paso a mantenimiento [cite: 56]
def test_mantenimiento_logic():
    # Creamos un patinete con poca batería
    client.post("/scooters/", json={
        "numero_serie": "LOW-BAT", "modelo": "X", 
        "bateria": 10, "estado": "disponible", "zona_id": 1
    })
    # Ejecutamos el endpoint especial [cite: 49]
    response = client.post("/zonas/1/mantenimiento")
    assert response.status_code == 200
    assert "1 patinetes" in response.json()["message"]