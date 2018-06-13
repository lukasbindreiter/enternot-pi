from math import sin, cos, sqrt, atan2, radians


def calculate_distance(lon1: float, lat1: float, lon2: float,
                       lat2: float) -> float:
    """
    Calculate the distance in meters between the two given geo locations.

    Args:
        lon1: Longitude from -180 to 180
        lat1: Latitude from -90 to 90
        lon2: Longitude from -180 to 180
        lat2: Latitude from -90 to 90

    Returns:
        Distance in meters

    """
    earth_radius = 6_371_000  # meters

    delta_lon = radians(lon2 - lon1)
    delta_lat = radians(lat2 - lat1)

    a = sin(delta_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(
        delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = earth_radius * c
    return distance
