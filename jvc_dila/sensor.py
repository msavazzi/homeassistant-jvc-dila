"""Support for JVC DILA via TCP socket based sensors."""
from __future__ import annotations

from typing import Final

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA as PARENT_PLATFORM_SCHEMA,
    SensorEntity,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType, StateType

from .common import JVC_DILA_PLATFORM_SCHEMA, JvcDilaEntity
from .const import (
    ICON_OFF,
    ICON,
)

PLATFORM_SCHEMA: Final = PARENT_PLATFORM_SCHEMA.extend(JVC_DILA_PLATFORM_SCHEMA)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the JVC DILA Sensor."""
    add_entities([JvcDilaSensor(hass, config)])


class JvcDilaSensor(JvcDilaEntity, SensorEntity):
    """Implementation of a JCV DILA via tcp socket based sensor."""

    @property
    def native_value(self) -> StateType:
        """Return the state of the device."""
        return self._state

    @property
    def icon(self) -> str | None:
        if self._state == 2:
            return ICON
        else:
            return ICON_OFF
