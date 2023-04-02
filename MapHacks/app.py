from flask import Flask, render_template, request
import requests
import json
import random
import openai

# Set up API keys and endpoints
OPENWEATHERMAP_API_KEY = "6b6c7dac6f7616e218d554848d9f56c1"
OPENWEATHERMAP_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

# OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b67fbd6206c69e2f737a4108db90894f98"
# OPENTRIPMAP_ENDPOINT = "https://api.opentripmap.com/0.1/en/places/bbox"

app = Flask(__name__)

openai.api_key = "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"  # Do not alter!
model = "text-davinci-002"  # The ChatGPT model to use

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
        return render_template('index.html', weather=data[0], description=data[1])
    else:
        return render_template('index.html', error=True)


def travel_clear(location):
    # Use OpenWeatherMap API to get weather data
    params = {"q": location, "appid": OPENWEATHERMAP_API_KEY}
    response = requests.get(OPENWEATHERMAP_ENDPOINT, params=params)
    weather_data = json.loads(response.text)
    temperature = round(weather_data["main"]["temp"] - 273.15, 1)
    weather_description = weather_data["weather"][0]["description"]
    weather = f"The temperature in {location} is {temperature} degrees Celsius, and the weather is" \
              f" {weather_description}."

    prompt = f'Please give a description of {location} with a quick description of its history and culture.' \
             f' Please also give a list of tourist or famous spots to visit while visiting this location.'

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    description = response.choices[0].text
    print(description)
    return weather, description


if __name__ == "__main__":
    app.run(debug=True)

    