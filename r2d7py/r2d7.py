"""
Support for r2d7 shade controllers.

These controllers are from Electronic Solutions Inc (ESI), a
Hunter Douglas Company.  More information can be found at:

http://elec-solutions.com/products/automation-accessories/accessories/r2d7.html

Communication is handled over a remote serial port (NPort) using
telnet protocol.

Michael Dubno - 2018 - New York
"""
import logging

from homeassistant.components.cover import (
    CoverDevice, SUPPORT_OPEN, SUPPORT_CLOSE, SUPPORT_SET_POSITION,
    ATTR_POSITION)

REQUIREMENTS = ['r2d7==0.0.1']

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the r2d7 shade controller and shades."""
    devs = []
    for (area_name, device) in hass.data[R2D7_DEVICES]['cover']:
        dev = LutronCover(area_name, device, hass.data[R2D7_CONTROLLER])
        devs.append(dev)

    add_entities(devs, True)
    return True


class R2D7Cover(LutronDevice, CoverDevice):
    """Representation of a Lutron shade."""

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_SET_POSITION

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        return self._lutron_device.last_level() < 1

    @property
    def current_cover_position(self):
        """Return the current position of cover."""
        return self._lutron_device.last_level()

    def close_cover(self, **kwargs):
        """Close the cover."""
        self._lutron_device.level = 0

    def open_cover(self, **kwargs):
        """Open the cover."""
        self._lutron_device.level = 100

    def set_cover_position(self, **kwargs):
        """Move the shade to a specific position."""
        if ATTR_POSITION in kwargs:
            position = kwargs[ATTR_POSITION]
            self._lutron_device.level = position

    def update(self):
        """Call when forcing a refresh of the device."""
        # Reading the property (rather than last_level()) fetches value
        level = self._lutron_device.level
        _LOGGER.debug("Lutron ID: %d updated to %f",
                      self._lutron_device.id, level)

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attr = {}
        attr['Lutron Integration ID'] = self._lutron_device.id
        return attr
