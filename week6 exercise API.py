import requests
import json
from geopy.geocoders import Nominatim

#Enter city name
city_name = input("Please enter a city name: ")

#Convert city name to coordinates
geolocator = Nominatim(user_agent="smart_cat_app")
location = geolocator.geocode(city_name)

if location is None:
    print("Sorry, we coud not find the city, please check the spelling.")
    exit()

latitude = location.latitude
longitude = location.longitude
print(f"Coordinates for {city_name}: Latitude: {latitude}, Longitude:{longitude}")

#request weather data from Open-Meteo API
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": "temperature_2m,precipitation",
    "timezone": "auto"
}

response = requests.get(url, params=params)

if response.status_code !=200:
    print("Request failed, status code:", response.status_code)
    exit()
else:
    data = response.json()
    print("Successfully fetched weather data")

#Generate cat care suggestion
hourly_temp = data["hourly"]["temperature_2m"]
hourly_precip = data["hourly"]["precipitation"]

print("\nCat Care Suggestion(next 24 hours):")
for i in range(24):
    temp = hourly_temp[i]
    rain = hourly_precip[i]
    advice = ""
    if temp < 10:
        advice = "Cold weather, keep your cat warm!"
    elif temp >30:
        advice = "Hot weather, ensure your cat has water and shade!"
    if rain > 0:
        advice += " It may rain, limit ourdoor activity."
    print(f"Hour{i}: Temp{temp}°F, Precip{rain}mm, {advice}")





