import asyncio
import uvicorn

from fastapi import FastAPI
from api.settings import ApiSettings
from api.routers import vessel_route,equipment_route


api_settings = ApiSettings()

api = FastAPI(title= api_settings.api_name,
              description= api_settings.api_description,
              version= api_settings.api_version,
              )

api.include_router(vessel_route.router)
api.include_router(equipment_route.router)

def main():
    uvicorn.run(api, host="0.0.0.0", port = api_settings.api_port)


if __name__ == "__main__":
    main()