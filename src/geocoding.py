import requests
from typing import Tuple

def address_to_coordinates(address: str) -> Tuple[float, float, str]:
    """
    Uses Nominatim (OpenStreetMap API gratuita) to translate an address
    like 'Torre Eiffel, París' to latitude and longitude.
    """
    if not address or not address.strip():
        raise ValueError("The address cannot be empty.")

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    # OpenStreetMap requires a User-Agent identified to avoid being blocked
    headers = {"User-Agent": "GeoHistoryApp/1.0"}

    response = requests.get(url, params=params, headers=headers, timeout=5)
    
    if response.status_code != 200:
        raise RuntimeError("Error connecting to the geolocation service.")

    data = response.json()
    if not data:
        raise ValueError(f"No coordinates found for the address: '{address}'")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    display_name = data[0]["display_name"]

    return lat, lon, display_name