from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from api.dal.equipment_repo import EquipmentRepo
from api.dal.vessel_repo import VesselRepo

from api.schemas.equipment_schema import EquipmentCreate,EquipmentUpdate,EquipmentDelete

class EquipmentBus:
  def __init__(self, db: Session ):
    self._equipment_repo = EquipmentRepo(db = db)
    self._vessel_repo = VesselRepo( db = db)

  def get_equipments(self,vessel_code: str, filter_inactive: str = True):
    vessel = self._get_vessel(vessel_code= vessel_code)
    return self._equipment_repo.get_equipment(vessel_id= vessel.id, filter_inactive= filter_inactive)

  def create_equipment(self, vessel_code: str, equipment_create: EquipmentCreate):
    vessel = self._get_vessel(vessel_code)
    try:
      return self._equipment_repo.create_equipment(vessel_id= vessel.id, equipment_create= equipment_create)
    except IntegrityError:
      raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= "Equipment code already registered")

  def update_equipment(self, vessel_code: str, equipment_update: EquipmentUpdate):
    vessel = self._get_vessel(vessel_code)
    return self._equipment_repo.update_equipment(vessel_id= vessel.id, equipment_update= equipment_update)

  def delete_equipment(self, vessel_code: str, eqps_delete_list: List[EquipmentDelete]):
    vessel = self._get_vessel(vessel_code)
    return self._equipment_repo.delete_equipment(vessel_id= vessel.id, eqps_delete_list= eqps_delete_list)


  def _get_vessel(self,vessel_code: str):
    vessel =  self._vessel_repo.get_vessel_by_code(vessel_code = vessel_code)
    if vessel:
      return vessel
    else:
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vessel not found")