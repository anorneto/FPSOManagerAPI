from datetime import datetime
from typing import List

from fastapi.testclient import TestClient
from fastapi import status

import pytest
from faker import Faker

from main import api
from api.schemas.vessel_schema import VesselCreate, VesselDelete, VesselRead
from api.settings import RouteSettings

# Setup
vessel_route = RouteSettings().vessels
client = TestClient(api)

# Fixtures
fake = Faker()

@pytest.fixture(scope="function")
def vessel_code_random() -> VesselCreate:
    return {
        "code": fake.pystr(min_chars=5, max_chars=8)
    }

@pytest.fixture(scope="session")
def vessel_code_fixed() -> VesselCreate:
    return {
        "code": fake.pystr(min_chars=5, max_chars=8)
    }

# Helpers

def post_vessel(vessel: VesselCreate):
    print(vessel)
    response = client.post(
        vessel_route,
        json= {'code': 'yiRUKb'}
    )
    return response

# Test Cases


""" def test_post_created_vessel(vessel_code_fixed: VesselCreate):
    response = post_vessel(vessel_code_fixed)
    print(vessel_route)
    print(response)
    assert response.status_code == 201
    assert response.json() == vessel_code_fixed """

def test_post_conflict_vessel(vessel_code_fixed: VesselCreate):
  response = post_vessel(vessel_code_fixed)
  assert response.status_code == 409
  assert response.json().detail == "Vessel already registered"

def test_get_all_vessels():
    response = client.get(vessel_route)
    assert response.status_code == status.HTTP_200_OK
