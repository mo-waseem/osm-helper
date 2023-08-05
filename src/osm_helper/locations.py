import random

from math import sin, radians, cos, asin, sqrt
from utils.type_hints import Location, LocationArray


# this is the direct distance between two points 
# on earth respecting the circularity of earth
def haversine_distance(
    location_a: Location, location_b: Location
) -> float:  # (source_lat, source_lng), (destination_lat, destination_lng)
    def hav(angle):
        return sin(angle / 2) ** 2

    # we convert from decimal degree to radians
    lat_a, lon_a, lat_b, lon_b = (
        radians(location_a[0]),
        radians(location_a[1]),
        radians(location_b[0]),
        radians(location_b[1]),
    )

    delta_lat = lat_b - lat_a
    delta_lon = lon_b - lon_a
    a = hav(delta_lat) + cos(lat_a) * cos(lat_b) * hav(delta_lon)
    c = 2 * asin(sqrt(a))
    # approximate radius of the Earth: 6371 km
    return c * 6371


def generate_random_locations(
    location: Location, number: int = 10, ratio: float = 50
) -> LocationArray:
    """
    Generate random locations:
        Parameters:
            - location: A tuple of str, it's a base location.
            - number: The number of needed random locations.
            - ratio: This decide how much the locations are far or close from 
            each others, higher ratio --> locations are closer.
        Returns:
            - locations: List of locations. 
    """
    return [
        (
            str(float(location[0]) + (random.random() / ratio)),
            str(float(location[1]) + (random.random() / ratio)),
        )
        for _ in range(number)
    ]
