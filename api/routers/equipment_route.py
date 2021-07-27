from typing import List
from fastapi import APIRouter,Depends,status
from fastapi.responses import Response

from api.settings import RouteSettings
from api.database import get_db
from api.bll.equipment_bus import EquipmentBus
from api.schemas.equipment_schema import EquipmentRead, EquipmentCreate, EquipmentUpdate, EquipmentDelete

route_settings = RouteSettings()

router = APIRouter(prefix = route_settings.vessels)

@router.get("/{vessel_code}" + route_settings.equipments, response_model=List[EquipmentRead], status_code= status.HTTP_200_OK)
async def get_vessel_equipments(vessel_code:str, filter_inactive: bool = True, db = Depends( get_db)):
  bus = EquipmentBus(db)
  db_active_equipments_list = bus.get_equipments(vessel_code= vessel_code, filter_inactive= filter_inactive)
  return db_active_equipments_list

@router.post("/{vessel_code}" + route_settings.equipments, response_model=EquipmentRead, status_code= status.HTTP_201_CREATED)
async def create_vessel_equipment(vessel_code:str, equipment_create: EquipmentCreate, db = Depends( get_db)):
  bus = EquipmentBus(db)
  db_equipment = bus.create_equipment(vessel_code= vessel_code, equipment_create= equipment_create)
  return db_equipment

@router.put("/{vessel_code}" + route_settings.equipments, response_model=EquipmentRead, status_code= status.HTTP_200_OK)
async def update_vessel_equipment(vessel_code:str, equipment_update: EquipmentUpdate, db = Depends( get_db)):
  bus = EquipmentBus(db)
  db_equipment = bus.update_equipment(vessel_code= vessel_code, equipment_update= equipment_update)
  return db_equipment

@router.delete("/{vessel_code}" + route_settings.equipments + "/deactivate", response_class=Response, status_code= status.HTTP_204_NO_CONTENT)
async def delete_vessel_equipments(vessel_code:str, eqps_delete_list: List[EquipmentDelete], db = Depends( get_db)):
  bus = EquipmentBus(db)
  bus.deactivate_equipments(vessel_code= vessel_code, eqps_update_status_list= eqps_delete_list)
