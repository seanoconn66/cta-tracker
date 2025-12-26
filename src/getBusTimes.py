import requests
import json
from datetime import datetime
from config import API_KEY_STORE

API_KEY = API_KEY_STORE
STOP_ID = "11024"
ROUTE = "76"

API_URL = f"https://ctabustracker.com/bustime/api/v3/getpredictions?key={API_KEY}&stpid={STOP_ID}&format=json&top=5"

def get_predictions(url=API_URL):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        bus_time_response = data.get('bustime-response', {})
        
        if 'error' in bus_time_response:
            return {"error": bus_time_response['error'][0]['msg']}
            
        predictions = bus_time_response.get('prd', [])

        if not predictions:
            return []

        results = []

        for prd in predictions:
            arrival_time_obj = datetime.strptime(prd['prdtm'], "%Y%m%d %H:%M")
            now = datetime.now()

            minutes_until = int((arrival_time_obj - now).total_seconds() // 60)
            minutes_until = max(minutes_until, 0)

            results.append({
                "destination": prd['des'],
                "vehicle": prd['vid'],
                "minutes": f"{minutes_until} minutes"
        })

        print(results)
        return results

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except json.JSONDecodeError:
        return {"error": "JSON decode failed"}
