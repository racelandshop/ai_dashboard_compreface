"""HACS Base entities."""
from __future__ import annotations

from homeassistant.core import Event, callback
from homeassistant.helpers.entity import Entity

from .base import AIFacialDashboardBase
from .const import DOMAIN


HACS_SYSTEM_ID = "0717a0cd-745c-48fd-9b16-c8534c9704f9-bc944b0f-fd42-4a58-a072-ade38d1444cd"
NAME_SHORT = "HACS"


def system_info(hacs: AIFacialDashboardBase) -> dict:
    """Return system info."""
    info = {
        "identifiers": {(DOMAIN, HACS_SYSTEM_ID)},
        "name": NAME_SHORT,
        "manufacturer": "hacs.xyz",
        "model": "",
        "sw_version": str(hacs.version),
        "configuration_url": "homeassistant://hacs",
    }
    # LEGACY can be removed when min HA version is 2021.12
    if hacs.core.ha_version >= "2021.12.0b0":
        # pylint: disable=import-outside-toplevel
        from homeassistant.helpers.device_registry import DeviceEntryType

        info["entry_type"] = DeviceEntryType.SERVICE
    else:
        info["entry_type"] = "service"
    return info


class BaseEntity(Entity):
    """Base entity."""

    _attr_should_poll = False

    def __init__(self, hacs: AIFacialDashboardBase) -> None:
        """Initialize."""
        self.hacs = hacs

    async def async_added_to_hass(self) -> None:
        """Register for status events."""
        self.async_on_remove(
            self.hass.bus.async_listen(
                event_type="hacs/repository",
                event_filter=self._filter_events,
                listener=self._update_and_write_state,
            )
        )

    @callback
    def _update(self) -> None:
        """Update the sensor."""

    async def async_update(self) -> None:
        """Manual updates of the sensor."""
        self._update()

    @callback
    def _filter_events(self, event: Event) -> bool:
        """Filter the events."""
        if self.repository is None:
            # System entities
            return True
        return event.data.get("repository_id") == self.repository.data.id

    @callback
    def _update_and_write_state(self, *_) -> None:
        """Update the entity and write state."""
        self._update()
        self.async_write_ha_state()


class HacsSystemEntity(BaseEntity):
    """Base system entity."""

    _attr_icon = "hacs:hacs"
    _attr_unique_id = HACS_SYSTEM_ID

    @property
    def device_info(self) -> dict[str, any]:
        """Return device information about HACS."""
        return system_info(self.hacs)

