import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import dump1090 

def collection_example():
	with dump1090.Connection() as connection:
		collection = dump1090.FlightCollection()
		
		while True:
			print("Number of flights in collection:", len(collection))
			for line in connection:
				message = dump1090.Message.from_string(line)
				collection.add(message)

if __name__ == "__main__":
	collection_example()
	