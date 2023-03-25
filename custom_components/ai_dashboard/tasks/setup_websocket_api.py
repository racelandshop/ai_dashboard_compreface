"""Register WS API endpoints for HACS."""
from __future__ import annotations
import logging

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.helpers import entity_registry as er

from homeassistant.components.websocket_api import (
    async_register_command,
)

from .base import AIFacialDashboardTask
from ..const import DOMAIN, SetupStage
from ..exceptions import NoUsablePhotoException


_LOGGER = logging.getLogger(__name__)

async def async_setup_task(hacs: AIFacialDashboardTask, hass: HomeAssistant) -> Task:
    """Set up this task."""
    return Task(hacs=hacs, hass=hass)


class Task(AIFacialDashboardTask):
    """Setup the HACS websocket API."""

    stages = [SetupStage.SETUP]

    async def async_execute(self) -> None:
        """Execute the task."""
        async_register_command(self.hass, send_camera_database_to_frontend)
        async_register_command(self.hass, teach_face)
        async_register_command(self.hass, delete_face)

       

@websocket_api.websocket_command(
    {
        vol.Required("type"): "raceland_ai_dashboard/get_face_list",
    }
        
)
@websocket_api.require_admin
@websocket_api.async_response
async def send_camera_database_to_frontend(hass, connection, msg):
    image_processing_entity = hass.data[DOMAIN].image_processing_entity
    result = await hass.async_add_executor_job(image_processing_entity.get_stored_faces)
    if result: 
        list_of_faces = image_processing_entity.registered_faces
        connection.send_message(websocket_api.result_message(msg["id"], list_of_faces))
    else: 
        connection.send_message(websocket_api.result_message(msg["id"], "compreface error"))

@websocket_api.websocket_command(
    {
        vol.Required("type"): "raceland_ai_dashboard/teach_face",
        vol.Required("name"): cv.string,
        vol.Required("url"): cv.ensure_list
    }
        
)
@websocket_api.require_admin
@websocket_api.async_response
async def teach_face(hass, connection, msg):
    name = msg["name"]
    url_list = msg["url"]
    image_processing_entity = hass.data[DOMAIN].image_processing_entity
    try: 
        await hass.async_add_executor_job(image_processing_entity.teach, name, url_list)
        connection.send_message(websocket_api.result_message(msg["id"], result = True))
    except NoUsablePhotoException:
        connection.send_message(websocket_api.result_message(msg["id"], result = False))

@websocket_api.websocket_command(
    {
        vol.Required("type"): "raceland_ai_dashboard/delete_face",
        vol.Required("name"): cv.string
    }
        
)
@websocket_api.require_admin
@websocket_api.async_response
async def delete_face(hass, connection, msg):
    face_name = msg["name"]
    image_processing_entity = hass.data[DOMAIN].image_processing_entity
    await hass.async_add_executor_job(image_processing_entity.delete_stored_faces, face_name)
    connection.send_message(websocket_api.result_message(msg["id"], result = True))
