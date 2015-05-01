import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import os.path
import math

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

import dump1090 
from dump1090.helpers import distance_between, bearing_between

from example_helpers import calculate_map_bounds, blacklist_hexidents

def basemap_plot_distances(filename, home):
	# number of sections
	N = 120

	bins = np.zeros(N)
	
	collection = dump1090.FlightCollection()
	#with dump1090.Connection() as file:
	with open(filename, 'r') as file:
		collection.add_list(file)

	for flight in collection:
		if flight.hexident in blacklist_hexidents:
			continue

		for lat, lon, alt in flight.path:
			bearing = bearing_between(home[0], home[1], lat, lon)
			distance = distance_between(home[0], home[1], lat, lon)
			
			if distance > 500e3:
				print("Warning: coordinates", message.latitude, ",", message.longitude, "sent by plane", message.hexident, "are very far away, skipping for now, you may consider blacklisting though.")
				continue
			
			bin = round(bearing * N / (2*math.pi))
			
			if distance > bins[bin]:
				bins[bin] = distance
	
	m = Basemap(projection='stere', resolution='i', lat_0=home[0], lon_0=home[1], width=bins.max()*2, height=bins.max()*2)
	
	fig = plt.figure()
	ax_map = fig.add_subplot(111)
	
	m.drawcoastlines()
	m.fillcontinents(color='white', lake_color='white')
	m.drawcountries()
	
	ax_polar = fig.add_axes(ax_map.get_position(), polar=True, frameon=False)
	ax_polar.set_autoscale_on(False)
	ax_polar.set_ylim(0, bins.max()/1000)
	
	ax_polar.fill(np.linspace(0, 2*math.pi, N) - math.pi/2, bins/1000, alpha=0.5)
	ax_polar.xaxis.set_ticklabels([])
	
	plt.title("Maximal distance: {:.1f} km".format(bins.max() / 1000))
	plt.show()
	
if __name__ == "__main__":
	filename = "example_recording.txt"
	home = (50.775346, 6.083887) # lon, lat of Aachen, Germany
	
	if not os.path.isfile(filename):
		print("Run example 'record_raw_to_file.py' to create a sample flight recording first.")
	else:
		basemap_plot_distances(filename, home)
	
	