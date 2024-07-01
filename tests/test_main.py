from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient
import pytest

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def test_login():
    form_data = {"username": "Lattja", "password": "123123"
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.anyio
async def test_registry():
    register_data = {
        "username": "test_username",
        "email": "test_email@gmail.com",
        "full_name": "test_full_name",
        "password": "test_password"
        }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/registry", json=register_data)
        assert response.status_code == 200
        assert response.json() == {
            "username": "test_username",
            "email": "test_email@gmail.com",
            "full_name": "test_full_name",
        }
    
