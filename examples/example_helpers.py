def calculate_map_bounds(lats, lons, fraction=1):
	import numpy as np

	latrange = np.max(lats) - np.min(lats)
	lonrange = np.max(lons) - np.min(lons)

	padding = fraction * max(latrange, lonrange)

	result = {}
	result['llcrnrlat'] = max(np.min(lats) - padding, -90)
	result['urcrnrlat'] = min(np.max(lats) + padding, 90)
	result['llcrnrlon'] = max(np.min(lons) - padding, -90)
	result['urcrnrlon'] = min(np.max(lons) + padding, 90)

	print(result)

	return result

def example_data_file():
	import sys, os.path

	if len(sys.argv) > 1:
		filename = sys.argv[1]
		if not os.path.isfile(filename):
			raise IOError("File '{filename:s}' does not exist.".format(filename=filename))
	else:
		filename = 'example_recording.txt'
		if not os.path.isfile(filename):
			raise IOError("Run example 'record_raw_to_file.py' to create a sample flight recording first.")

	return filename


map_bounds = {
	"europe": {
		"urcrnrlat": 70,
		"urcrnrlon": 40,
		"llcrnrlat": 35,
		"llcrnrlon": -15,
	},
	"usa": {
		"urcrnrlat": 50,
		"urcrnrlon": -65,
		"llcrnrlat": 23,
		"llcrnrlon": -125,
	},
	"canada": {
		"urcrnrlat": 75,
		"urcrnrlon": -55,
		"llcrnrlat": 45,
		"llcrnrlon": -140,
	}
}

blacklist_hexidents = (
	'406B88',
	'400C7D',
	'400584',
	'405F12',
	)

