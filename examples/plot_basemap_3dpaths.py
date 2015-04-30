import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import os.path
from collections import defaultdict, namedtuple

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

import dump1090

from example_helpers import calculate_map_bounds, blacklist_hexidents

class Path:
	def __init__(self):
		self.lats = []
		self.lons = []
		self.alts = []

def basemap_plot_paths(filename):
	paths = defaultdict(Path)
	
	lats, lons = [], []
	#with dump1090.Connection() as file:
	with open(filename, 'r') as file:
		count = 0
		for line in file:
			count += 1
			if count % 100 == 0:
				print("Processing message #{:d}".format(count))
				
			message = dump1090.Message.from_string(line)
			if message.latitude and message.longitude and message.altitude and message.hexident not in blacklist_hexidents:
				if message.longitude < 3:
					print("AAAAAAAAAAAAAAAAAAA", message.hexident)
				paths[message.hexident].lats.append(message.latitude)
				paths[message.hexident].lons.append(message.longitude)
				paths[message.hexident].alts.append(message.altitude)
				
				lats.append(message.latitude)
				lons.append(message.longitude)

	m = Basemap(projection='merc', resolution='i', **calculate_map_bounds(lats, lons, fraction=0.3))
	
	fig = plt.figure()
	ax = Axes3D(fig)
	
	ax.add_collection3d(m.drawcoastlines(linewidth=0.25))
	ax.add_collection3d(m.drawcountries(linewidth=0.35))

	color_cycle = ['r', 'g', 'b', 'k', 'y', 'orange', 'purple', 'lightblue', 'gray']
	for i, path in enumerate(paths.values()):
		if i > 20: break
		
		x, y = m(path.lons, path.lats)
		z = path.alts

		ax.plot(x, y, z, '.-', color=color_cycle[i % len(color_cycle)])

	plt.title("Paths in file '{:s}'".format(filename))
	plt.show()
	
if __name__ == "__main__":
	filename = "../dump.txt" # "example_recording.txt"
	
	if not os.path.isfile(filename):
		print("Run example 'record_raw_to_file.py' to create a sample flight recording first.")
	else:
		basemap_plot_paths(filename)
	