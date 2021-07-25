from pydantic import BaseModel

class EquipmentBase(BaseModel):
  code: str

class EquipmentCreate(EquipmentBase):
  name: str
  location: str

class EquipmentUpdate(EquipmentBase):
  name: str
  location: str

class EquipmentDelete(EquipmentBase):
  pass

class EquipmentRead(EquipmentBase):
  name: str
  location: str
  is_active: bool

  class Config:
    orm_mode = True