from typing import List
from fastapi import APIRouter,Depends,status
from fastapi.responses import Response

from api.settings import RouteSettings
from api.database import get_db
from api.bll.vessel_bus import VesselBus
from api.schemas.vessel_schema import VesselRead,VesselCreate

route_settings = RouteSettings()
router = APIRouter(prefix = route_settings.vessels)

@router.get("", response_model=List[VesselRead], status_code= status.HTTP_200_OK)
def get_all_vessels(filter_inactive: bool = True, db = Depends( get_db )):
  bus = VesselBus(db)
  return bus.get_vessels(filter_inactive)

@router.get("/{vessel_code}", response_model=VesselRead, status_code= status.HTTP_200_OK)
def get_vessel_by_code(vessel_code:str, db = Depends( get_db )):
  bus = VesselBus(db)
  db_vessel = bus.get_vessel_by_code(vessel_code)
  return db_vessel


@router.post("", response_model=VesselRead, status_code= status.HTTP_201_CREATED)
def create_vessel(vessel_create: VesselCreate, db = Depends( get_db )):
  bus = VesselBus(db)
  db_vessel = bus.create_vessel(vessel_create)
  return db_vessel

@router.patch("/{vessel_code}/deactivate", response_class=Response, status_code= status.HTTP_204_NO_CONTENT)
def deactivate_vessel(vessel_code: str, db = Depends( get_db )):
  bus = VesselBus(db)
  bus.deactivate_vessel(vessel_code)

@router.patch("/{vessel_code}/activate", response_class=Response, status_code= status.HTTP_204_NO_CONTENT)
def activate_vessel(vessel_code: str, db = Depends( get_db )):
  bus = VesselBus(db)
  bus.activate_vessel(vessel_code)
