import requests
import pandas as pd

def get_rainfall_time_series_data(start_date, end_date, region_coords):
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMDI2NzcyMiwianRpIjoiMDU5NDdmYTItY2MzZi00OTAxLTg0ZDgtNTExN2ExMmI5ZTM4IiwibmJmIjoxNzMwMjY3NzIyLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiWDBHTnNYTm1zWGFlY3AzVDg5MFBKOEdURUxtMSIsImV4cCI6MTczNTQ1MTcyMiwicm9sZXMiOiJ1c2VyIiwidXNlcl9pZCI6IlgwR05zWE5tc1hhZWNwM1Q4OTBQSjhHVEVMbTEifQ.ec5EFyGPI6gmWcT30ctGAlGecJkudQfMhGAvNLwhons"

    url = "https://api.climateengine.org/timeseries/native/points"

    # Construct the coordinates parameter for the request
    coordinates = f"[[{region_coords['longitude']},{region_coords['latitude']}]]"

    params = {
        "dataset": "GRIDMET",
        "variable": "pr",  # Precipitation variable
        "area_reducer": "mean",  # Area reducer
        "start_date": start_date,
        "end_date": end_date,
        "coordinates": coordinates,
    }

    headers = {
        'Authorization': api_key,
        'Accept': 'application/json'
    }

    print("Request URL:", url)
    print("Request Params:", params)
    print("Request Headers:", headers)

    response = requests.get(url, params=params, headers=headers)

    print("Response Status Code:", response.status_code)
    print("Full Response:", response.json())  # Print the full response for debugging

    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.json_normalize(data)
            return df
        else:
            print("No data found in the response.")
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None

# Example usage
#start_date = "2018-01-01"  # Use a date range that you know has data
#end_date = "2018-03-31"
#region_coords = {"latitude": 38.78, "longitude": -121.61}  # Example coordinates from CURL command

#rainfall_data = get_rainfall_time_series_data(start_date, end_date, region_coords)
#if rainfall_data is not None:
#    print(rainfall_data)
#