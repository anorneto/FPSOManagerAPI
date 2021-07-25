from fastapi import APIRouter

from api.settings import RouteSettings

route_settings = RouteSettings()

router = APIRouter(prefix = route_settings.equipments)

@router.get("/equipments")
async def get_vessles():
  return "Vessels"

@router.post("/equipments")
async def add_vessel():
  return 'OK'