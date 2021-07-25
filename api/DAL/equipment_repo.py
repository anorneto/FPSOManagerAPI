from typing import List
from sqlalchemy.orm import Session

from api.models.equipment_model import Equipment
from api.schemas.equipment_schema import EquipmentCreate,EquipmentRead,EquipmentUpdate,EquipmentDelete

class EquipmentRepo:
  def __init__(self, db: Session):
    self._db = db


  def create_equipment(self, vessel_id: int, equipment_create: EquipmentCreate) -> Equipment:
    db_new_equipment = Equipment( **equipment_create, vessel_id = vessel_id)
    self._db.add(db_new_equipment)
    self._db.commit()
    self._db.refresh(db_new_equipment)
    return db_new_equipment

  def update_equipment(self, vessel_id: int, equipment_update: EquipmentUpdate) -> Equipment:
    db_equipment = self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id, Equipment.code == equipment_update.code)
    db_equipment = equipment_update
    self._db.commit()
    self._db.refresh(db_equipment)
    return db_equipment

  def delete_equipment(self, vessel_id: int, eqps_delete_list: List[EquipmentDelete]) -> List[Equipment]:
    equipments_code_list = list( map( lambda eqp: eqp.code, eqps_delete_list))
    db_equipments_delete_list = self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id, Equipment.code.in_(equipments_code_list))

    for equipment in db_equipments_delete_list:
      equipment.is_active = False

    self._db.commit()
    self._db.refresh(db_equipments_delete_list)
    return db_equipments_delete_list