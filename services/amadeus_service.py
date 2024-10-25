# services/amadeus_service.py
import requests
from config import AMADEUS_API_KEY, AMADEUS_API_SECRET

def get_access_token():
    # Obtain access token from Amadeus API
    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    data = {
        'grant_type': 'client_credentials',
        'client_id': AMADEUS_API_KEY,
        'client_secret': AMADEUS_API_SECRET
    }
    
    response = requests.post(token_url, data=data)

    if response.status_code != 200:
         print(f"Error retrieving access token: {response.json()}")

    response.raise_for_status() 
    return response.json().get('access_token')

def get_city_code(city_name):

    access_token = get_access_token()
    city_search_url = f"https://test.api.amadeus.com/v1/reference-data/locations?subType=CITY&keyword={city_name}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(city_search_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data['data']:
           
            return data['data'][0]['iataCode']  # Extract the IATA code
        else:
            print("No city code found.")
            return None
        
    except requests.RequestException as e:
        print(f"Error fetching city code: {e}")
        return None

def get_flights_and_hotels(departure_city, destination_city, start_date, end_date, num_adults=1):
  
    access_token = get_access_token()

    # Get the city code for the destination city
    destination = get_city_code(destination_city)
    if not destination:
        print("Destination city code could not be found.")
        return [], [] 
    
     # Get the city code for the departure city
    departure = get_city_code(departure_city)
    if not departure:
        print("Destination city code could not be found.")
        return [], [] 
    
    
     
    flight_url = f'https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={departure}&destinationLocationCode={destination}&departureDate={start_date}&returnDate={end_date}&adults={num_adults}&max=5'
    
    hotel_url = f'https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city?cityCode={destination}&radiusUnit=KM&hotelSource=ALL'
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
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
