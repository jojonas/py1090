from collections import namedtuple, defaultdict
import csv
csv.register_dialect('excel-modern', delimiter=';', lineterminator='\n', quoting=csv.QUOTE_NONE)

from .message import Message

class FlightCollectionEntry:
	def __init__(self):
		self.messages = []
		self.hexident = None
	
	def append(self, message):
		if self.hexident is None:
			self.hexident = message.hexident
		else:
			if self.hexident != message.hexident:
				raise ValueError("Added message of different hexident.")

		self.messages.append(message)

	@property
	def last_position(self):
		for message in reversed(self.messages):
			if message.latitude and message.longitude:
				return (message.latitude, message.longitude)
		return None, None

	@property
	def last_altitude(self):
		for message in reversed(self.messages):
			if message.altitude:
				return message.altitude
		return None

	@property
	def path(self):
		for message in self.messages:
			lat, lon, alt = message.latitude, message.longitude, message.altitude
			if lat and lon and alt:
				yield (lat, lon, alt)


	def __iter__(self):
		return iter(self.messages)



class FlightCollection:
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
		self._dictionary[message.hexident].append(message)
			
	def flights(self):
		return self._dictionary.values()

	def add_list(self, list):
		for item in list:
			message = Message.from_string(item)
			self.add(message)
	