"""Tests setup async_initialize_integration in the AI dashboard"""
import json
import pytest

from pytest_homeassistant_custom_component.common import MockConfigEntry, load_fixture

from custom_components.ai_dashboard.const import DOMAIN
from custom_components.ai_dashboard.base import AIFacialDashboardBase
from custom_components.ai_dashboard import async_initialize_integration

FIXTURES_TEST = json.loads(load_fixture("config_flow_fixture.json"))

@pytest.mark.asyncio
async def test_async_setup_entry(hass): 
    """Test async_setup_entry"""
  

    #Load config flow data
    fixture_test = FIXTURES_TEST["default"]["config_flow_data"]

    # Create a mock entry so we don't have to go through config flow
    config_entry = MockConfigEntry(domain=DOMAIN, data = fixture_test, entry_id="setup_test")

    #Run tests
    assert await async_initialize_integration(hass, config_entry=config_entry)

    assert DOMAIN in hass.data and type(hass.data[DOMAIN]) == AIFacialDashboardBase