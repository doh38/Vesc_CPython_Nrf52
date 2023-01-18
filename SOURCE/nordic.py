# SPDX-FileCopyrightText: 2019 Dan Halbert for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`nordic`
====================================================

This module provides Services used by Nordic Semiconductors.

"""

from __future__ import annotations

from . import Service
from ..uuid import VendorUUID
from ..characteristics.stream import StreamOut, StreamIn

try:
    from typing import Optional, TYPE_CHECKING

    if TYPE_CHECKING:
        from circuitpython_typing import WriteableBuffer, ReadableBuffer
        import _bleio

except ImportError:
    pass

__version__ = "9.0.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE.git"


class UARTService(Service):
    """
    Provide UART-like functionality via the Nordic NUS service.

    See ``examples/ble_uart_echo_test.py`` for a usage example.
    """

    # pylint: disable=no-member
    uuid = VendorUUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
    _server_tx = StreamOut(
        uuid=VendorUUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
        timeout=0.2,
        buffer_size=16384,
    )
    _server_rx = StreamIn(
        uuid=VendorUUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
        timeout=0.2,
        buffer_size=8192,
    )

    def __init__(self, service: Optional[_bleio.Service] = None) -> None:
        super().__init__(service=service)
        self.connectable = True
        if not service:
            self._rx = self._server_rx
            self._tx = self._server_tx
        else:
            # If we're a client then swap the characteristics we use.
            self._tx = self._server_rx
            self._rx = self._server_tx

    def read(self, nbytes: Optional[int] = None) -> Optional[bytes]:
        """
        Read characters. If ``nbytes`` is specified then read at most that many bytes.
        Otherwise, read everything that arrives until the connection times out.
        Providing the number of bytes expected is highly recommended because it will be faster.

        :return: Data read
        :rtype: bytes or None
        """
        return self._rx.read(nbytes)

    def readinto(
        self, buf: WriteableBuffer, nbytes: Optional[int] = None
    ) -> Optional[int]:
        """
        Read bytes into the ``buf``. If ``nbytes`` is specified then read at most
        that many bytes. Otherwise, read at most ``len(buf)`` bytes.

        :return: number of bytes read and stored into ``buf``
        :rtype: int or None (on a non-blocking error)
        """
        return self._rx.readinto(buf, nbytes)

    def readline(self) -> Optional[bytes]:
        """
        Read a line, ending in a newline character.

        :return: the line read
        :rtype: bytes or None
        """
        return self._rx.readline()

    @property
    def in_waiting(self) -> int:
        """The number of bytes in the input buffer, available to be read."""
        return self._rx.in_waiting

    def reset_input_buffer(self) -> None:
        """Discard any unread characters in the input buffer."""
        self._rx.reset_input_buffer()

    def write(self, buf: ReadableBuffer) -> None:
        """Write a buffer of bytes."""
        self._tx.write(buf)
