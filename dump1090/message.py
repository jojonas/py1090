from enum import Enum
from datetime import datetime
	
# http://www.homepages.mcb.net/bones/SBS/Article/Barebones42_Socket_Data.htm
def _parse_datetime(datestr, timestr):
	date = datetime.strptime(datestr, '%Y/%m/%d')
	
	timestr, separator, millisstr = timestr.rpartition('.')
	time = datetime.strptime(timestr, '%H:%M:%S')
	
	seconds = float(separator + millisstr)
	time = time.replace(microsecond=int(seconds*1000000))
	
	return datetime.combine(date.date(), time.time())
	
def _parse_bool(str):
	if str.lower() in ('true', 'y', 'yes', 'on', '1'):
		return True
	elif str.lower() in ('false', 'n', 'no', 'off', '0'):
		return False
	
def _parse_or_none(value, function):
	if len(value) == 0:
		return None
	else:
		return function(value)
		
		
def _dump_datetime(time):
	str = datetime.strftime(time, '%Y/%m/%d,%H:%M:%S')
	str += '.{:03d}'.format(int(time.microsecond/1000))
	return str

def _dump_bool(value):
	if value == True:
		return '1'
	else:
		return '0'

def _dump_or_none(value, func=str):
	if value is None:
		return ''
	else:
		return func(value)
		
def iter_messages(iterator):
	for item in iterator:
		yield Message.from_string(item)
	
class Message:
	def to_string(self):
		format_coordinates = lambda x: '{:.5f}'.format(x)
		
		return ','.join((
			_dump_or_none(self.message_type),
			_dump_or_none(self.transmission_type),
			_dump_or_none(self.session_id),
			_dump_or_none(self.aircraft_id),
			_dump_or_none(self.hexident),
			_dump_or_none(self.flight_id),
			_dump_or_none(self.generation_time, _dump_datetime),
			_dump_or_none(self.record_time, _dump_datetime),
			_dump_or_none(self.callsign),
			_dump_or_none(self.altitude),
			_dump_or_none(self.ground_speed),
			_dump_or_none(self.track),
			_dump_or_none(self.latitude, format_coordinates),
			_dump_or_none(self.longitude, format_coordinates),
			_dump_or_none(self.vertical_rate),
			_dump_or_none(self.squawk),
			_dump_or_none(self.squawk_alert, _dump_bool),
			_dump_or_none(self.emergency, _dump_bool),
			_dump_or_none(self.spi, _dump_bool),
			_dump_or_none(self.on_ground, _dump_bool),
		)) + '\n'
		
	@classmethod
	def from_string(cls, string):
		message = cls()
		parts = string.strip().split(',')
		
		# (MSG, STA, ID, AIR, SEL or CLK)
		message.message_type = _parse_or_none(parts[0].upper(), str)
	
		# MSG sub types 1 to 8. Not used by other message types.
		message.transmission_type = _parse_or_none(parts[1], int)
		
		# Database Session record number
		if parts[2] != '111':
			message.session_id = _parse_or_none(parts[2], int)
		else:
			message.session_id = None
		
		# Database Aircraft record number
		if parts[3] != '11111':
			message.aircraft_id = _parse_or_none(parts[3], int)									
		else:
			message.aircraft_id = None
		
		# Aircraft Mode S hexadecimal code
		message.hexident = _parse_or_none(parts[4].upper(), str)
		
		# Database Flight record number
		if parts[5] != '111111':
			message.flight_id = _parse_or_none(parts[5].upper(), str)
		else:
			message.flight_id = None
		
		if len(parts[6]) > 0 and len(parts[7]) > 0:
			message.generation_time = _parse_datetime(parts[6], parts[7])
		else:
			message.generation_time = None
			
		if len(parts[8]) > 0 and len(parts[8]) > 0:
			message.record_time = _parse_datetime(parts[8], parts[9])
		else:
			message.record_time = None
		
		# An eight digit flight ID - can be flight number or registration (or even nothing).
		message.callsign = _parse_or_none(parts[10].upper(), str)
		
		# Mode C altitude. Height relative to 1013.2mb (Flight Level). Not height AMSL..
		message.altitude = _parse_or_none(parts[11], int)
		
		# Speed over ground (not indicated airspeed)
		message.ground_speed = _parse_or_none(parts[12], int)
		
		# Track of aircraft (not heading). Derived from the velocity E/W and velocity N/S
		message.track = _parse_or_none(parts[13], int)
		
		# North and East positive.
		message.latitude = _parse_or_none(parts[14], float)
		
		# South and West negative.
		message.longitude = _parse_or_none(parts[15], float)
	
		# 64ft resolution
		message.vertical_rate = _parse_or_none(parts[16], int)
		
		# Assigned Mode A squawk code.
		message.squawk = _parse_or_none(parts[17], int)
		
		# Flag to indicate squawk has changed.
		message.squawk_alert = _parse_or_none(parts[18], _parse_bool)
		
		# Flag to indicate emergency code has been set
		message.emergency = _parse_or_none(parts[19], _parse_bool)
		
		# Flag to indicate transponder Ident has been activated.
		message.spi = _parse_or_none(parts[20], _parse_bool)
		
		# Flag to indicate ground squat switch is active
		message.on_ground = _parse_or_none(parts[21], _parse_bool)
		
		return message
		
