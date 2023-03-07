"""
AI facial dashboard gives you a powerfull integration that allows the user to manage facial recognition data
"""
from __future__ import annotations

from awesomeversion import AwesomeVersion
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, __version__ as HAVERSION
from homeassistant.core import CoreState, HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_call_later
from homeassistant.loader import async_get_integration
from homeassistant.helpers import entity_registry as er

import voluptuous as vol

from .base import AIFacialDashboardBase
from .const import DOMAIN, ConfigurationType, AIFacialDashboardDisabledReason, SetupStage
from .tasks.manager import AIFacialDashboardTaskManager
from .utils.configuration_schema import ai_facial_dashboard_config
from .utils.queue_manager import QueueManager

CONFIG_SCHEMA = vol.Schema({DOMAIN: ai_facial_dashboard_config()}, extra=vol.ALLOW_EXTRA)

async def async_initialize_integration(
    hass: HomeAssistant,
    *,
    config_entry: ConfigEntry | None = None,
) -> bool:
    """Initialize the integration"""
    if config_entry.options != {}:
        config_entry.data = config_entry.options
        
    if hass.data.get(DOMAIN) == None: 
        hass.data[DOMAIN] = ai_facial_base = AIFacialDashboardBase()
    else: 
        ai_facial_base = hass.data[DOMAIN]

    ai_facial_base.configuration.update_from_dict(
        {
            "config_entry": config_entry,
            "config_type": ConfigurationType.CONFIG_ENTRY,
            **config_entry.data,
            **config_entry.options,
        }
    )

    integration = await async_get_integration(hass, DOMAIN)

    await ai_facial_base.async_set_stage(None)

    ai_facial_base.integration = integration
    ai_facial_base.version = integration.version
    ai_facial_base.configuration.dev = integration.version == "0.0.0"
    ai_facial_base.hass = hass
    ai_facial_base.queue = QueueManager(hass=hass) 
    ai_facial_base.system.running = True
    ai_facial_base.tasks = AIFacialDashboardTaskManager(hacs=ai_facial_base, hass=hass)
    ai_facial_base.session = async_get_clientsession(hass)

    ai_facial_base.log.debug("Configuration type: %s", ai_facial_base.configuration.config_type)
    ai_facial_base.core.config_path = ai_facial_base.hass.config.path()

    if ai_facial_base.core.ha_version is None:
        ai_facial_base.core.ha_version = AwesomeVersion(HAVERSION)

    await ai_facial_base.tasks.async_load()


    async def async_startup():
        """AI Dashboard startup tasks."""

        await ai_facial_base.async_set_stage(SetupStage.SETUP)
        if ai_facial_base.system.disabled:
            return False

        # Setup startup tasks
        if ai_facial_base.hass.state == CoreState.running:
            async_call_later(ai_facial_base.hass, 5, ai_facial_base.startup_tasks)
        else:
            ai_facial_base.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, ai_facial_base.startup_tasks)

        await ai_facial_base.async_set_stage(SetupStage.WAITING)
        ai_facial_base.log.info("Setup complete, waiting for Home Assistant before startup tasks starts")

        return not ai_facial_base.system.disabled

    await async_startup()

    # Mischief managed!
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    config_entry.async_on_unload(config_entry.add_update_listener(async_reload_entry))
    return await async_initialize_integration(hass=hass, config_entry=config_entry)

   

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    ai_facial_base: AIFacialDashboardBase = hass.data[DOMAIN]

    # Clear out pending queue
    ai_facial_base.queue.clear()

    for task in ai_facial_base.recuring_tasks:
        # Cancel all pending tasks
        task()

    try:
        if hass.data.get("frontend_panels", {}).get("ai_dashboard"):
            hass.components.frontend.async_remove_panel("ai_dashboard")
    except AttributeError:
        pass

    platforms = ["image_processing"]
    
    unload_ok = await hass.config_entries.async_unload_platforms(config_entry, platforms) #Unload_ok returns False. It is supposed to return True (?)
    
    image_processing_entity = hass.data[DOMAIN].image_processing_entity
    entity_registry = er.async_get(hass)
    hass.data[DOMAIN]
    entity_registry.async_remove(image_processing_entity.entity_id) 

    await ai_facial_base.async_set_stage(None)
    hass.data.pop(DOMAIN, None)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload the AI Facial Dashboard config entry."""
    await async_unload_entry(hass, config_entry)
    await async_initialize_integration(hass=hass, config_entry=config_entry)
