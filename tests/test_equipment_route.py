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

from .fixtures import vessel_fixed,vessel_random,equipment_create_update_fixed,equipment_create_update_random,equipment_create_delete_fixed,list_equipment_create_delete_fixed

############ Setup ##############
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

############## Helpers ##############

def post_vessel(vessel: VesselCreate):
    response = client.post(
        routes.vessels,
        json= vessel,
    )
    return response

def get_equipments(vessel_code:str, filter_inactive:bool = True):
  route = routes.vessels + f"/{vessel_code}" + routes.equipments + f"?filter_inactive={filter_inactive}"
  response = client.get(
      route,
  )
  return response

def post_equipment(vessel_code: str, equipment: EquipmentUpdate):
  response = client.post(
      routes.vessels + f"/{vessel_code}" + routes.equipments,
      json= equipment,
  )
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
    return response

############# Test Cases #################

# creates equipment_create_update_fixed
def test_equipment_post_created(vessel_fixed: VesselCreate, equipment_create_update_fixed : EquipmentCreate):
  post_vessel(vessel_fixed)
  response = post_equipment(vessel_code=vessel_fixed.get("code"), equipment= equipment_create_update_fixed)
  assert response.status_code == status.HTTP_201_CREATED
  json_response = response.json()
  assert json_response.get("code") == equipment_create_update_fixed.get("code")
  assert json_response.get("location") == equipment_create_update_fixed.get("location")
  assert json_response.get("name") == equipment_create_update_fixed.get("name")

# validates get equipments works
def test_equipment_get_ok(vessel_fixed: VesselCreate, equipment_create_update_fixed : EquipmentCreate):
  response = get_equipments(vessel_code=vessel_fixed.get("code"))
  assert response.status_code == status.HTTP_200_OK

# validates error when trying to get equipments from inexistent vessel
def test_equipment_get_vessel_not_found():
  response = get_equipments(vessel_code={"code" : "12345"})
  assert response.status_code == status.HTTP_404_NOT_FOUND
  json_response = response.json()
  assert json_response.get("detail") == "Vessel not found"

# validates equipment_create_update_fixed exists in vessel_fixed
def test_equipment_exists_get_ok(vessel_fixed: VesselCreate, equipment_create_update_fixed : EquipmentCreate):
  response = get_equipments(vessel_code=vessel_fixed.get("code"))
  assert response.status_code == status.HTTP_200_OK
  json_response = response.json()
  assert any(equipment.get("code") == equipment_create_update_fixed.get("code") for equipment in json_response )

# validates conflict when trying to create equipment_create_update_fixed again
def test_equipment_post_conflict(vessel_fixed: VesselCreate,equipment_create_update_fixed: EquipmentCreate):
  response = post_equipment(vessel_code=vessel_fixed.get("code"), equipment= equipment_create_update_fixed)
  assert response.status_code == status.HTTP_409_CONFLICT
  json_response = response.json()
  assert json_response.get("detail") == "Equipment code already registered"

# validates error when trying to insert equipment into inexistent vessel
def test_equipment_post_vessel_not_found(vessel_random: VesselCreate,equipment_create_update_fixed: EquipmentCreate):
  response = post_equipment(vessel_code=vessel_random.get("code"), equipment= equipment_create_update_fixed)
  assert response.status_code == status.HTTP_404_NOT_FOUND
  json_response = response.json()
  assert json_response["detail"] == "Vessel not found"

# validates error when trying to insert equipment with empty code
def test_equipment_post_unprocessable_entity_code(vessel_fixed: VesselCreate):
  response = post_equipment(vessel_code=vessel_fixed.get("code"), equipment= {"code": "  ","name": "compressor", "location": "Brazil"})
  assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
  json_response = response.json()
  assert json_response["detail"][0]["msg"] == "Equipment Code cannot be empty"

# updates equipment_create_update_fixed
def test_equipment_put_ok(vessel_fixed: VesselCreate, equipment_create_update_fixed : EquipmentUpdate):
  equipment_create_update_fixed["location"] = "USA"
  equipment_create_update_fixed["name"] = "FakeEquipmentName"
  response = put_equipment(vessel_code=vessel_fixed.get("code"), equipment= equipment_create_update_fixed)
  assert response.status_code == status.HTTP_200_OK
  json_response = response.json()
  assert json_response.get("code") == equipment_create_update_fixed.get("code")
  assert json_response.get("location") == "USA"
  assert json_response.get("name") == "FakeEquipmentName"

# validates error when trying to update equipment with empty code
def test_equipment_put_unprocessable_entity_code(vessel_fixed: VesselCreate):
  response = put_equipment(vessel_code=vessel_fixed.get("code"), equipment= {"code": "  ","name": "compressor", "location": "Brazil"})
  assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
  json_response = response.json()
  assert json_response["detail"][0]["msg"] == "Equipment Code cannot be empty"

# validates error when trying to update inexistent equipment
def test_equipment_put_not_found(vessel_fixed: VesselCreate, equipment_create_update_random : EquipmentUpdate):
  response = put_equipment(vessel_code=vessel_fixed.get("code"), equipment= equipment_create_update_random)
  assert response.status_code == status.HTTP_404_NOT_FOUND
  json_response = response.json()
  assert json_response["detail"] == "Equipment not found"

# validates error when trying to update equipment of inexistent vessel
def test_equipment_put_vessel_not_found(vessel_random: VesselCreate, equipment_create_update_random : EquipmentUpdate):
  response = put_equipment(vessel_code=vessel_random.get("code"), equipment= equipment_create_update_random)
  assert response.status_code == status.HTTP_404_NOT_FOUND
  json_response = response.json()
  assert json_response["detail"] == "Vessel not found"

# validates no content when deleting equipment
def test_equipment_del_no_content(vessel_fixed: VesselCreate, equipment_create_delete_fixed : EquipmentDelete):
  response = delete_equipment(vessel_code=vessel_fixed.get("code"), eqps_list=[equipment_create_delete_fixed])
  assert response.status_code == status.HTTP_204_NO_CONTENT

# validates error when trying to delete equipment of inexistent vessel
def test_equipment_del_vessel_not_found(vessel_fixed: VesselCreate, equipment_create_delete_fixed : EquipmentDelete):
  response = delete_equipment(vessel_code={"code" : "1123232314"}, eqps_list= [equipment_create_delete_fixed])
  assert response.status_code == status.HTTP_404_NOT_FOUND
  json_response = response.json()
  assert json_response["detail"] == "Vessel not found"
# add equipments and validates they where added, than deactivate them and validates the deactivation
def test_equipment_create_exists_del_doesnt_exists(vessel_fixed: VesselCreate, list_equipment_create_delete_fixed: List[EquipmentDelete]):
  vessel_code = vessel_fixed.get("code")
  for equipment_create in list_equipment_create_delete_fixed:
    response_create = post_equipment(vessel_code=vessel_code, equipment=equipment_create)
    assert response_create.status_code == status.HTTP_201_CREATED
    assert response_create.json().get("code") == equipment_create.get("code")

  response_get = get_equipments(vessel_code=vessel_code)
  assert response_get.status_code == status.HTTP_200_OK
  for equipment_exists in response_get.json():
    assert any(equipment.get("code") == equipment_exists.get("code") for equipment in response_get.json())

  response_delete = delete_equipment(vessel_code=vessel_code, eqps_list=list_equipment_create_delete_fixed)
  response_delete.status_code == status.HTTP_204_NO_CONTENT

  response_get = get_equipments(vessel_code=vessel_code)
  assert response_get.status_code == status.HTTP_200_OK
  for equipment_deleted in list_equipment_create_delete_fixed:
    assert not any(equipment.get("code") == equipment_deleted.get("code") for equipment in response_get.json())

# validates equipments are listed when passing "filter_inactive=False" to the route
def test_equipment_create_exists_when_filter_inactive_false(vessel_fixed: VesselCreate, list_equipment_create_delete_fixed: List[EquipmentDelete]):
  vessel_code = vessel_fixed.get("code")

  response_get = get_equipments(vessel_code=vessel_code, filter_inactive=False)
  assert response_get.status_code == status.HTTP_200_OK
  for equipment_deleted in list_equipment_create_delete_fixed:
    assert any(equipment.get("code") == equipment_deleted.get("code") for equipment in response_get.json())