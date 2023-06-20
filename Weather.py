from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Location Management
locations = []
location_id = 1

class Location:
    def __init__(self, id, city_name, country_code):
        self.id = id
        self.city_name = city_name
        self.country_code = country_code

@app.post("/locations")
async def create_location(city_name: str, country_code: str):
    global location_id
    location = Location(location_id, city_name, country_code)
    locations.append(location)
    location_id += 1
    return location

@app.get("/locations")
async def get_locations():
    return locations

@app.get("/locations/{location_id}")
async def get_location(location_id: int):
    for location in locations:
        if location.id == location_id:
            return location
    raise HTTPException(status_code=404, detail="Location not found")

@app.put("/locations/{location_id}")
async def update_location(location_id: int, city_name: str, country_code: str):
    for location in locations:
        if location.id == location_id:
            location.city_name = city_name
            location.country_code = country_code
            return location
    raise HTTPException(status_code=404, detail="Location not found")

@app.delete("/locations/{location_id}")
async def delete_location(location_id: int):
    for location in locations:
        if location.id == location_id:
            locations.remove(location)
            return
    raise HTTPException(status_code=404, detail="Location not found")

# Weather Forecast
API_KEY = "your_api_key"
API_URL = "http://api.weatherapi.com/v1/current.json"

@app.get("/weather/{location_id}")
async def get_weather(location_id: int):
    for location in locations:
        if location.id == location_id:
            query_params = {
                "key": API_KEY,
                "q": f"{location.city_name},{location.country_code}"
            }
            response = requests.get(API_URL, params=query_params)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Error retrieving weather data")
    raise HTTPException(status_code=404, detail="Location not found")
