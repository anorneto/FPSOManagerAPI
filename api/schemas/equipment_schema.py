from pydantic import BaseModel, validator

class EquipmentBase(BaseModel):
  code: str

  @validator("code", pre=True, always=True)
  def check_code(cls,code_string):
    assert bool(code_string and not code_string.isspace()), "Equipment Code cannot be empty"
    return code_string.strip()

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

  class Config:
    orm_mode = True