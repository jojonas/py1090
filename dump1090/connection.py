import socket
import select
import io

from .message import Message

class Connection(io.TextIOWrapper):
	def __init__(self, *, host="127.0.0.1", port=30003):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host, port))
		
		# have to keep a reference of the wrapper, otherwise it is garbage collected at the end of 
		# the __init__ function and we will get an error 'I/O operation on closed file'.
		self._wrapper = self.socket.makefile('r')
		super().__init__(self._wrapper.buffer, encoding=self._wrapper.encoding, errors=self._wrapper.errors)
		
	def __next__(self):
		# make this iterator non-blocking
		while not self.has_data():
			pass
		return super().__next__()
		
	def has_data(self):
		rlist, _, _ = select.select([ self.socket ], [], [], 0)
		return len(rlist) > 0
		
	def readmessage(self):
		return Message.from_string(self.readline())
		
	def __del__(self):
		self.socket.close()
		