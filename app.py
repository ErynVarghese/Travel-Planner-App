from flask import Flask, render_template, request
from services.weather_service import get_weather
from services.amadeus_service import get_flights_and_hotels
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_results', methods=['POST'])
def get_results():
  
    departure = request.form['departure']
    destination = request.form['destination']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # Fetch flights and hotels from API
    flights, hotels = get_flights_and_hotels(departure, destination, start_date, end_date)

    # Fetch weather data from API
    weather = get_weather(destination)

    flights_limited = flights[:5]
    hotels_limited = hotels[:5]

    return render_template('results.html', flights=flights_limited, hotels=hotels_limited, weather=weather)

if __name__ == '__main__':
    app.run(debug=True)