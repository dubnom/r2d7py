"""
r2d7py is a library for controlling shades using a controller from
Electronic Solutions Inc (ESI), a Hunter Douglas Company.

More information can be found at:

http://elec-solutions.com/products/automation-accessories/accessories/r2d7.html

Communication is handled over a remote serial port (NPort) using
telnet protocol.

Michael Dubno - 2018 - New York
"""

from threading import Thread
import time
import telnetlib

MAX_ADDRS = 7
MAX_UNITS = 60


class R2D7Shade(object):
    """Represent one (or a pre-coded group) of shades."""
    def __init__(self, hub, addr, unit, length):
        self._hub = hub
        self._addr = addr
        self._unit = unit
        self._length = length
        self._position = 0.
        # FIX: Close the shade automatically at start up
        #      so it will be in a known position

    def open(self):
        """Open the shade."""
        self.position = 100

    def close(self):
        """Close the shade."""
        self.position = 0

    @property
    def position(self):
        """Get the position of the shade."""
        return self._position

    @position.setter
    def position(self, position):
        """Set the position of the shade."""
        amount = position - self._position
        duration = int(20. * self._length * amount / 100.)
        self._hub.move(self._addr, self._unit, duration)
        self._position = position


class R2D7Hub(Thread):
    """Interface with an R2D7 shade controller."""

    def __init__(self, host, port):
        Thread.__init__(self, target=self)
        self._host = host
        self._port = port

        self._telnet = None
        self._running = False
        self._connect()
        self.start()

    def _connect(self):
        # FIX: Add userID and password
        self._telnet = telnetlib.Telnet(self._host, self._port)

    def shade(self, addr, unit, length):
        """Create an object for each shade unit."""
        if 0 < addr <= MAX_ADDRS and 0 < unit <= MAX_UNITS:
            return R2D7Shade(self, addr, unit, length)
        raise ValueError('Address or Unit is out of range.')

    def move(self, addr, unit, duration):
        """Move the shade a relative +/- duration."""
        # duration is specified as 20ths of a second
        if duration != 0:
            direction = ['o', 'c'][duration > 0]
            duration = abs(duration)
            self._send('*%d%s%02d%03d;' % (addr, direction, unit, duration))

    def _send(self, command):
        # FIX: If error, reconnect
        self._telnet.write((command+'\n').encode('utf8'))

    def run(self):
        # FIX: In the future do something with the feedback
        self._running = True
        while self._running:
            self._telnet.read_until(b' ', 1.)

    def close(self):
        """Close the connection to the controller."""
        self._running = False
        if self._telnet:
            time.sleep(1.)
            self._telnet.close()
            self._telnet = None
