"""Base AI Dashboard class."""
from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass, field
import logging
import pathlib
from typing import TYPE_CHECKING, Any, Dict


from awesomeversion import AwesomeVersion
from aiohttp.client import ClientSession
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.loader import Integration

from .const import SetupStage, ConfigurationType, AIFacialDashboardDisabledReason
from .exceptions import AIDashboardExecutionStillInProgress

from .utils.queue_manager import QueueManager
from .utils.logger import get_hacs_logger

if TYPE_CHECKING: #Avoid circular imports
    from .tasks.manager import AIFacialDashboardTaskManager

@dataclass
class AIFacialDashboardConfiguration:
    """AI Facial Dashboard configuration class."""
    config: dict[str, Any] = field(default_factory=dict)
    config_entry: ConfigEntry | None = None
    config_type: ConfigurationType | None = None
    country: str = "ALL"
    debug: bool = False
    dev: bool = False
    experimental: bool = False
    frontend_compact: bool = False
    frontend_mode: str = "Grid"
    frontend_repo_url: str = "http://localhost:5000"
    frontend_repo: str = ""
    dev_mode: str = ""
    onboarding_done: bool = False
    sidepanel_icon: str = "mdi:face-recognition"
    sidepanel_title: str = "AI Dashboard"
    image_processing_entity = None

    def to_json(self) -> str:
        """Return a json string."""
        return asdict(self)

    def update_from_dict(self, data: dict) -> None:
        """Set attributes from dicts."""
        if not isinstance(data, dict):
            raise AIDashboardExecutionStillInProgress("Configuration is not valid.")

        for key in data:
            self.__setattr__(key, data[key])

@dataclass
class AIFacialDashboardStatus:
    """AI Facial Dashboard Status."""

    startup: bool = True
    new: bool = False
    reloading_data: bool = False
    upgrading_all: bool = False


@dataclass
class AIFacialDashboardCore:
    """AI Facial Dashboard Core info."""

    config_path: pathlib.Path | None = None
    ha_version: AwesomeVersion | None = None

@dataclass
class AIFacialDashboardSystem:
    """AI Facial Dashboard System info."""

    disabled_reason: AIFacialDashboardDisabledReason | None = None
    running: bool = False
    stage = SetupStage.SETUP
    action: bool = False

    @property
    def disabled(self) -> bool:
        """Return if AI Facial Dashboard is disabled."""
        return self.disabled_reason is not None



class AIFacialDashboardBase:
    """Base AI Facial Dashboard class."""

    configuration = AIFacialDashboardConfiguration()
    core = AIFacialDashboardCore()
    frontend_version: str | None = None
    hass: HomeAssistant | None = None
    integration: Integration | None = None
    log: logging.Logger = get_hacs_logger()
    queue: QueueManager | None = None
    recuring_tasks = []
    session: ClientSession | None = None
    stage: SetupStage | None = None
    status: AIFacialDashboardStatus = AIFacialDashboardStatus()
    system = AIFacialDashboardSystem()
    tasks: AIFacialDashboardTaskManager | None = None
    version: str | None = None
    adders = {}
    devices = {}
    config = {}

    @property
    def integration_dir(self) -> pathlib.Path:
        """Return the AI Facial Dashboard integration dir."""
        return self.integration.file_path

    async def async_set_stage(self, stage: SetupStage | None) -> None:
        """Set AI Facial Dashboard stage."""
        if stage and self.stage == stage:
            return

        self.stage = stage
        if stage is not None:
            self.log.info("Stage changed: %s", self.stage)
            # self.hass.bus.async_fire("hacs/stage", {"stage": self.stage})
            await self.tasks.async_execute_runtume_tasks()


    async def startup_tasks(self, _event=None) -> None:
        """Tasks that are started after setup."""
        await self.async_set_stage(SetupStage.STARTUP)
        self.status.startup = False

        self.hass.bus.async_fire("hacs/status", {})

        await self.async_set_stage(SetupStage.RUNNING)

        self.hass.bus.async_fire("hacs/reload", {"force": True})

        if queue_task := self.tasks.get("prosess_queue"):
            await queue_task.execute_task()

        self.hass.bus.async_fire("hacs/status", {})


    async def async_recreate_entities(self) -> None:
        """Recreate entities."""
        if (
            self.configuration == ConfigurationType.YAML
            or not self.core.ha_version >= "2022.4.0.dev0"
            or not self.configuration.experimental
        ):
            return

        platforms = ["update"]

        await self.hass.config_entries.async_unload_platforms(
            entry=self.configuration.config_entry,
            platforms=platforms,
        )

        self.hass.config_entries.async_setup_platforms(self.configuration.config_entry, platforms)



