""""Starting setup task: Image processing platform."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform

from ..base import AIFacialDashboardBase
from ..const import DOMAIN, SetupStage
from .base import AIFacialDashboardTask

from homeassistant.components.image_processing import (
 DOMAIN as IMAGE_PROCESSING_DOMAIN
)

import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_task(hacs: AIFacialDashboardBase, hass: HomeAssistant) -> Task:
    """Set up this task."""
    return Task(hacs=hacs, hass=hass)


class Task(AIFacialDashboardTask):
    """Setup the Ai Dashboard image_processing platform."""

    stages = [SetupStage.SETUP]

    async def async_execute(self) -> None:
        """Execute the task."""
        #There does not seem to be a way to setup platforms of image_processing entities through config flow, hence use async_load_platforms as a workaround
        self.hass.async_create_task(
            async_load_platform(
                self.hass, 
                IMAGE_PROCESSING_DOMAIN, 
                DOMAIN, 
                {}, 
                {"ai_dashboard": None} # this dictionary is used to pass an assert in the core code
            )
        )