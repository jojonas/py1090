def calculate_map_bounds(lats, lons, fraction=3):
	import numpy as np

	latrange = np.max(lats) - np.min(lats)
	lonrange = np.max(lons) - np.min(lons)
	
	padding = fraction * max(latrange, lonrange)
	
	result = {}
	result['llcrnrlat'] = np.min(lats) - padding
	result['urcrnrlat'] = np.max(lats) + padding
	result['llcrnrlon'] = np.min(lons) - padding
	result['urcrnrlon'] = np.max(lons) + padding
	
	return result
	
	
blacklist_hexidents = ('406B88', '400C7D', '400584')
	