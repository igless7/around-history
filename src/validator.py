import math
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Coordinates:
    latitude: float
    longitude: float

def validate_coordinates(lat: float, lon: float) -> Coordinates:
    """
    Ensures that the coordinates lie within the physical boundaries of the Earth.
    """
    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (ValueError, TypeError):
        raise ValueError("The coordinates must be valid numbers.")

    if not (-90.0 <= lat_f <= 90.0):
        raise ValueError(f"Invalid latitude: {lat_f}. Must be between -90 and 90.")
    if not (-180.0 <= lon_f <= 180.0):
        raise ValueError(f"Invalid longitude: {lon_f}. Must be between -180 and 180.")

    return Coordinates(latitude=lat_f, longitude=lon_f)

def validate_radius(radius_km: float) -> float:
    """Ensures that the search radius is within the valid range of 0.1 km to 50 km."""
    try:
        r = float(radius_km)
    except (ValueError, TypeError):
        raise ValueError("The radius must be a valid number.")


    if r <= 0 or r > 50:
        raise ValueError("The radius must be greater than 0 and at most 50 km.")
    return r

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Haversine formula: Calculates the great circle distance in kilometers between two points
    on the Earth's surface.
    """
    R = 6371.0  # Average radius of the Earth in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return round(R * c, 2)