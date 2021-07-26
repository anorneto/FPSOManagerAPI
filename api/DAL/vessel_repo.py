from typing import List
from sqlalchemy.orm import Session

from api.models.vessel_model import Vessel
from api.schemas.vessel_schema import VesselCreate,VesselDelete

class VesselRepo:
  def __init__(self, db: Session):
    self._db = db


  def get_vessels(self, filter_inactive: bool = True) -> List[Vessel]:
    if filter_inactive:
      return self._db.query(Vessel).filter(Vessel.is_active == True).all()
    else:
      return self._db.query(Vessel).all()

  def get_vessel_by_code(self, vessel_code: str) -> Vessel:
    return self._db.query(Vessel).filter(Vessel.code == vessel_code).one_or_none()

  def create_vessel(self, vessel_create: VesselCreate) -> Vessel:
    db_new_vessel = Vessel(code = vessel_create.code)
    self._db.add(db_new_vessel)
    self._db.commit()
    self._db.refresh(db_new_vessel)
    return db_new_vessel


  def update_vessel_active_status(self, vessel_id: int, active_status: bool) -> None:
    db_delete_vessel = self._db.query(Vessel).filter_by(id = vessel_id).first()
    db_delete_vessel.is_active = active_status
    self._db.commit()
    return