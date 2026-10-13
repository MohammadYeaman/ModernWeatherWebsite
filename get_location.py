import requests


def get_coordinates(user_input):
  # Default fallback if input is empty or defaults to New York
  cleaned_input = (user_input or "New York").strip().title()

  fallback_locations = {
      "New York": {
          "lat": "40.7128",
          "lon": "-74.0060",
          "display_name": "New York, NY, USA",
      },
  }

  url = "https://nominatim.openstreetmap.org/search"
  params = {"q": cleaned_input, "format": "json", "limit": 1}
  headers = {"User-Agent": "MyGeocodingApp/1.0 (contact@gmail.com)"}

  try:
    response = requests.get(url, params=params, headers=headers, timeout=5)
    if response.status_code == 200:
      data = response.json()
      if data and len(data) > 0:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        display_name = data[0]["display_name"]
        print(f"Found via Nominatim: {display_name} -> Lat: {lat}, Lon: {lon}")
        return lat, lon, display_name
  except Exception as e:
    print(f"Network warning (Nominatim): {e}")

  # Default ultimate fallback
  default = fallback_locations["New York"]
  return default["lat"], default["lon"], default["display_name"]