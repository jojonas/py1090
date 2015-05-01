import math

earth_radius = 6371.0e3 #m

def distance_between(lat1, lon1, lat2, lon2):
	lambda1 = math.radians(lon1)
	lambda2 = math.radians(lon2)
		
	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)	

	dphi = phi2-phi1
	dlambda = lambda2-lambda1
	
	a = math.pow(math.sin(dphi/2), 2) + math.cos(phi1)*math.cos(phi2)*math.pow(math.sin(dlambda/2), 2)
	dsigma = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
	
	distance = earth_radius * dsigma

	return distance

def bearing_between(lat1, lon1, lat2, lon2):
	lambda1 = math.radians(lon1)
	lambda2 = math.radians(lon2)
		
	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)	

	dphi = phi2-phi1
	dlambda = lambda2-lambda1
	
	bearing = math.atan2(math.sin(dlambda)*math.cos(phi1), \
		math.cos(phi2)*math.sin(phi1)-math.sin(phi2)*math.cos(phi1)*math.cos(dlambda)) 

	return bearing