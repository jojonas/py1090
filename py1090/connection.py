import socket
import select
import io

from .message import Message

class Connection(io.TextIOWrapper):
	"""File like object which can be used to read BaseStation messages from a TCP server.

	The connection can be used as contextmanager (:keyword:`with`-block) and as iterator: ::

		with Connection() as connection:
			for line in connection:
				print(line)

	Args:
		host(str): IP or hostname
		port(int): Port number

	"""

	def __init__(self, host="localhost", port=30003):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host, port))

		# have to keep a reference of the wrapper, otherwise it is garbage collected at the end of
		# the __init__ function and we will get an error 'I/O operation on closed file'.
		self._wrapper = self.socket.makefile('r')
		super().__init__(self._wrapper.buffer, encoding=self._wrapper.encoding, errors=self._wrapper.errors)

	def __next__(self):
		# make this iterator non-blocking for Ctrl+C
		while not self.has_data():
			pass
		return super().__next__()


	def has_data(self):
		"""Checks if the socket currently has data available for reading (using :py:func:`select.select`).

		Returns:
			bool: True if there is data available for reading, False otherwise.

		"""
		rlist, _, _ = select.select([ self.socket ], [], [], 0)
		return len(rlist) > 0

	def readmessage(self):
		"""Reads a single line from the connection, parses it via :py:meth:`Message.from_string` and returns it.

		Returns:
			Message: next unread message from socket
		"""
		return Message.from_string(self.readline())

	def __del__(self):
		self.socket.close()
