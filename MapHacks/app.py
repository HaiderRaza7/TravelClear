from flask import Flask, render_template, request
import requests
import json
import random
import openai

# Set up API keys and endpoints
OPENWEATHERMAP_API_KEY = "6b6c7dac6f7616e218d554848d9f56c1"
OPENWEATHERMAP_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

openai.api_key = "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"  # For running ChatGPT model
model = "text-davinci-002"  # The ChatGPT model to use

app = Flask(__name__)

# 100 of the most popular tourist attractions. Used to "surprise" the user with a random location
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
    This function is called when the user submits their location input (or if they click the Surprise me button).
    It scrapes the web using open weather map API and utilizes openai API (chatGPT) to get important information about
    the location's weather and popular tourist spots in addition to providing a brief introduction for the location.
    :return: Weather and description about the location which is to be sent to index.html to be displayed to the user.
    """
    if request.method == 'POST':
        if 'submit' in request.form:
            # Handle form submission
            location = request.form['text_input'].title()
        elif 'random' in request.form:
            location = random.choice(cities)
        else:
            return render_template('index.html', error=True)
        description, tourist_spots, weather = travel_clear(location)
        return render_template('index.html', description=description, tourist_spots=tourist_spots, weather=weather)
    else:
        return render_template('index.html', error=True)


def travel_clear(location):
    """
    Extract the information that index() needs to do its job.
    :param location: city that we need to obtain information about.
    :return: Weather, description, and tourist spots about the location.
    """
    # Use OpenWeatherMap API to get weather data
    params = {"q": location, "appid": OPENWEATHERMAP_API_KEY}
    response = requests.get(OPENWEATHERMAP_ENDPOINT, params=params)
    weather_data = json.loads(response.text)
    temperature = round(weather_data["main"]["temp"] - 273.15, 1)
    weather_description = weather_data["weather"][0]["description"]
    weather = f"The temperature in {location} is {temperature} degrees Celsius, and the weather is" \
              f" {weather_description}."

    prompt = f'Please give a description of the location, history, and culture of {location}.' \
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

    prompt = f'Please give a list of tourist spots in {location}, but you must separate them with a comma. ' \
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
    app.run(debug=True)
