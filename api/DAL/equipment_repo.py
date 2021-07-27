from typing import List
from sqlalchemy.orm import Session
import datetime

from api.models.equipment_model import Equipment
from api.schemas.equipment_schema import EquipmentCreate,EquipmentRead,EquipmentUpdate,EquipmentDelete

class EquipmentRepo:
  def __init__(self, db: Session):
    self._db = db

  def get_single_equipment(self,vessel_id: int, equipment_code: str) -> EquipmentRead:
    db_equipment = self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id, Equipment.code == equipment_code).first()
    return db_equipment

  def get_equipments(self,vessel_id: int) -> List[EquipmentRead]:
    return self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id, Equipment.is_active == True).all()

  def create_equipment(self, vessel_id: int, equipment_create: EquipmentCreate) -> EquipmentRead:
    db_new_equipment = Equipment( **equipment_create.dict(), vessel_id = vessel_id)
    self._db.add(db_new_equipment)
    self._db.commit()
    self._db.refresh(db_new_equipment)
    return db_new_equipment

  def update_equipment(self, vessel_id: int, equipment_update: EquipmentUpdate) -> EquipmentRead:
    db_equipment = self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id, Equipment.code == equipment_update.code, Equipment.is_active == True).first()

    db_equipment.name = equipment_update.name
    db_equipment.location = equipment_update.location
    db_equipment.update_date = datetime.datetime.now()

    self._db.commit()
    self._db.refresh(db_equipment)
    return db_equipment

  def delete_equipments(self, vessel_id: int, eqps_delete_list: List[EquipmentDelete]) -> None:
    equipments_code_list = list( map( lambda eqp: eqp.code, eqps_delete_list))
    db_equipments_delete_list = self._db.query(Equipment).filter(Equipment.vessel_id == vessel_id, Equipment.code.in_(equipments_code_list), Equipment.is_active == True).all()

    for equipment in db_equipments_delete_list:
      equipment.is_active = False
      equipment.delete_date = datetime.datetime.now()

    self._db.commit()
    return