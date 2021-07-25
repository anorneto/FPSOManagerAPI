from sqlalchemy.orm import Session

from api.dal.vessel_repo import VesselRepo
from api.schemas.vessel_schema import VesselCreate,VesselDelete

from fastapi import status,HTTPException

class VesselBus:
  def __init__(self, db: Session ):
    self._repo = VesselRepo(db = db)

  def get_vessels(self):
    return self._repo.get_vessels()

  def get_vessel_by_code(self, vessel_code: str):
    vessel = self._repo.get_vessel_by_code(vessel_code = vessel_code)
    if vessel:
      return vessel
    else:
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vessel not Found")

  def create_vessel(self, vessel_create: VesselCreate):
    vessel = self.get_vessel_by_code(vessel_create.code)
    if vessel:
      raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Vessel already registered")
    else:
      return self._repo.create_vessel(vessel_create)

  def delete_vessel(self, vessel_delete: VesselDelete):
    vessel = self.get_vessel_by_code(vessel_delete.code)
    if vessel:
      return self._repo.delete_vessel(vessel_delete)
    else:
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vessel not Found")
