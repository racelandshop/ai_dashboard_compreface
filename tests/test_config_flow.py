"""Test the dashboard AI config flow."""
import json
import pytest

from pytest_homeassistant_custom_component.common import load_fixture

from unittest.mock import patch

from homeassistant import config_entries, data_entry_flow

from custom_components.ai_dashboard.const import (
    DOMAIN,
)


PATCH_SETUP_ENTRY = patch(
    "custom_components.ai_dashboard.async_setup_entry",
    return_value=True,
)

FIXTURES_TEST = json.loads(load_fixture("config_flow_fixture.json"))

# This fixture bypasses the actual setup of the integration
# since we only want to test the config flow. We test the
# actual functionality of the integration in other test modules.
# Based on (https://github.com/mathias-jakobsen/ha-mj-dashboard/t)
@pytest.fixture(autouse=True, name="bypass_setup_fixture")
def bypass_setup_fixture():
    """Prevent setup."""
    with patch(
        "custom_components.ai_dashboard.async_setup_entry",
        return_value=True,
    ):
        yield


@pytest.mark.asyncio
async def test_form(hass, bypass_setup_fixture):
    """Test a successful config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM

    with PATCH_SETUP_ENTRY as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=FIXTURES_TEST["default"]["user_data"]
        )
        await hass.async_block_till_done()

    assert result2["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result2["title"] == "AI Dashboard"
    assert result2["data"] == FIXTURES_TEST["default"]["config_flow_data"]

    assert len(mock_setup_entry.mock_calls) == 1

@pytest.mark.asyncio
async def test_form_no_save_folder(hass, bypass_setup_fixture):
    """Test a successful config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM

    with PATCH_SETUP_ENTRY as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=FIXTURES_TEST["no_save_folder"]["user_data"]
        )
        await hass.async_block_till_done()

    assert result2["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result2["title"] == "AI Dashboard"
    assert result2["data"] == FIXTURES_TEST["no_save_folder"]["config_flow_data"]

    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.asyncio
async def test_form_save_folder(hass, bypass_setup_fixture):
    """Test a successful config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM

    with PATCH_SETUP_ENTRY as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=FIXTURES_TEST["save_folder"]["user_data"]
        )
        await hass.async_block_till_done()

    assert result2["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result2["title"] == "AI Dashboard"
    assert result2["data"] == FIXTURES_TEST["save_folder"]["config_flow_data"]

    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.asyncio
async def test_default_values(hass, bypass_setup_fixture):
    """Test a successful config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM

    with PATCH_SETUP_ENTRY as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=FIXTURES_TEST["default_values"]["user_data"]
        )
        await hass.async_block_till_done()

    assert result2["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result2["title"] == "AI Dashboard"
    assert result2["data"] == FIXTURES_TEST["default_values"]["config_flow_data"]

    assert len(mock_setup_entry.mock_calls) == 1
