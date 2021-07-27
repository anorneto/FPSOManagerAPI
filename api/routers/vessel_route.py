from typing import List
from fastapi import APIRouter,Depends,status
from fastapi.responses import Response

from api.settings import RouteSettings
from api.database import get_db
from api.bll.vessel_bus import VesselBus
from api.schemas.vessel_schema import VesselRead,VesselCreate

route_settings = RouteSettings()
router = APIRouter(prefix = route_settings.vessels)

@router.get(
  "",
  response_model=List[VesselRead],
  status_code= status.HTTP_200_OK,
  tags=["Vessels"],
  summary="Get all vessels",
  description="Return all vessels and its active equipments",
  responses={
    200: {"model": List[VesselRead], "description": "List of vessels and its active equipments"}
  }
)
def get_all_vessels( db = Depends( get_db )):
  bus = VesselBus(db)
  return bus.get_vessels()

@router.get(
  "/{vessel_code}",
  tags=["Vessels"],
  response_model=VesselRead,
  status_code= status.HTTP_200_OK,
  summary="Get vessel by code",
  description="Return vessel with given code and its active equipments",
  responses={
    200 : {"model": VesselRead, "description": "The vessel requested by code"},
    404:  {"description": "Vessel not Found", "content":{ "application/json": { "example": {"detail": "Vessel not found"} } }}
  }
)
def get_vessel_by_code(vessel_code:str, db = Depends( get_db )):
  bus = VesselBus(db)
  db_vessel = bus.get_vessel_by_code(vessel_code)
  return db_vessel


@router.post(
  "",
  tags=["Vessels"],
  response_model=VesselRead,
  status_code= status.HTTP_201_CREATED,
  summary="Create a vessel",
  description="Create a vessel with given code and returns it",
  responses={
    201: {"model": VesselRead, "description": "The vessel created"},
    409: {"description": "Vessel already registered", "content":{ "application/json": { "example": {"detail": "Vessel already registered"} } }}
  }
)
def create_vessel(vessel_create: VesselCreate, db = Depends( get_db )):
  bus = VesselBus(db)
  db_vessel = bus.create_vessel(vessel_create)
  return db_vessel
