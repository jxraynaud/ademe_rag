from fastapi.testclient import TestClient
from app.server import app
from unittest.mock import patch

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Greetings from the server!"}

@patch("app.server.process_carb_equiv")
def test_create_carb_equiv(mock_process_carb_equiv):
    mock_process_carb_equiv.return_value = {"processed_data": "mocked_data"}
    test_payload = {"name": "sugar", "description": "white sugar", "unit": "grams", "quantity": 100}

    response = client.post("/carb_equiv", json=test_payload)

    assert response.status_code == 200
    assert response.json() == {"payload_processed": {"processed_data": "mocked_data"}}
