"""Test the normal start of the dashboard AI image processing entity"""
import json
import pytest

from unittest.mock import PropertyMock, patch


from homeassistant.components.image_processing import DOMAIN as SENSOR_DOMAIN
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.setup import async_setup_component

from pytest_homeassistant_custom_component.common import (
    mock_device_registry,
    mock_registry,
    load_fixture
)


from . import (
    create_image_processing_entity
)

FIXTURES_TEST = json.loads(load_fixture("config_flow_fixture.json"))

@pytest.mark.asyncio
async def test_image_processing(hass):
    fixture_test = FIXTURES_TEST["default"]["config_flow_data"]#Continue from here
