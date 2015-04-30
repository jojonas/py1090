import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import os.path

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

import dump1090 

from example_helpers import calculate_map_bounds

def basemap_plot_positions(filename):
	#connection = dump1090.Connection()
	database = dump1090.FlightDatabase()
	database.load_csv(filename)
	
	lats, lons = [], []
	print("Loading positions...")
	for flight in database.flights():
		if flight.latitude and flight.longitude:
			print(flight.latitude, flight.longitude)
			lats.append(flight.latitude)
			lons.append(flight.longitude)
	
	m = Basemap(projection='merc', resolution='i', **calculate_map_bounds(lats, lons))
	
	x, y = m(lons, lats) # apply projection
	m.scatter(x, y, 3, marker='s', color='red', zorder=1000)
	
	m.drawcoastlines()
	m.fillcontinents(color='white', lake_color='white')
	m.drawcountries()
	
	plt.title("Flights in Database '{:s}'".format(filename))
	plt.show()
	
if __name__ == "__main__":
	filename = "example_flight_database.csv"
	
	if not os.path.isfile(filename):
		print("Run example 'persistent_flight_database.py' to create a sample database first.")
	else:
		basemap_plot_positions(filename)
	