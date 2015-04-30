from collections import namedtuple, defaultdict
import csv
csv.register_dialect('excel-modern', delimiter=';', lineterminator='\n', quoting=csv.QUOTE_NONE)

from .message import _parse_or_none, _parse_bool

class FlightEntry:
	COPY_FROM_MESSAGE = [ 'hexident', 'session_id', 'aircraft_id', 'flight_id', 'callsign', 
				'altitude', 'ground_speed', 'track', 'latitude', 'longitude', 'vertical_rate',  
				'squawk', 'squawk_alert', 'emergency', 'spi', 'on_ground' ]
				
	def __init__(self):
		for name in self.COPY_FROM_MESSAGE:
			setattr(self, name, None)
			
		self.last_update = None
		self.last_message = None
	
	def update(self, message):
		for name in self.COPY_FROM_MESSAGE:
			if hasattr(message, name) and getattr(message, name) is not None:
				setattr(self, name, getattr(message, name))
				
		self.last_update = message.generation_time
		self.last_message = message

class FlightDatabase:
	def __init__(self, connection=None):
		self.connection = connection
		self.dictionary = defaultdict(FlightEntry)
		
	def __len__(self):
		return len(self.dictionary)
		
	def update(self):
		if not self.connection:
			raise ValueError("Running without live connection.")
			
		while self.connection.has_data():
			message = self.connection.readmessage()
			self.dictionary[message.hexident].update(message)
			
	def flights(self):
		return self.dictionary.values()
	
	def dump_csv(self, filename):
		with open(filename, 'w') as file:
			fieldnames = FlightEntry.COPY_FROM_MESSAGE + ['last_update']
			writer = csv.DictWriter(file, dialect='excel-modern', fieldnames=fieldnames)
			writer.writeheader()
			for entry in self.dictionary.values():
				dict = {}
				for name in fieldnames:
					dict[name] = getattr(entry, name)
				writer.writerow(dict)
		
	def load_csv(self, filename):
		with open(filename, 'r') as file:
			reader = csv.DictReader(file, dialect='excel-modern')
			for row in reader:
				hexident = row['hexident']
				message = self.dictionary[hexident]
				for name, value in row.items():
					setattr(message, name, value)
					
				for field in ('session_id', 'aircraft_id', 'flight_id', 'altitude', 'ground_speed',
					'track', 'vertical_rate', 'squawk'):
					setattr(message, field, _parse_or_none(getattr(message, field), int))
					
				for field in ('latitude', 'longitude'):
					setattr(message, field, _parse_or_none(getattr(message, field), float))
			
				for field in ('squawk_alert', 'emergency', 'spi', 'on_ground'):
					setattr(message, field, _parse_or_none(getattr(message, field), _parse_bool))

			