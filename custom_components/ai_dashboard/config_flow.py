"""Adds config flow for AI Facial Dashboard"""
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_PORT,
)

import voluptuous as vol

from .const import (
    DOMAIN, 
    CONF_DEV_MODE, 
    DEFAULT_API_RECOGNITION_KEY,
    DEFAULT_API_DETECTION_KEY,
    CONF_TIMEOUT,
    CONF_DETECT_ONLY,
    CONF_SAVE_FILE_FOLDER,
    CONF_SAVE_TIMESTAMPTED_FILE,
    CONF_SAVE_FACES_FOLDER,
    CONF_SAVE_FACES,
    CONF_SHOW_BOXES,
    CONF_MIN_CONFIDANCE,
    CONF_API_RECOGNITION_KEY,
    CONF_API_DETECTION_KEY,
    DEFAULT_TIMEOUT, 
    DEFAULT_IP_ADRESS, 
    DEFAULT_PORT,
    DEFAULT_SAVE_FILE_FOLDER,
    DEFAULT_SAVE_FACE_FOLDER,
    DEFAULT_MIN_CONFIDANCE
    )

import logging
_LOGGER = logging.getLogger(__name__)

class AIFacialDashboardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for AI Dashboard"""
    async def async_step_user(self, user_input = None):
        data = {}
        if user_input is not None: 
            data = user_input
            data[CONF_SAVE_TIMESTAMPTED_FILE] = True if data.get(CONF_SAVE_FILE_FOLDER) != "" else False
            data[CONF_SAVE_FACES] = True if (data.get(CONF_SAVE_FACES_FOLDER) != "") else False
            return self.async_create_entry(title="AI Dashboard", data=data)

        data_schema = {
            vol.Required(CONF_DEV_MODE): bool,
            vol.Required(CONF_IP_ADDRESS, default=DEFAULT_IP_ADRESS): str,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): str,
            vol.Required(CONF_API_RECOGNITION_KEY, default=DEFAULT_API_RECOGNITION_KEY): str,
            vol.Required(CONF_API_DETECTION_KEY, default=DEFAULT_API_DETECTION_KEY): str,
            vol.Required(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int, 
            vol.Required(CONF_MIN_CONFIDANCE, default= DEFAULT_MIN_CONFIDANCE): float,
            vol.Optional(CONF_DETECT_ONLY, default=False): bool,
            vol.Optional(CONF_SAVE_FILE_FOLDER, default=DEFAULT_SAVE_FILE_FOLDER): str,
            vol.Optional(CONF_SAVE_FACES_FOLDER, default=DEFAULT_SAVE_FACE_FOLDER): str,
            vol.Optional(CONF_SHOW_BOXES, default=True): bool,   
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(data_schema)
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return AIFacialDashboardOptionsFlowHandler(config_entry)

class AIFacialDashboardOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        current_config = self.config_entry.data
        data = {}
        if user_input is not None: 
            data = user_input
            data[CONF_SAVE_TIMESTAMPTED_FILE] = True if data.get(CONF_SAVE_FILE_FOLDER) != "" else False
            data[CONF_SAVE_FACES] = True if (data.get(CONF_SAVE_FACES_FOLDER) != "") else False
            return self.async_create_entry(title="", data=user_input)

        data_schema = {
            vol.Required(CONF_DEV_MODE): bool,
            vol.Required(CONF_IP_ADDRESS, default=DEFAULT_IP_ADRESS): str,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): str,
            vol.Required(CONF_API_RECOGNITION_KEY, default=DEFAULT_API_RECOGNITION_KEY): str,
            vol.Required(CONF_API_DETECTION_KEY, default=DEFAULT_API_DETECTION_KEY): str,
            vol.Required(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int, 
            vol.Required(CONF_MIN_CONFIDANCE, default= DEFAULT_MIN_CONFIDANCE): float,
            vol.Optional(CONF_DETECT_ONLY, default=False): bool,
            vol.Optional(CONF_SAVE_FILE_FOLDER, default=DEFAULT_SAVE_FILE_FOLDER): str,
            vol.Optional(CONF_SAVE_FACES_FOLDER, default=DEFAULT_SAVE_FACE_FOLDER): str,
            vol.Optional(CONF_SHOW_BOXES, default=True): bool,   
        }

        #Save faces folder and save file folder have to be a string. Delete if they are none before the configuration
        if data_schema[CONF_SAVE_FILE_FOLDER] == "": 
            del data_schema[CONF_SAVE_FILE_FOLDER]

        if data_schema[CONF_SAVE_FACES_FOLDER] == "": 
            del data_schema[CONF_SAVE_FACES_FOLDER]


        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(data_schema),
        )