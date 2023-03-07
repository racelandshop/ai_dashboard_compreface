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
    CONF_API_KEY,
    CONF_TIMEOUT,
    CONF_DETECT_ONLY,
    CONF_SAVE_FILE_FOLDER,
    CONF_SAVE_TIMESTAMPTED_FILE,
    CONF_SAVE_FACES_FOLDER,
    CONF_SAVE_FACES,
    CONF_SHOW_BOXES,
    DEFAULT_API_KEY,
    DEFAULT_TIMEOUT, 
    DEFAULT_IP_ADRESS, 
    DEFAULT_PORT,
    DEFAULT_SAVE_FILE_FOLDER,
    DEFAULT_SAVE_FACE_FOLDER
)

import logging
_LOGGER = logging.getLogger(__name__)

class AIFacialDashboardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for AI Dashboard"""
    async def async_step_user(self, user_input = None):
        data = {}
        if user_input != None: 
            data = user_input
            
            data[CONF_SAVE_TIMESTAMPTED_FILE] = True if data.get(CONF_SAVE_FILE_FOLDER) != "" else False
            data[CONF_SAVE_FACES] = True if (data.get(CONF_SAVE_FACES_FOLDER) != "") else False
        
        if user_input is not None:
            return self.async_create_entry(title="AI Dashboard", data=data)

        data_schema = {
            vol.Required(CONF_DEV_MODE): bool,
            vol.Required(CONF_IP_ADDRESS, default=DEFAULT_IP_ADRESS): str,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): str,
            vol.Optional(CONF_API_KEY, default=DEFAULT_API_KEY): str,
            vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): str, 
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
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = {
            vol.Required(CONF_DEV_MODE, default=current_config.get(CONF_DEV_MODE, CONF_DEV_MODE)): bool,
            vol.Required(CONF_IP_ADDRESS, default=current_config.get(CONF_IP_ADDRESS, CONF_IP_ADDRESS)): str,
            vol.Required(CONF_PORT, default=current_config.get(CONF_PORT, CONF_PORT)): str,
            vol.Optional(CONF_API_KEY, default=current_config.get(CONF_API_KEY, DEFAULT_API_KEY)): str,
            vol.Optional(CONF_TIMEOUT, default=current_config.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)): str, 
            vol.Optional(CONF_DETECT_ONLY, default=current_config.get(CONF_DETECT_ONLY, False)): bool,
            vol.Optional(CONF_SAVE_FILE_FOLDER, default=current_config.get(CONF_SAVE_FILE_FOLDER, "")): str,
            vol.Optional(CONF_SAVE_FACES_FOLDER, default=current_config.get(CONF_SAVE_FACES_FOLDER, "")): str,
            vol.Optional(CONF_SHOW_BOXES, default=current_config.get(CONF_SHOW_BOXES, True)): bool,
        }

        #Save faces folder and save file folder have to be a string. Delete if they are none before the configuration
        if data_schema[CONF_SAVE_FILE_FOLDER] == "": 
            del data_schema[CONF_SAVE_FILE_FOLDER]

        if data_schema[CONF_SAVE_FACES_FOLDER] == "": 
            del data_schema[CONF_SAVE_FACES_FOLDER]


        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(data_schema),
        )