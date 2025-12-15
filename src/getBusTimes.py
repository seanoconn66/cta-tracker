import requests
import json
from datetime import datetime
from config import API_KEY_STORE

# Install requests: pip install requests

# Replace "YOUR_API_KEY" with your actual CTA Bus Tracker API key.
API_KEY = API_KEY_STORE
STOP_ID = "11024"# Stop ID for Diversey & Southport EB
#1126
ROUTE = "76"

# -- CORRECTED ENDPOINT FOR V3, HTTPS, and JSON format --
API_URL = f"https://ctabustracker.com/bustime/api/v3/getpredictions?key={API_KEY}&stpid={STOP_ID}&format=json&top=5"

def get_predictions_json_mvp(url):
    """
    Fetches and prints raw bus arrival predictions using the corrected V3 JSON endpoint.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for HTTP errors (404, 500, etc.)
        
        data = response.json()
        
        # CTA API nests everything under a 'bustime-response' key
        bus_time_response = data.get('bustime-response', {})
        
        if 'error' in bus_time_response:
            # Handle API-specific errors (e.g., invalid key, invalid stop)
            error_msg = bus_time_response['error'][0]['msg']
            print(f"API Error: {error_msg}")
            return
            
        predictions = bus_time_response.get('prd', [])

        if not predictions:
            print("No predictions found for this stop/route combination.")
            return

        for prd in predictions:
            # New Line: Parse the API time string into a Python datetime object
            arrival_time_obj = datetime.strptime(prd['prdtm'], "%Y%m%d %H:%M")
            
            # Changed Line: Use .strftime() to format the object into "HH:MM AM/PM"
            formatted_time = arrival_time_obj.strftime("%I:%M %p") 

            print(f"* Dest: {prd['des']} (Vehicle {prd['vid']}), Arrival Time: {formatted_time}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    get_predictions_json_mvp(API_URL)





