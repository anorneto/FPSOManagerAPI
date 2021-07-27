from datetime import datetime
from typing import List
import json

from fastapi.testclient import TestClient
from fastapi import status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import Base, get_db

from main import api
from api.schemas.vessel_schema import VesselCreate
from api.settings import RouteSettings


from .fixtures import vessel_fixed,vessel_random

############ Setup ###########

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

############## Helpers #############

def post_vessel(vessel: VesselCreate):
    response = client.post(
        vessel_route,
        json= vessel,
    )
    return response

########### Test Cases ################

# creates vessel_fixed
def test_post_created_vessel(vessel_fixed: VesselCreate):
    response = post_vessel(vessel_fixed)
    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response.get("code") == vessel_fixed.get("code")
# validates conflict when trying to create vessel_fixed again
def test_post_conflict_vessel(vessel_fixed: VesselCreate):
  response = post_vessel(vessel_fixed)
  assert response.status_code == status.HTTP_409_CONFLICT
  json_response = response.json()
  assert json_response.get("detail") == "Vessel already registered"
# validates error when trying to insert empty vessel code
def test_post_unprocessable_entity_vessel_code():
  response = post_vessel({"code" : "                     "})
  assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
  json_response = response.json()
  assert json_response["detail"][0]["msg"] == "Vessel Code cannot be empty"
# creates vessel_random
def test_post_created_random_vessel(vessel_random: VesselCreate):
    response = post_vessel(vessel_random)
    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response.get("code") == vessel_random.get("code")
# Get all vessels and check if vessel_fixed exists
def test_get_ok_all_vessels(vessel_fixed: VesselCreate):
    response = client.get(vessel_route)
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert any(vessel.get("code") == vessel_fixed.get("code") for vessel in json_response )
# get vessel_fixed Vessel
def test_get_ok_vessel_by_code(vessel_fixed: VesselCreate):
    vessel_test_code = vessel_fixed.get("code")
    response = client.get(vessel_route + f"/{vessel_test_code}")
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response.get("code") == vessel_fixed.get("code")
# get vessel_random Vessel
def test_get_not_found_vessel_by_code(vessel_random: VesselCreate):
    vessel_test_code = vessel_random.get("code")
    response = client.get(vessel_route + f"/{vessel_test_code}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert json_response.get("detail") == "Vessel not Found"
