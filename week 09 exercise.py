import numpy as np
import requests
from geopy.geocoders import Nominatim
import sys

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
    "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean",
    "timezone": "auto"
}

response = requests.get(url, params=params)

if response.status_code !=200:
    print("Request failed, status code:", response.status_code)
    exit()
else:
    data = response.json()
    print("Successfully fetched weather data")

#Calculate the mean temperature
daily_mean = np.array(data['daily']['temperature_2m_mean'])

# Convert the temperatures from Celsius to Fahrenheit and Count days with temperatures above 20°C.
max_temp = np.max(daily_mean)
min_temp = np.min(daily_mean)
overall_mean = np.mean(daily_mean)
daily_fahrenheit = daily_mean * 9/5 + 32
days_above_20 = np.sum(daily_mean > 20)

#print results
print("\n--- Weather Analysis for", city_name, "---")
print("Daily mean temperatures (°C):", daily_mean)
print("Daily mean temperatures (°F):", daily_fahrenheit)
print("Highest daily mean temperature (°C):", max_temp)
print("Lowest daily mean temperature (°C):", min_temp)
print("Overall mean temperature (°C):", overall_mean)
print("Number of days above 20°C:", days_above_20)