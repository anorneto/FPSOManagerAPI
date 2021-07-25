from typing import List
from fastapi import APIRouter,Depends,status,HTTPException

from api.settings import RouteSettings
from api.database import get_db
from api.bll.vessel_bus import VesselBus
from api.schemas.vessel_schema import VesselRead,VesselCreate,VesselDelete

route_settings = RouteSettings()
router = APIRouter(prefix = route_settings.vessels)

@router.get("/", response_model=List[VesselRead], status_code= status.HTTP_200_OK)
def get_vessels( db = Depends( get_db )):
  bus = VesselBus(db)
  return bus.get_vessels()

@router.get("/{vessel_code}", response_model=VesselRead, status_code= status.HTTP_200_OK)
def get_vessel_by_code(vessel_code:str, db = Depends( get_db )):
  bus = VesselBus(db)
  db_vessel = bus.get_vessel_by_code(vessel_code)
  if db_vessel is None:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vessel not Found")
  else:
    return db_vessel


@router.post("/", response_model=VesselRead, status_code= status.HTTP_201_CREATED)
def create_vessel(vessel_create: VesselCreate, db = Depends( get_db )):
  bus = VesselBus(db)
  db_vessel = bus.create_vessel(vessel_create)
  if db_vessel is None:
    raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Vessel already registered")
  else:
    return db_vessel

@router.delete("/", response_model=VesselRead, status_code= status.HTTP_200_OK)
def delete_vessel(vessel_delete: VesselDelete, db = Depends( get_db )):
  bus = VesselBus(db)
  db_vessel = bus.delete_vessel(vessel_delete)
  if db_vessel is None:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vessel not Found")
  else:
    return db_vessel