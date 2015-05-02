"""
This module provides a pythonic way to process ADS-B messages. It can work with any software that provides BaseStation-like output,
for example `dump1090 <https://github.com/antirez/dump1090>`_.
"""
from .connection import Connection
from .message import Message
from .collection import FlightCollection