from typing import List, Optional

from pydantic import BaseModel

from .equipment_model import Equipment

class VesselBase(BaseModel):
  code: str

class VesselCreate(VesselBase):
  pass;

class VesselDelete(VesselBase):
  pass;

class Vessel(VesselBase):
  id: int
  equipments: List[Equipment] = []

  class Config:
    orm_mode = True