from typing import List, Union

import pytest
from faker import Faker

from api.schemas.vessel_schema import VesselCreate
from api.schemas.equipment_schema import EquipmentCreate, EquipmentUpdate, EquipmentRead, EquipmentDelete
# Fixtures
fake = Faker()

@pytest.fixture(scope="function")
def vessel_random() -> VesselCreate:
    return {
        "code": fake.pystr(min_chars=5, max_chars=8)
    }

@pytest.fixture(scope="session")
def vessel_fixed() -> VesselCreate:
    return {
        "code": fake.pystr(min_chars=5, max_chars=8)
    }


@pytest.fixture(scope="function")
def equipment_create_update_random() -> Union[EquipmentCreate,EquipmentUpdate]:
    return {
        "code": fake.pystr(min_chars=5, max_chars=8),
        "location": fake.country(),
        "name": "FakeName"
    }

@pytest.fixture(scope="session")
def equipment_create_update_fixed() -> Union[EquipmentCreate,EquipmentUpdate]:
    return {
        "code": fake.pystr(min_chars=5, max_chars=8),
        "location": fake.country(),
        "name": "FakeName"
    }
