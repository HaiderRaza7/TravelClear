import sys

from flask import Flask, render_template, request
import requests
import json
import random
import openai
import time

# Set up API keys and endpoints
OPENWEATHERMAP_API_KEY = "6b6c7dac6f7616e218d554848d9f56c1"
OPENWEATHERMAP_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

openai.api_key = "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"  # For running ChatGPT model
model = "text-davinci-002"  # The ChatGPT model to use

app = Flask(__name__)

# 100 of the most popular tourist attractions. Used to "surprise" the user with a random city
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
    """
    This function is called when the user submits their city input (or if they click the Surprise me button).
    It scrapes the web using open weather map API and utilizes openai API (chatGPT) to get important information about
    the city's weather and popular tourist spots in addition to providing a brief introduction for the city.
    :return: Weather and description about the city which is to be sent to index.html to be displayed to the user.
    """
    if request.method == 'POST':
        if 'submit' in request.form:
            # Handle form submission
            city = request.form['text_input'].title()
        elif 'random' in request.form:
            city = random.choice(cities)
        else:
            return render_template('index.html', error=True)
        description, tourist_spots, weather = travel_clear(city)
        return render_template('index.html', description=description, tourist_spots=tourist_spots, weather=weather)
    else:
        return render_template('index.html', error=True)


def travel_clear(city):
    """
    Extract the information that index() needs to do its job.
    :param city: city that we need to obtain information about.
    :return: Weather, description, and tourist spots about the city.
    """
    # Use OpenWeatherMap API to get weather data
    time.sleep(30)
    params = {"q": city, "appid": OPENWEATHERMAP_API_KEY}
    response = requests.get(OPENWEATHERMAP_ENDPOINT, params=params)
    weather_data = json.loads(response.text)
    temperature = round(weather_data["main"]["temp"] - 273.15, 1)
    weather_description = weather_data["weather"][0]["description"]
    weather = f"The current temperature in {city} is {temperature} degrees Celsius, and the current weather is" \
              f" {weather_description}."

    prompt = f'Please give a description of the location, history, and culture of {city}.' \
             f'You must complete sentences that you start.'

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    description = response.choices[0].text
    description = description[:description.rindex('.') + 1]

    prompt = f'Please give a list of tourist spots in {city}, but you must separate them with a comma. ' \
             f'For example, if you would like to list 3 locations called A, B, and C then please output them ' \
             f'exactly in this format: A,B,C.' \
             f'You may list as many as you like as long as they are worth visiting.'

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    tourist_spots = response.choices[0].text.split(",")
    for i in range(len(tourist_spots)):
        tourist_spots[i] = tourist_spots[i].strip()

    return description, tourist_spots, weather


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Correct usage: openai API key should be the one and only argument")
        exit(1)
    openai.api_key = sys.argv[1]
    app.run(debug=True)
