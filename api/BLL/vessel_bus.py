from sqlalchemy.orm import Session

from api.dal.vessel_repo import VesselRepo
from api.schemas.vessel_schema import VesselCreate,VesselDelete

class VesselBus:
  def __init__(self, db: Session ):
    self._repo = VesselRepo(db = db)

  def get_vessels(self):
      return self._repo.get_vessels()

  def get_vessel_by_code(self, vessel_code: str):
      return self._repo.get_vessel_by_code(vessel_code = vessel_code)

  def create_vessel(self, vessel_create: VesselCreate):
    if self.get_vessel_by_code(vessel_create.code):
      return None
    else:
      return self._repo.create_vessel(vessel_create)

  def delete_vessel(self, vessel_delete: VesselDelete):
    vessel_delete = self.get_vessel_by_code(vessel_delete.code)
    if not vessel_delete:
      return None
    else:
      return self._repo.delete_vessel(vessel_delete)
