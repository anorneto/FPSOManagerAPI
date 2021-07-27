from datetime import datetime
from typing import List, Union
import json

from fastapi.testclient import TestClient
from fastapi import status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import Base, get_db

from main import api
from api.schemas.vessel_schema import VesselCreate
from api.schemas.equipment_schema import EquipmentCreate, EquipmentUpdate, EquipmentRead, EquipmentDelete
from api.settings import RouteSettings

from .fixtures import vessel_fixed,vessel_random,equipment_create_update_fixed,equipment_create_update_random

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

routes = RouteSettings()

# Helpers

def post_vessel(vessel: VesselCreate):
    response = client.post(
        routes.vessels,
        json= vessel,
    )
    return response

def post_equipment(vessel_code: str, equipment: EquipmentUpdate):
  print(routes.vessels + f"/{vessel_code}" + routes.equipments)
  response = client.post(
      routes.vessels + f"/{vessel_code}" + routes.equipments,
      json= equipment,
  )
  print(response)
  return response

def put_equipment(vessel_code: str, equipment: EquipmentUpdate):
    response = client.put(
        routes.vessels + f"/{vessel_code}" + routes.equipments,
        json= equipment,
    )
    return response

def delete_equipment(vessel_code: str, eqps_list: List[EquipmentDelete] ):
    response = client.delete(
        routes.vessels + f"/{vessel_code}" + routes.equipments + "/deactivate",
        json= eqps_list,
    )

# Test Cases

def test_equipment_post_created(vessel_fixed: VesselCreate, equipment_create_update_fixed : EquipmentCreate): # creates equipment_create_update_fixed
  post_vessel(vessel_fixed)
  response = post_equipment(vessel_code=vessel_fixed.get("code"), equipment= equipment_create_update_fixed)
  assert response.status_code == status.HTTP_201_CREATED
  json_response = response.json()
  assert json_response.get("code") == equipment_create_update_fixed.get("code")
  assert json_response.get("location") == equipment_create_update_fixed.get("location")
  assert json_response.get("name") == equipment_create_update_fixed.get("name")

def test_equipment_post_conflict(vessel_fixed: VesselCreate,equipment_create_update_fixed: EquipmentCreate): # validates conflict when trying to create equipment_create_update_fixed again
  response = post_equipment(vessel_code=vessel_fixed.get("code"), equipment= equipment_create_update_fixed)
  assert response.status_code == status.HTTP_409_CONFLICT
  json_response = response.json()
  assert json_response.get("detail") == "Equipment code already registered"

def test_equipment_post_vessel_not_found(vessel_random: VesselCreate,equipment_create_update_fixed: EquipmentCreate): # validates error when trying to insert equipment into inexistent vessel
  response = post_equipment(vessel_code=vessel_random.get("code"), equipment= equipment_create_update_fixed)
  assert response.status_code == status.HTTP_404_NOT_FOUND
  json_response = response.json()
  assert json_response["detail"] == "Vessel not found"

def test_equipment_post_unprocessable_entity_code(vessel_fixed: VesselCreate): # validates error when trying to insert equipment with empty code
  response = post_equipment(vessel_code=vessel_fixed.get("code"), equipment= {"code": "  ","name": "compressor", "location": "Brazil"})
  assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
  json_response = response.json()
  assert json_response["detail"][0]["msg"] == "Equipment Code cannot be empty"


def test_equipment_put_ok(vessel_fixed: VesselCreate, equipment_create_update_fixed : EquipmentUpdate): # updates equipment_create_update_fixed
  equipment_create_update_fixed["location"] = "USA"
  equipment_create_update_fixed["name"] = "FakeEquipmentName"
  response = put_equipment(vessel_code=vessel_fixed.get("code"), equipment= equipment_create_update_fixed)
  assert response.status_code == status.HTTP_200_OK
  json_response = response.json()
  assert json_response.get("code") == equipment_create_update_fixed.get("code")
  assert json_response.get("location") == "USA"
  assert json_response.get("name") == "FakeEquipmentName"

def test_equipment_put_unprocessable_entity_code(vessel_fixed: VesselCreate): # validates error when trying to update equipment with empty code
  response = put_equipment(vessel_code=vessel_fixed.get("code"), equipment= {"code": "  ","name": "compressor", "location": "Brazil"})
  assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
  json_response = response.json()
  assert json_response["detail"][0]["msg"] == "Equipment Code cannot be empty"


def test_equipment_put_not_found(vessel_fixed: VesselCreate, equipment_create_update_random : EquipmentUpdate): # validates error when trying to update inexistent equipment
  response = put_equipment(vessel_code=vessel_fixed.get("code"), equipment= equipment_create_update_random)
  assert response.status_code == status.HTTP_404_NOT_FOUND
  json_response = response.json()
  assert json_response["detail"] == "Equipment not found"

def test_equipment_put_vessel_not_found(vessel_random: VesselCreate, equipment_create_update_random : EquipmentUpdate): # validates error when trying to update equipment of inexistent vessel
  response = put_equipment(vessel_code=vessel_random.get("code"), equipment= equipment_create_update_random)
  assert response.status_code == status.HTTP_404_NOT_FOUND
  json_response = response.json()
  assert json_response["detail"] == "Vessel not found"

def test_equipment_del_no_content(vessel_fixed: VesselCreate, equipment_create_update_fixed : EquipmentUpdate): # validates error when trying to update inexistent equipment
  response = delete_equipment(vessel_code=vessel_fixed.get("code"), eqps_list= list(equipment_create_update_fixed))
  assert response == None

def test_equipment_del_no_content(vessel_fixed: VesselCreate, equipment_create_update_fixed : EquipmentDelete): # validates error when trying to update inexistent equipment
  response = delete_equipment(vessel_code={"code" : "112314"}, eqps_list= list(equipment_create_update_fixed))
  assert response == None