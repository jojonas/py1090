import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import py1090 
		
def record_positions_to_file(filename):
	with py1090.Connection() as connection, open(filename, 'a') as file:
		lines = 0
		for line in connection:
			message = py1090.Message.from_string(line)
			if message.latitude and message.longitude:
				file.write(line)
				lines += 1			
				print("Recorded lines:", lines)

if __name__ == "__main__":
	record_positions_to_file("example_recording.txt")
	