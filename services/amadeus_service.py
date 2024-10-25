# services/amadeus_service.py
import requests
from config import AMADEUS_API_KEY

def get_flights_and_hotels(departure, destination, start_date, end_date):
    
    flight_url = f'https://test.api.amadeus.com/v1/shopping/flight-offers?origin={departure}&destination={destination}&departureDate={start_date}&returnDate={end_date}'
    hotel_url = f'https://test.api.amadeus.com/v1/shopping/hotel-offers?cityCode={destination}&checkInDate={start_date}&checkOutDate={end_date}'
    
    headers = {"Authorization": f"Bearer {AMADEUS_API_KEY}"}
    
    # Request flight data
    try:
        flight_response = requests.get(flight_url, headers=headers)
        flight_response.raise_for_status()
        flights = flight_response.json().get('data', [])

    except requests.RequestException as e:
        print(f"Error fetching flights: {e}")
        flights = []

    # Request hotel data
    try:
        hotel_response = requests.get(hotel_url, headers=headers)
        hotel_response.raise_for_status()
        hotels = hotel_response.json().get('data', [])

    except requests.RequestException as e:
        print(f"Error fetching hotels: {e}")
        hotels = []

    return flights, hotels