from flask import Flask
import requests

# Set up API keys and endpoints
OPENWEATHERMAP_API_KEY = "6b6c7dac6f7616e218d554848d9f56c1"
OPENWEATHERMAP_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

TRIPADVISOR_API_KEY = "apify_api_fQIKIcGbnWKzOQI27corBbs2k1gGmp3YKKvk"
TRIPADVISOR_ENDPOINT = "https://api.tripadvisor.com/api/partner/2.0/location/{}/attractions"

OPENAQ_ENDPOINT = "https://api.openaq.org/v1/latest"




@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # Handle form submission
        symbol = request.form['text_input'].upper()

<form method="POST">
      <label for="text_input">Enter a stock ticker symbol:</label>
      <input type="text" name="text_input" id="text_input">
      <button type="submit">Submit</button>
    </form>

def TravelClear():

    # Set up the location you want to query
    location = "New York"

    # Use OpenWeatherMap API to get weather data
    params = {"q": location, "appid": OPENWEATHERMAP_API_KEY}
    response = requests.get(OPENWEATHERMAP_ENDPOINT, params=params)
    weather_data = response.json()

    # Use TripAdvisor API to get tourist attractions and hotel/living cost
    params = {"location_id": "g60763", "limit": "10"} # "g60763" is TripAdvisor's location ID for New York City
    headers = {"x-api-key": TRIPADVISOR_API_KEY}
    response = requests.get(TRIPADVISOR_ENDPOINT.format(location), params=params, headers=headers)
    attractions_data = response.json()

    # Use OpenAQ API to get air pollution metrics
    params = {"country": "US", "city": "New York"}
    response = requests.get(OPENAQ_ENDPOINT, params=params)
    air_data = response.json()

    # Print the results
    print("Weather data:", weather_data)
    print("Tourist attractions and hotel/living cost data:", attractions_data)
    print("Air pollution data:", air_data)
    return "hello flask"







if __name__=="__main__":
    app.run()