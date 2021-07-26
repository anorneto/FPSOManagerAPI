from typing import List

from pydantic import BaseModel, validator

from .equipment_schema import EquipmentRead

class VesselBase(BaseModel):
  code: str

class VesselCreate(VesselBase):
  @validator("code", pre=True, always=True)
  def check_code(cls,code_string):
    assert bool(code_string and not code_string.isspace()), "Vessel Code cannot be empty."
    return code_string.strip()

  pass;

class VesselRead(VesselBase):
  id: int
  is_active: bool
  equipments: List[EquipmentRead] = []

  class Config:
    orm_mode = True