from datetime import datetime
from typing import List

from fastapi.testclient import TestClient
from fastapi import status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import Base, get_db

import pytest
from faker import Faker

from main import api
from api.schemas.vessel_schema import VesselCreate, VesselRead
from api.settings import RouteSettings

# Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine( SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} )
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

api.dependency_overrides[get_db] = override_get_db
client = TestClient(api)

vessel_route = RouteSettings().vessels

# Fixtures
fake = Faker()

@pytest.fixture(scope="function")
def vessel_code_random() -> VesselCreate:
    return {
        "code": fake.pystr(min_chars=5, max_chars=8)
    }

@pytest.fixture(scope="session")
def vessel_code_fixed() -> VesselCreate:
    return {
        "code": fake.pystr(min_chars=5, max_chars=8)
    }

# Helpers

def post_vessel(vessel: VesselCreate):
    response = client.post(
        vessel_route,
        json= vessel,
    )
    return response

# Test Cases

def test_post_created_vessel(vessel_code_fixed: VesselCreate):
    response = post_vessel(vessel_code_fixed)
    assert response.status_code == 201
    json_response = response.json()
    assert json_response.get("code") == vessel_code_fixed.get("code")
    assert json_response.get("is_active") == True

def test_post_conflict_vessel(vessel_code_fixed: VesselCreate):
  response = post_vessel(vessel_code_fixed)
  assert response.status_code == 409
  json_response = response.json()
  assert json_response.get("detail") == "Vessel already registered"

def test_get_all_vessels():
    response = client.get(vessel_route)
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert list(json_response) is List
