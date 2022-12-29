"""Common code for JVC DILA component."""
from __future__ import annotations

import logging
import select
import socket
import time

##import time
from typing import Any, Final

import voluptuous as vol

from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_TIMEOUT,
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType

from .const import (
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    ICON,
)
from .model import JvcDilaSensorConfig

_LOGGER: Final = logging.getLogger(__name__)

JVC_DILA_PLATFORM_SCHEMA: Final[dict[vol.Marker, Any]] = {
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT): cv.port,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
}


class JvcDilaEntity(Entity):
    """Base entity class for JVC DILA platform."""

    def __init__(self, hass: HomeAssistant, config: ConfigType) -> None:
        """Set all the config values if they exist and get initial state."""

        self._attr_icon = ICON
        self._hass = hass
        self._config: JvcDilaSensorConfig = {
            CONF_NAME: config[CONF_NAME],
            CONF_HOST: config[CONF_HOST],
            CONF_PORT: config[CONF_PORT],
            CONF_TIMEOUT: config[CONF_TIMEOUT],
        }

        self._state: str | None = None
        self.update()

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return self._config[CONF_NAME]

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return (
            "JVC-DILA-"
            + self._config[CONF_HOST].replace(".", "_")
            + "-"
            + str(self._config[CONF_PORT])
        )

    def update(self) -> None:
        retry = 0
        """Get the latest value for this sensor."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self._config[CONF_TIMEOUT])
            try:
                sock.connect((self._config[CONF_HOST], self._config[CONF_PORT]))
            except OSError as err:
                retry = retry + 1
                _LOGGER.error(
                    "%s Unable to connect to %s on port %s: %s",
                    retry,
                    self._config[CONF_HOST],
                    self._config[CONF_PORT],
                    err,
                )
                """
                Timeout we consider it meaning Meaning
                0 - Power Off
                """
                if retry > 5:
                    self._state = 0
                    sock.close()
                    return
                else:
                    time.sleep(0.6)

            readable, _, _ = select.select([sock], [], [], self._config[CONF_TIMEOUT])
            if not readable:
                _LOGGER.warning(
                    "Timeout (%s second(s)) waiting for a response after "
                    "reading from %s on port %s",
                    self._config[CONF_TIMEOUT],
                    self._config[CONF_HOST],
                    self._config[CONF_PORT],
                )
                sock.close()
                return

            """ Project sends PJ_OK """
            value = sock.recv(1024).decode()
            time.sleep(0.6)

            """ Reply PJREQ within 5 sec """
            try:
                sock.send("PJREQ".encode())
                time.sleep(0.6)
            except OSError as err:
                _LOGGER.warning(
                    "Unable to send PJREQ on port %s: %s error %s",
                    self._config[CONF_HOST],
                    self._config[CONF_PORT],
                    err,
                )
                sock.close()
                return

            readable, _, _ = select.select([sock], [], [], self._config[CONF_TIMEOUT])
            if not readable:
                _LOGGER.warning(
                    "Timeout (%s second(s)) waiting for a response after PJREQ"
                    "reading from %s on port %s",
                    self._config[CONF_TIMEOUT],
                    self._config[CONF_HOST],
                    self._config[CONF_PORT],
                )
                sock.close()
                return

            """ Projector sends PJACK """
            value = sock.recv(1024).decode()
            time.sleep(0.6)

            """ prepare command in buffer """
            buffer = bytearray(6)
            buffer[0] = 0x3F
            buffer[1] = 0x89
            buffer[2] = 0x01
            buffer[3] = 0x50
            buffer[4] = 0x57
            buffer[5] = 0x0A

            retry = 0
            while True:
                try:
                    sock.send(buffer)
                    time.sleep(0.6)
                except OSError as err:
                    _LOGGER.warning(
                        "Unable to send buffer to %s on port %s error %s",
                        self._config[CONF_HOST],
                        self._config[CONF_PORT],
                        err,
                    )
                    sock.close()
                    return

                """ Projector Acknowledge request"""
                value = sock.recv(6)
                time.sleep(0.6)
                if len(value) > 0:
                    break
                else:
                    retry = retry + 1
                if retry > 5:
                    break

            """ Projectr Request response details """
            value = sock.recv(7)
            time.sleep(0.6)

            """ Explicit close to free the projector """
            sock.close()

            """
            Response (RR) Meaning
            0x30 - Standby
            0x31 - Power On
            0x32 - Cooling
            0x34 - Emergency

            to use option we subtract 0x2F so index is
            0 -> Power Off
            1 -> Standby
            2 -> Power On
            3 -> Cooling
            5 -> Emergency
            """

        if value[5] == 0x34:
            _LOGGER.error(
                "JVC DILA reporter Emergency condition %s",
                value,
            )

        self._state = value[5] - 0x2F
        # self.state = self.options[value[5] - 0x2F]
