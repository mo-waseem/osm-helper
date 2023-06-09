from math import sin, radians, cos, asin, sqrt
from config import Config


# this is the direct distance between two points on earth respecting the circularity of earth
def haversine_distance(
    location_a, location_b
):  # (source_lat, source_lng), (destination_lat, destination_lng)
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
