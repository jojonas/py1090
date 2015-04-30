import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import time
import os

import dump1090 

def record_to_database(filename):
	with dump1090.Connection() as connection:
		database = dump1090.FlightDatabase(connection)
		
		if os.path.isfile(filename):
			database.load_csv(filename)
			
		try:
			while True:
				print("Number of flights:", len(database))
				database.update()
				time.sleep(0.5)
		finally:
			database.dump_csv(filename)
		

if __name__ == "__main__":
	record_to_database("example_flight_database.csv")
	