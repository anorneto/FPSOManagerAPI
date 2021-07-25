from typing import List
from sqlalchemy.orm import Session

from api.dal.equipment_repo import EquipmentRepo
from api.dal.vessel_repo import VesselRepo

from api.schemas.equipment_schema import EquipmentCreate,EquipmentUpdate,EquipmentDelete

class EquipmentBus:
  def __init__(self, db: Session ):
    self._equipment_repo = EquipmentRepo(db = db)
    self._vessel_repo = VesselRepo( db = db)

  def create_equipment(self, vessel_code: str, equipment_create: EquipmentCreate):
    vessel = self._get_vessel(vessel_code)
    if vessel:
      return self._equipment_repo.create_equipment(vessel_id= vessel.id, equipment_create= equipment_create)
    else:
      return None

  def update_equipment(self, vessel_code: str, equipment_update: EquipmentUpdate):
    vessel = self._get_vessel(vessel_code)
    if vessel:
      return self._equipment_repo.update_equipment(vessel_id= vessel.id, equipment_update= equipment_update)
    else:
      return None

  def delete_equipment(self, vessel_code: str, eqps_delete_list: List[EquipmentDelete]):
    vessel = self._get_vessel(vessel_code)
    if vessel:
      return self._equipment_repo.delete_equipment(vessel_id= vessel.id, eqps_delete_list= eqps_delete_list)
    else:
      return None


  def _get_vessel(self,vessel_code: str):
    vessel =  self._vessel_repo.get_vessel_by_code(vessel_code = vessel_code)
    return vessel