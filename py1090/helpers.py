import math

EARTH_RADIUS = 6371008.7714 # m
r"""The average earth radius :math:`R_0`. It is defined as the mean radius of the semi-axes.
The values are taken from the WGS 84 (World Geodetic System 1984) ellipsoid
`(definition of the Department Of Defense, Jan. 2000, p. 37) <http://earth-info.nga.mil/GandG/publications/tr8350.2/wgs84fin.pdf>`_ .

.. math::

	R_0 = 6371008.7714 \mathrm{m}

"""

def distance_between(lat1, lon1, lat2, lon2):
	r"""Calculates the distance between two locations, in meters, using the `Haversine <http://en.wikipedia.org/wiki/Haversine_formula>`_
	formula.

	The bearing between latitude, longitude: :math:`(\phi_1, \lambda_1)` and :math:`(\phi_2, \lambda_2)` is given by

	.. math::

		a = \sin^2(\frac{\phi_2 - \phi_1}{2}) + \cos(\phi_1) \cos(\phi_2) \sin^2(\frac{\lambda_2 - \lambda_1}{2})

		d = 2 R_0 \cdot \mathrm{atan2}(\sqrt{a}, \sqrt{1-a})

	The earth radius :math:`R_0` is taken to be :py:data:`py1090.helpers.EARTH_RADIUS`. The approximation of a spherical earth is made.

	Args:
		lat1 (float): :math:`\phi_1`, the latitude of the reference location
		lon1 (float): :math:`\lambda_1`, the longitude of the reference location
		lat2 (float): :math:`\phi_2`, the latitude of the target location
		lon2 (float): :math:`\lambda_2`, the longitude of the target location

	Returns:
		float: the distance in meters.

	"""
	lambda1 = math.radians(lon1)
	lambda2 = math.radians(lon2)

	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)

	dphi = phi2-phi1
	dlambda = lambda2-lambda1

	a = math.pow(math.sin(dphi/2), 2) + math.cos(phi1)*math.cos(phi2)*math.pow(math.sin(dlambda/2), 2)
	dsigma = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

	distance = EARTH_RADIUS * dsigma

	return distance

def bearing_between(lat1, lon1, lat2, lon2):
	r"""Calculates the bearing angle between two locations, in radians.

	The bearing between latitude, longitude: :math:`(\phi_1, \lambda_1)` and :math:`(\phi_2, \lambda_2)` is given by

	.. math::

		\mathrm{atan2}(\sin(\lambda_2 - \lambda_1) \cos(\phi_1), \cos(\phi_2) \sin(\phi_1) - \sin(\phi_2) \cos(\phi_2) \cos(\lambda_2 - \lambda_1))

	Args:
		lat1 (float): :math:`\phi_1`, the latitude of the reference location
		lon1 (float): :math:`\lambda_1`, the longitude of the reference location
		lat2 (float): :math:`\phi_2`, the latitude of the target location
		lon2 (float): :math:`\lambda_2`, the longitude of the target location

	Returns:
		float: the bearing angle in radians, between :math:`-\pi` and :math:`\pi`.

	"""
	lambda1 = math.radians(lon1)
	lambda2 = math.radians(lon2)

	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)

	dphi = phi2-phi1
	dlambda = lambda2-lambda1

	bearing = math.atan2(math.sin(dlambda)*math.cos(phi1), \
		math.cos(phi2)*math.sin(phi1)-math.sin(phi2)*math.cos(phi1)*math.cos(dlambda))

	return bearing


def knots_to_kmh(knots):
	"""Converts velocity in knots to velocity in km/h.

	1 knot is 1 nm/h (nautical mile per hour) and 1.852 km/h.

	Args:
		knots (float): velocity in knots

	Returns:
		float: velocity in km/h

	"""
	return 1.852*knots

def knots_to_mps(knots):
	"""Converts velocity in knots to velocity in m/s (meters per second).

	1 knot is 1 nm/h (nautical mile per hour), 1.852 km/h and about 6.67 m/s.

	Args:
		knots (float): velocity in knots

	Returns:
		float: velocity in m/s

	"""
	kmh = knots_to_kmh(knots)
	return 3.6*kmh
