from datetime import datetime
from typing import List
import json

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

def test_post_created_vessel(vessel_code_fixed: VesselCreate): # creates vessel_code_fixed
    response = post_vessel(vessel_code_fixed)
    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response.get("code") == vessel_code_fixed.get("code")
    assert json_response.get("is_active") == True

def test_post_conflict_vessel(vessel_code_fixed: VesselCreate): # validates conflict when trying to create vessel_code_fixed again
  response = post_vessel(vessel_code_fixed)
  assert response.status_code == status.HTTP_409_CONFLICT
  json_response = response.json()
  assert json_response.get("detail") == "Vessel already registered"

def test_post_empty_vessel_code(): # validates error when trying to insert empty vessel code
  response = post_vessel({"code" : "                     "})
  assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
  json_response = response.json()
  assert json_response["detail"][0]["msg"] == "Vessel Code cannot be empty."


def test_get_all_vessels(vessel_code_fixed: VesselCreate): # Get all vessels and check if vessel_code_fixed exists
    response = client.get(vessel_route)
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert any(vessel.get("code") == vessel_code_fixed.get("code") for vessel in json_response )

def test_get_vessel_by_code(vessel_code_fixed: VesselCreate): # get vessel_code_fixed Vessel
    vessel_test_code = vessel_code_fixed.get("code")
    response = client.get(vessel_route + f"/{vessel_test_code}")
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response.get("code") == vessel_code_fixed.get("code")
