# created by Thinh Vo on 4/6/2024
import json
import requests
import os
import sys
from datetime import datetime, timedelta
from collections import Counter
from uszipcode import SearchEngine
import weather_functions 

# Define constants:
today = datetime.now().strftime('%Y-%m-%d')
current_location = os.path.dirname(os.path.abspath(sys.argv[0]))
report_list = []

# connecting this program to its function
if current_location not in sys.path:
    sys.path.append(current_location)

# report location and list for weather forecast
report_folder = f'{current_location}/API report/'
report_location = f'{report_folder}/{today} report.txt'
report_list = []

# data source from api
temp_url = 'https://api.weather.gov/gridpoints/OUN/35,97/forecast'
precipitation_url = 'https://api.weather.gov/gridpoints/OUN/35,97'


# loop to prevent disconnection from script to api and grabbing weather data
max_attempt = 10
attempt = 0 
while attempt < max_attempt:
    POPSresponse = requests.get(precipitation_url) 
    forcastResponse = requests.get(temp_url) 

    if POPSresponse.status_code == 200 and forcastResponse.status_code == 200:
        POPSdata = POPSresponse.json()
        forcastData = forcastResponse.json()
        searchStartWeather = forcastData['properties']['periods']

        # grabbing weather data
        max_temp, avg_temp, min_temp, max_dewP, avg_dewP, min_dewP, max_humid, avg_humid, min_humid, max_windS, avg_windS, min_windS, actualPrecipitation, snowAmount, forcast = weather_functions.get_weather(searchStartWeather, POPSdata)
        report_list.insert(0, 'Successfull data retrival\n')
        break
    elif POPSresponse.status_code == 304 or forcastResponse.status_code == 304:
        report_list.insert(0, 'Resource not modified, use cached data\n')
        break  
    else:
        # Handle other status codes appropriately
        print(f"Error: {POPSresponse.status_code + ' ' + forcastResponse.status_code}. Retrying...")
        attempt += 1
        continue 
if attempt > max_attempt:
    report_list.insert(0, 'Maximum number of attempts reached. Failed to retrieve data.\n')

# upload data to database

# report_list.extend(weather_functions.database_upload( 'username', 'password', 'hostname', 'database_name', max_temp, avg_temp, min_temp, max_dewP, 
#                             avg_dewP, min_dewP, max_humid, avg_humid, 
#                             min_humid, max_windS, avg_windS, min_windS, 
#                             actualPrecipitation, snowAmount, forcast))


# making folder for api report
if not os.path.exists(report_folder):
    os.makedirs(report_folder)

with open(report_location, 'w') as file:
    file.write(today + " report: \n")
    for report in range(0, len(report_list)):
        file.write(report_list[report])

# printout today's forecast comment out the values that you don't want in your report with #   
forecast_location = f'{current_location}/{today} forecast.txt'
with open(forecast_location, 'w') as file:
    file.write(today + " forecast: \n")
    file.write(f'Max Temperature: {max_temp} \n')
    file.write(f'Avg Temperature: {avg_temp} \n')
    file.write(f'Min Temperature: {min_temp} \n')
    file.write(f'Max Dew Point: {max_dewP } \n')
    file.write(f'Avg Dew Point: {avg_dewP} \n')
    file.write(f'Min Dew Point: {min_dewP } \n')    
    file.write(f'Max Humidity: {max_humid} \n')
    file.write(f'Avg Humidity: {avg_humid} \n')
    file.write(f'Min Humidity: {min_humid} \n')
    file.write(f'Max wind speed: {max_windS} \n')
    file.write(f'Avg wind speed: {avg_windS} \n')
    file.write(f'Min wind speed: {min_windS} \n')
    file.write(f'precipitation: {actualPrecipitation} \n')
    file.write(f'snow amount: {snowAmount} \n')
    file.write(f'Forecast: {forcast} \n')    



