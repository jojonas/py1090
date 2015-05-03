from collections import namedtuple, defaultdict
from .message import Message

class FlightCollection:
	"""A collection of :py:class:`FlightCollectionEntry`'s, stored by hexident.

	It does not provide groundbreaking new features, but it's a helper that stores flights for easy querying.
	An instance can be queried (``collection['xxxxx']``) and iterated through.
	"""

	def __init__(self):
		self._dictionary = defaultdict(FlightCollectionEntry)

	def __len__(self):
		return len(self._dictionary)

	def __getitem__(self, name):
		if name in self._dictionary:
			return self._dictionary[name]
		else:
			raise KeyError(name)

	def __iter__(self):
		return iter(self._dictionary.values())

	def add(self, message):
		"""Adds a message to this collection.

		Args:
			message (:py:class:`Message`): message to add

		"""
		if not isinstance(message, Message):
			message = Message.from_string(message)
		self._dictionary[message.hexident].append(message)

	def flights(self):
		"""All stored flights.

		Returns:
			list: List of :py:class:`py1090.collection.FlightCollectionEntry`

		"""
		return self._dictionary.values()

	def add_list(self, iterable):
		"""Adds multiple messages to the collection.

		Args:
			iterable (iterable): List, file-like object or :py:class:`Connection` which contains all lines to be added.
				Calls :py:meth:`Message.from_string` on each item if it is not a :py:class:`Message` already.

		"""
		for message in iterable:
			if not isinstance(message, Message):
				message = Message.from_string(item)
			self.add(message)

class FlightCollectionEntry:
	"""Entry of a :py:class:`FlightCollection`. Allows for easy querying flight data, since one single message does not contain all the data
	information about a flight.

	See Also:
		:py:class:`Message`
			For details about the accuracy of the positional information provided by this class.

	"""
	def __init__(self):
		self.messages = []
		self.hexident = None

	def append(self, message):
		"""Adds a message that should belong to this collection.

		Will raise an exception if the message hexident does not match the one of the flight. Only adds message of type 'MSG'
		(transmission messages).

		Args:
			message (Message): the message to append

		"""
		if self.hexident is None:
			self.hexident = message.hexident
		else:
			if self.hexident != message.hexident:
				raise ValueError("Added message of different hexident.")

		if message.message_type == 'MSG':
			self.messages.append(message)

	@property
	def last_position(self):
		"""Finds the last known position of the flight (by iterating backwards through collected messages).

		Returns:
			tuple: a tuple of :py:class:`float` if the position was ever recorded, (None, None) otherwise.

		"""
		for message in reversed(self.messages):
			if message.latitude and message.longitude:
				return (message.latitude, message.longitude)
		return None, None

	@property
	def last_altitude(self):
		"""Finds the last known altitude of the flight (by iterating backwards through collected messages).

		Returns:
			float: the altitude in feet, None otherwise.

			"""
		for message in reversed(self.messages):
			if message.altitude:
				return message.altitude
		return None

	@property
	def path(self):
		"""Reconstructs the flight path. Yields it as an iterator.

		Yields:
			tuple: (lat, lon, alt) describing the latitude, longitude and altitude of a message

		"""
		for message in self.messages:
			lat, lon, alt = message.latitude, message.longitude, message.altitude
			if lat and lon and alt:
				yield (lat, lon, alt)


	def __iter__(self):
		return iter(self.messages)

