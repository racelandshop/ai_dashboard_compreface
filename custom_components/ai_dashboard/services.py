"""Setup for the image processing services used in the AI dashboard"""

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import entity_platform
import homeassistant.helpers.config_validation as cv

import voluptuous as vol
import logging

from .const import (
    URL, 
    SERVICE_SCAN,
    CAMERA_SCAN_ENTITY_ID
)

_LOGGER = logging.getLogger(__name__)

SERVICE_SCAN_SCHEMA = {
        vol.Required(CAMERA_SCAN_ENTITY_ID): cv.string,
    }


async def setup_services(hass):
    platform = entity_platform.async_get_current_platform()

    platform.async_register_entity_service(
        SERVICE_SCAN, 
        SERVICE_SCAN_SCHEMA, 
        "async_process_image"
    )