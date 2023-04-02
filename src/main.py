import requests

# Set the API endpoint URL
endpoint = "https://api.opentripmap.com/0.1/en/places/radius"

# Set the API key
api_key = "5ae2e3f221c38a28845f05b67fbd6206c69e2f737a4108db90894f98"

# Set the location and radius for the search
location = "New York"
radius = 10000  # in meters

# Set the API parameters
params = {
    "apikey": api_key,
    "radius": radius,
    "limit": 50,
    "kinds": "hotels,hostels",
    "rate": "3,4,5",
    "format": "json",
    "lon": "",
    "lat": "",
}

# Get the latitude and longitude for the location using the OpenTripMap API
geo_endpoint = "https://api.opentripmap.com/0.1/en/places/geoname"
geo_params = {
    "apikey": api_key,
    "name": location,
    "format": "json",
}
geo_response = requests.get(geo_endpoint, params=geo_params).json()
location_lat = geo_response["lat"]
location_lon = geo_response["lon"]

# Set the location coordinates in the API parameters
params["lon"] = location_lon
params["lat"] = location_lat

# Send the API request to get the list of accommodations
response = requests.get(endpoint, params=params).json()

# Sort the accommodations by price
accommodations = sorted(response["features"], key=lambda x: x["properties"]["rate"])

# Print the top low-end, medium, and high-end accommodation options
print("Low-end:")
for i in range(3):
    print(accommodations[i]["properties"]["name"], "($"+str(accommodations[i]["properties"]["price"])+")")

print("\nMedium:")
for i in range(3, 6):
    print(accommodations[i]["properties"]["name"], "($"+str(accommodations[i]["properties"]["price"])+")")

print("\nHigh-end:")
for i in range(6, 9):
    print(accommodations[i]["properties"]["name"], "($"+str(accommodations[i]["properties"]["price"])+")")

# Get the list of tourist spots
tourist_spots = []
for feature in response["features"]:
    if "museum" in feature["properties"]["name"].lower():
        tourist_spots.append(feature["properties"]["name"])

# Print the list of tourist spots
print("\nMust-visit tourist spots:")
for spot in tourist_spots:
    print("- "+spot)
