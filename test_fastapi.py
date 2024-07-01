from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)

def test_root():
    response = client.get("/api/rest/v1/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}

def test_countries():
    response = client.get("/api/rest/v1/countries")
    assert response.status_code == 200
    # Add more assertions based on your expected response

def test_countries_year():
    response = client.get("/api/rest/v1/countries/year/2010")
    assert response.status_code == 200
    # Add more assertions based on your expected response