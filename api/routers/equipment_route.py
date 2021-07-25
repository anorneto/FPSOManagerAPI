from typing import List
from fastapi import APIRouter,Depends,status,HTTPException

from api.settings import RouteSettings
from api.database import get_db
from api.bll.equipment_bus import EquipmentBus
from api.schemas.equipment_schema import EquipmentRead, EquipmentCreate, EquipmentUpdate, EquipmentDelete

route_settings = RouteSettings()

router = APIRouter(prefix = route_settings.vessels)

@router.get("/equipments")
async def get_vessles():
  return "Vessels"

@router.post("/{vessel_code}" + route_settings.equipments, response_model=EquipmentRead, status_code= status.HTTP_201_CREATED)
async def create_equipment(vessel_code:str, equipment_create: EquipmentCreate, db = Depends( get_db)):
  bus = EquipmentBus(db)
  db_equipment = bus.create_equipment(vessel_code= vessel_code, equipment_create= equipment_create)
  if db_equipment is None:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vessel not found")
  else:
    return db_equipment

@router.patch("/{vessel_code}" + route_settings.equipments, response_model=EquipmentRead, status_code= status.HTTP_200_OK)
async def update_equipment(vessel_code:str, equipment_update: EquipmentUpdate, db = Depends( get_db)):
  bus = EquipmentBus(db)
  db_equipment = bus.update_equipment(vessel_code= vessel_code, equipment_update= equipment_update)
  if db_equipment is None:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vessel not found")
  else:
    return db_equipment

@router.delete("/{vessel_code}" + route_settings.equipments, response_model=EquipmentRead, status_code= status.HTTP_200_OK)
async def delete_vessel(vessel_code:str, eqps_delete_list: List[EquipmentDelete], db = Depends( get_db)):
  bus = EquipmentBus(db)
  db_equipment_list = bus.delete_equipment(vessel_code= vessel_code, eqps_delete_list= eqps_delete_list)
  if db_equipment_list is None:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vessel not found")
  else:
    return db_equipment_list