from typing import List
from sqlalchemy.orm import Session

from api.models.equipment_model import Equipment
from api.schemas.equipment_schema import EquipmentCreate,EquipmentRead,EquipmentUpdate,EquipmentActiveStatus

class EquipmentRepo:
  def __init__(self, db: Session):
    self._db = db

  def get_equipment(self,vessel_id: int, filter_inactive: bool = True) -> List[Equipment]:
    if filter_inactive:
      return self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id, Equipment.is_active == True).all()
    else:
      return self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id).all()

  def create_equipment(self, vessel_id: int, equipment_create: EquipmentCreate) -> Equipment:
    db_new_equipment = Equipment( **equipment_create.dict(), vessel_id = vessel_id)
    self._db.add(db_new_equipment)
    self._db.commit()
    self._db.refresh(db_new_equipment)
    return db_new_equipment

  def update_equipment(self, vessel_id: int, equipment_update: EquipmentUpdate) -> Equipment:
    db_equipment = self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id, Equipment.code == equipment_update.code).first()

    db_equipment.name = equipment_update.name
    db_equipment.location = equipment_update.location

    self._db.commit()
    self._db.refresh(db_equipment)
    return db_equipment

  def update_equipment_status(self, vessel_id: int, eqps_update_status_list: List[EquipmentActiveStatus], active_status: bool) -> None:
    equipments_code_list = list( map( lambda eqp: eqp.code, eqps_update_status_list))
    db_equipments_delete_list = self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id, Equipment.code.in_(equipments_code_list)).all()

    for equipment in db_equipments_delete_list:
      equipment.is_active = active_status

    self._db.commit()
    return