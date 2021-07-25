from fastapi import APIRouter

from api.settings import RoutersSettings

router_settings = RoutersSettings()

router = APIRouter(prefix = router_settings.vessels_route)

@router.get("/equipments")
async def get_vessles():
  return "Vessels"

@router.post("/equipments")
async def add_vessel():
  return 'OK'