import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import os.path
from collections import defaultdict, namedtuple

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

import py1090

from example_helpers import map_bounds, blacklist_hexidents

def basemap_plot_paths(filename):
	m = Basemap(projection='merc', resolution='i', **map_bounds['europe'])
	
	fig = plt.figure()
	ax = Axes3D(fig)
	
	ax.add_collection3d(m.drawcoastlines(linewidth=0.25))
	ax.add_collection3d(m.drawcountries(linewidth=0.35))

	collection = py1090.FlightCollection()

	#with py1090.Connection() as connection:
	with open(filename, 'r') as connection:
		collection.add_list(connection)

	for flight in collection:
		if flight.hexident in blacklist_hexidents:
			continue

		path = list(flight.path)
		if len(path) > 1:
			lats, lons, alts = np.array(path).T
			x, y = m(lons, lats)
			m.plot(x,y, alts,".-")
	
	plt.title("Flights in file '{:s}'".format(filename))
	plt.show()
	
if __name__ == "__main__":
	filename = "example_recording.txt"
	
	if not os.path.isfile(filename):
		print("Run example 'record_raw_to_file.py' to create a sample flight recording first.")
	else:
		basemap_plot_paths(filename)
	