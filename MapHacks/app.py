from flask import Flask, render_template, request, send_file, jsonify
import requests

# Set up API keys and endpoints
OPENWEATHERMAP_API_KEY = "6b6c7dac6f7616e218d554848d9f56c1"
OPENWEATHERMAP_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b67fbd6206c69e2f737a4108db90894f98"
OPENTRIPMAP_ENDPOINT = "https://api.opentripmap.com/0.1/en/places/bbox"

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # Handle form submission
        location = request.form['text_input'].title()
        data = travel_clear(location)
        return render_template('index.html', data=data)
    else:
        return render_template('index.html')


def travel_clear(location):
    # Use OpenWeatherMap API to get weather data
    params = {"q": location, "appid": OPENWEATHERMAP_API_KEY}
    response = requests.get(OPENWEATHERMAP_ENDPOINT, params=params)
    weather_data = response.json()

    # Use OpenTripMap API to get accommodations data
    headers = {"x-api-key": OPENTRIPMAP_API_KEY}
    response = requests.get(OPENTRIPMAP_ENDPOINT.format(location), headers=headers)
    accommodations_data = response.json()

    # Convert JSON data to strings
    weather_str = jsonify(weather_data)
    accommodations_str = jsonify(accommodations_data)

    # Return the string data
    return {"Weather data": weather_str, "Accommodations data": accommodations_str}


if __name__=="__main__":
    app.run(debug=True)

    