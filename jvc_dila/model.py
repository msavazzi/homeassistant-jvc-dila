"""Models for JVC DILA platform."""
from __future__ import annotations

from typing import TypedDict

from homeassistant.helpers.template import Template


class JvcDilaSensorConfig(TypedDict):
    """TypedDict for JvcDila Sensor config."""

    name: str
    host: str
    port: str
    timeout: int
