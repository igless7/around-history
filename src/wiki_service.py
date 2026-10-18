import requests
from typing import List, Dict, Any
from src.validator import calculate_haversine_distance

def fetch_nearby_history(lat: float, lon: float, radius_km: float) -> List[Dict[str, Any]]:
    """
    Consults the official Wikipedia GeoSearch API to fetch pages with coordinates
    near the submitted location.
    """
    url = "https://en.wikipedia.org/w/api.php"
    
    # Convert kilometers to meters that is what the Wikipedia API requires
    radius_meters = int(radius_km * 1000)

    params = {
        "action": "query",
        "list": "geosearch",
        "gscoord": f"{lat}|{lon}",
        "gsradius": radius_meters,
        "gslimit": 10,  # Fetch up to 10 places
        "format": "json"
    }
    headers = {"User-Agent": "GeoHistoryApp/1.0"}

    response = requests.get(url, params=params, headers=headers, timeout=5)
    if response.status_code != 200:
        raise RuntimeError("Error connecting to the Wikipedia server.")

    data = response.json()
    search_results = data.get("query", {}).get("geosearch", [])

    history_places = []
    for item in search_results:
        place_lat = item["lat"]
        place_lon = item["lon"]
        
        # Re calculate the exact distance with our own tested function
        dist = calculate_haversine_distance(lat, lon, place_lat, place_lon)
        page_id = item["pageid"]

        history_places.append({
            "pageid": page_id,
            "title": item["title"],
            "lat": place_lat,
            "lon": place_lon,
            "distance_km": dist,
            "url": f"https://en.wikipedia.org/?curid={page_id}"
        })

    # OOrder from closest to farthest
    history_places.sort(key=lambda x: x["distance_km"])
    return history_places