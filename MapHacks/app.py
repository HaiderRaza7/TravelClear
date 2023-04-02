from flask import Flask, render_template, request
import requests
import json
import random

# Set up API keys and endpoints
OPENWEATHERMAP_API_KEY = "6b6c7dac6f7616e218d554848d9f56c1"
OPENWEATHERMAP_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

# OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b67fbd6206c69e2f737a4108db90894f98"
# OPENTRIPMAP_ENDPOINT = "https://api.opentripmap.com/0.1/en/places/bbox"

app = Flask(__name__)

cities = ['Paris', 'New York City', 'Rome', 'London', 'Dubai', 'Barcelona', 'Bangkok', 'Singapore', 'Istanbul',
          'Tokyo', 'Hong Kong', 'Amsterdam', 'Vienna', 'Prague', 'Los Angeles', 'Marrakesh', 'Shanghai', 'Berlin',
          'Madrid', 'Miami', 'Sydney', 'Florence', 'Buenos Aires', 'Toronto', 'San Francisco', 'Las Vegas',
          'Rio de Janeiro', 'Mexico City', 'Cape Town', 'Dublin', 'Edinburgh', 'Vancouver', 'Stockholm', 'Brussels',
          'Munich', 'Budapest', 'Copenhagen', 'Krakow', 'Lisbon', 'Zurich', 'Athens', 'Honolulu', 'Hanoi', 'San Diego',
          'Osaka', 'Washington D.C.', 'Seoul', 'St. Petersburg', 'Dubrovnik', 'Venice', 'Montreal', 'Jerusalem',
          'Kyoto', 'Sao Paulo', 'Beijing', 'Nairobi', 'Hamburg', 'Naples', 'Abu Dhabi', 'Cairo', 'Cartagena',
          'Seville', 'Cusco', 'Jakarta', 'Salzburg', 'Stavanger', 'Bordeaux', 'Cologne', 'Queenstown', 'Reykjavik',
          'Kruger National Park', 'Valletta', 'Cannes', 'Santiago', 'Melbourne', 'Santorini', 'Split', 'Oslo',
          'Marseille', 'Auckland', 'Lucerne', 'Geneva', 'Granada', 'Bologna', 'Brisbane', 'Tallinn', 'Krakow',
          'Munich', 'San Sebastian', 'Bruges', 'Pula', 'Siem Reap', 'Zanzibar', 'Helsinki', 'Plovdiv', 'La Paz',
          'Beirut', 'Lviv', 'Quebec City', 'Baku', 'Minsk']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'submit' in request.form:
            # Handle form submission
            location = request.form['text_input'].title()
        elif 'random' in request.form:
            location = random.choice(cities)
        else:
            return render_template('index.html', error=True)
        data = travel_clear(location)
        return render_template('index.html', data=data)
    else:
        return render_template('index.html', error=True)


def travel_clear(location):
    # Use OpenWeatherMap API to get weather data
    params = {"q": location, "appid": OPENWEATHERMAP_API_KEY}
    response = requests.get(OPENWEATHERMAP_ENDPOINT, params=params)
    weather_data = json.loads(response.text)
    temperature = round(weather_data["main"]["temp"] - 273.15, 1)
    weather_description = weather_data["weather"][0]["description"]
    weather_str = f"The temperature in {location} is {temperature} degrees Celsius, and the weather is" \
                  f" {weather_description}."

    # # Use OpenTripMap API to get accommodations data
    # params = {"apikey": OPENTRIPMAP_API_KEY, "bbox": get_bbox(location)}
    # response = requests.get(OPENTRIPMAP_ENDPOINT, params=params)
    # accommodations_data = response.json()
    # # Iterate through the accommodations data and extract relevant information
    # accommodations_list = accommodations_data.get("accommodations", [])
    # print(accommodations_list)
    # accommodations_info = []
    # for accommodation in accommodations_list:
    #     name = accommodation.get("name", "Unknown")
    #     address = accommodation.get("address", "Unknown")
    #     rating = accommodation.get("rate", {}).get("rating", "Unknown")
    #     accommodations_info.append(f"{name} - {address}, Rating: {rating}")

    # # Convert the accommodations information into a readable string format
    # accommodations_info = "\n".join(accommodations_info)
    # accommodations_str = f"Accommodations in {location}:\n{accommodations_info}"
    accommodations_str = "you should see something about accommodations here"
    # Return the string data
    return {"Weather data": weather_str, "Accommodations data": accommodations_str}


# def get_bbox(location):
#     # Use Nominatim API to get coordinates of the location
#     nominatim_endpoint = "https://nominatim.openstreetmap.org/search"
#     params = {"q": location, "format": "json"}
#     response = requests.get(nominatim_endpoint, params=params)
#     data = response.json()
#     lat = data[0]["lat"]
#     lon = data[0]["lon"]
#     # Calculate the bounding box
#     bbox = f"{float(lon)-0.5},{float(lat)-0.5},{float(lon)+0.5},{float(lat)+0.5}"
#     return bbox


if __name__ == "__main__":
    app.run(debug=True)

    