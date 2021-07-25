from pydantic import BaseSettings
from fastapi import HTTPException, status

class ApiSettings(BaseSettings):
  api_name : str = "FPSOManagerAPI"
  api_description: str = "Python backend to manage different equipment of an FPSO."
  api_version: str = "1.0.0"
  api_port: int = 8000



class RouteSettings():
  vessels: str = "/vessels"
  equipments: str = "/equipments"