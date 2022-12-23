"""Provides a binary sensor which gets its values from a JCV DILA via tcp socket."""
from __future__ import annotations

from typing import Final
from .const import (
    ICON_OFF,
    ICON,
)

from homeassistant.components.binary_sensor import (
    PLATFORM_SCHEMA as PARENT_PLATFORM_SCHEMA,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .common import JVC_DILA_PLATFORM_SCHEMA, JvcDilaEntity

PLATFORM_SCHEMA: Final = PARENT_PLATFORM_SCHEMA.extend(JVC_DILA_PLATFORM_SCHEMA)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the JCV DILA via tcp binary sensor."""
    add_entities([JvcDilaBinarySensor(hass, config)])


class JvcDilaBinarySensor(JvcDilaEntity, BinarySensorEntity):
    """A binary sensor which is on when its state == CONF_VALUE_ON."""

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self._state == 2

    @property
    def icon(self) -> str | None:
        if self._state == 2:
            return ICON
        else:
            return ICON_OFF
