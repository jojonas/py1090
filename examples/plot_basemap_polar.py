import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import os.path
import math

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

import dump1090 

from example_helpers import calculate_map_bounds, blacklist_hexidents

def basemap_plot_distances(filename, home):
	# number of sections
	N = 120
	r_earth = 6371e3 # m
	
	max_distance = 0
	
	bins = np.zeros(N)
	
	
	counter = 0
	lats, lons = [], []
	ids = set()
	#with dump1090.Connection() as file:
	with open(filename, 'r') as file:
		for line in file:
			counter += 1
			if counter % 100 == 0:
				print("Processing message #{:d}.".format(counter))
			message = dump1090.Message.from_string(line)
			if message.latitude and message.longitude and message.hexident not in blacklist_hexidents:
				lats.append(message.latitude)
				lons.append(message.longitude)
			
				lambda1 = math.radians(home[1])
				lambda2 = math.radians(message.longitude)
			
				phi1 = math.radians(home[0])
				phi2 = math.radians(message.latitude)	
			
				dphi = phi2-phi1
				dlambda = lambda2-lambda1
				
				a = math.pow(math.sin(dphi/2), 2) + math.cos(phi1)*math.cos(phi2)*math.pow(math.sin(dlambda/2), 2)
				dsigma = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
				
				bearing = math.atan2(math.sin(dlambda)*math.cos(phi1), \
					math.cos(phi2)*math.sin(phi1)-math.sin(phi2)*math.cos(phi1)*math.cos(dlambda)) #\
				
				distance = r_earth*dsigma
				
				ids.add(message.hexident)
				
				if distance > 500e3:
					print("Warning: coordinates", message.latitude, ",", message.longitude, "sent by plane", message.hexident, "are very far away, skipping for now, you may consider blacklisting though.")
					continue
				
				bin = round(bearing * N / (2*math.pi))
				
				if distance > bins[bin]:
					bins[bin] = distance
				
				if distance > max_distance:
					max_distance = distance
			
			
	print("Anzahl:", len(ids))
	
	m = Basemap(projection='stere', resolution='i', lat_0=home[0], lon_0=home[1], width=max_distance*2, height=max_distance*2)
	
	fig = plt.figure()
	ax_map = fig.add_subplot(111)
	
	x, y = m(home[1], home[0])
	m.scatter(x, y, zorder=1000, color="red")
	
	#x, y = m(lons, lats)
	#m.scatter(x, y, zorder=999, color="gray")
	
	m.drawcoastlines()
	m.fillcontinents(color='white', lake_color='white')
	m.drawcountries()
	
	ax_polar = fig.add_axes(ax_map.get_position(), polar=True, frameon=False)
	ax_polar.set_autoscale_on(False)
	ax_polar.set_ylim(0, max_distance/1000)
	
	#ax_polar.plot(np.array(ds)-math.pi/2, np.array(rs)/1000, 'x')
	ax_polar.fill(np.linspace(0, 2*math.pi, N) - math.pi/2, bins/1000, alpha=0.5)
	ax_polar.xaxis.set_ticklabels([])
	
	plt.title("Maximal distance: {:.1f} km".format(max_distance / 1000))
	plt.show()
	
if __name__ == "__main__":
	filename = "../dump.txt" #example_recording.txt"
	home = (50.775346, 6.083887) # lon, lat of Aachen, Germany
	
	if not os.path.isfile(filename):
		print("Run example 'record_raw_to_file.py' to create a sample flight recording first.")
	else:
		basemap_plot_distances(filename, home)
	
	