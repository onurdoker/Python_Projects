"""
Title: Simple Weather Portal

Subject: Using external APIs and handling JSON data

Requirements:
- Create a web form that accepts user input for a city name.
- Send a GET request to external weather API using requests
- Parse the received JSON data (extract temperature, description( and display it on the screen using Jinja2
- Handle and manage 404 errors returned by the API (e.g., city not found)
"""

from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        access_key = "04eccfd0993ddf9885e24d473ff1875e"

        response = requests.get(f'http://api.weatherstack.com/current?access_key={access_key}&query={city}')
        if response.status_code == 400:
            error_message = 'City not found. Please try again.'
            return render_template('index.html', error=error_message)
        elif response.status_code != 200:
            error_message = 'There is an error occurred. Please try again. '
            return render_template('index.html', error=error_message)
        else:
            data = response.json()
            temperature = data['current']['temperature']
            weather_description = data['current']['weather_descriptions'][0]
            return render_template('index.html', city=city, temperature=temperature, weather_description=weather_description)

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
