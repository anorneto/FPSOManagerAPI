from typing import List
from fastapi import APIRouter,Depends,status
from fastapi.responses import Response

from api.settings import RouteSettings
from api.database import get_db
from api.bll.equipment_bus import EquipmentBus
from api.schemas.equipment_schema import EquipmentRead, EquipmentCreate, EquipmentUpdate, EquipmentDelete

route_settings = RouteSettings()

router = APIRouter(prefix = route_settings.vessels)

@router.get(
  "/{vessel_code}" + route_settings.equipments,tags=["Vessels"] ,
  response_model=List[EquipmentRead] ,
  status_code= status.HTTP_200_OK ,
  summary="Get vessel equipments",
  description="Return vessel's active arquipments",
  responses={
    200 : {"model": List[EquipmentRead], "description": "The vessel's active equipments'"},
    404:  {"description": "Vessel not Found", "content":{ "application/json": { "example": {"detail": "Vessel not found"} } }}
  }
)
async def get_vessel_equipments(vessel_code:str, filter_inactive: bool = True, db = Depends( get_db)):
  bus = EquipmentBus(db)
  db_active_equipments_list = bus.get_equipments(vessel_code= vessel_code, filter_inactive= filter_inactive)
  return db_active_equipments_list

@router.post(
  "/{vessel_code}" + route_settings.equipments,tags=["Vessels"],
  response_model=EquipmentRead,
  status_code= status.HTTP_201_CREATED,
  summary="Create vessel's equipment",
  description="Create vessel's equipment and returns it",
  responses={
    201 : {"model": EquipmentRead, "description": "The vessel's created equipment'"},
    404:  {"description": "Vessel not Found", "content":{ "application/json": { "example": {"detail": "Vessel not found"} } }},
    409:  {"description": "Equipment code already registered", "content":{ "application/json": { "example": {"detail": "Equipment code already registered"} } }},
  }
)
async def create_vessel_equipment(vessel_code:str, equipment_create: EquipmentCreate, db = Depends( get_db)):
  bus = EquipmentBus(db)
  db_equipment = bus.create_equipment(vessel_code= vessel_code, equipment_create= equipment_create)
  return db_equipment

@router.put(
  "/{vessel_code}" + route_settings.equipments,
  tags=["Vessels"],
  response_model=EquipmentRead,
  status_code= status.HTTP_200_OK,
  summary="Updates vessel's equipment",
  description="Updates vessel's equipment and returns it",
  responses={
    200: {"model": EquipmentRead, "description": "The vessel's updated equipment'"},
    404:  {"description": "Vessel not Found", "content":{ "application/json": { "example": {"detail": "Vessel not found"} } }},
    404:  {"description": "Equipment not found", "content":{ "application/json": { "example": {"detail": "Equipment not found"} } }},
  }
)
async def update_vessel_equipment(vessel_code:str, equipment_update: EquipmentUpdate, db = Depends( get_db)):
  bus = EquipmentBus(db)
  db_equipment = bus.update_equipment(vessel_code= vessel_code, equipment_update= equipment_update)
  return db_equipment

@router.delete(
  "/{vessel_code}" + route_settings.equipments + "/deactivate",tags=["Vessels"],
  response_class=Response,
  status_code= status.HTTP_204_NO_CONTENT,
  summary="Delete vessel's equipment",
  description="Delete vessel's equipment, returns no content",
  responses={
    204:  {"description": "No Content"},
    404:  {"description": "Vessel not Found", "content":{ "application/json": { "example": {"detail": "Vessel not Found"} } }},
  }
)
async def delete_vessel_equipments(vessel_code:str, eqps_delete_list: List[EquipmentDelete], db = Depends( get_db)):
  bus = EquipmentBus(db)
  bus.delete_equipments(vessel_code= vessel_code, eqps_delete_list= eqps_delete_list)
