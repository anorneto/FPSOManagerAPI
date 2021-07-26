from typing import List

from pydantic import BaseModel

from .equipment_schema import EquipmentRead

class VesselBase(BaseModel):
  code: str

class VesselCreate(VesselBase):
  pass;

class VesselRead(VesselBase):
  id: int
  is_active: bool
  equipments: List[EquipmentRead] = []

  class Config:
    orm_mode = True