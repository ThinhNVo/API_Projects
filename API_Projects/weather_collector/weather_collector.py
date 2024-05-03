# created by Thinh Vo on 4/6/2024
import json
import requests
import os
import sys
from datetime import datetime, timedelta
from collections import Counter
import weather_functions 

# Define constants:
today = datetime.now().strftime('%Y-%m-%d')
current_location = os.path.dirname(os.path.abspath(sys.argv[0]))
report_list = []
max_attempt = 10
attempt = 0 
zipcode = "45236"

# connecting this program to its function
if current_location not in sys.path:
    sys.path.append(current_location)

def fetch_weather_data(zipcode, MAX_ATTEMPT):
    global report_list

    # loop to prevent disconnection from script to api and grabbing weather data
    for attempt in range(MAX_ATTEMPT):
        # data source from api
        temp_url, precipitation_url, city, state = weather_functions.getCityLink(zipcode, MAX_ATTEMPT)
        
        # if zipcode exists but invalid
        if temp_url == None:
            return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None 

        # if zipcode exists
        POPSresponse = requests.get(precipitation_url) 
        forcastResponse = requests.get(temp_url) 
        if POPSresponse.status_code == 200 and forcastResponse.status_code == 200:
            POPSdata = POPSresponse.json()
            forcastData = forcastResponse.json()
            searchStartWeather = forcastData['properties']['periods']

            # grabbing weather data
            report_list.append('Successfull data retrival\n')
            max_temp, avg_temp, min_temp, max_dewP, avg_dewP, min_dewP, max_humid, avg_humid, min_humid, max_windS, avg_windS, min_windS, actualPrecipitation, snowAmount, forcast = weather_functions.get_weather(searchStartWeather, POPSdata)
 
            # upload data to database
            # report_list.extend(weather_functions.database_upload( 'username', 'password', 'hostname', 'database_name', max_temp, avg_temp, min_temp, max_dewP, 
            #                             avg_dewP, min_dewP, max_humid, avg_humid, 
            #                             min_humid, max_windS, avg_windS, min_windS, 
            #                             actualPrecipitation, snowAmount, forcast))
            
            return max_temp, avg_temp, min_temp, max_dewP, avg_dewP, min_dewP, max_humid, avg_humid, min_humid, max_windS, avg_windS, min_windS, actualPrecipitation, snowAmount, forcast, city, state
        elif POPSresponse.status_code == 304 or forcastResponse.status_code == 304:
            report_list.append('Resource not modified, use cached data\n')
            return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None  
        else:
            # Handle other status codes appropriately
            report_list.append(f"Error: {POPSresponse.status_code + ' ' + forcastResponse.status_code}. Retrying...")
            attempt += 1
            continue 
    report_list.append('Maximum number of attempts reached. Failed to retrieve data.\n')
    return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        

def run_application(zipcode, choice):
    global max_attempt
    global current_location
    global today

    # calling the fetch_weather_data function
    max_temp, avg_temp, min_temp, max_dewP, avg_dewP, min_dewP, max_humid, avg_humid, min_humid, max_windS, avg_windS, min_windS, actualPrecipitation, snowAmount, forcast, city, state = fetch_weather_data(zipcode, max_attempt)

    # report location and list for weather forecast
    report_folder = f'{current_location}/API report/'
    report_location = f'{report_folder}/{today} report.txt'

    # making folder for api report
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    # write report of api calling
    with open(report_location, 'w') as file:
        file.write(today + " report: \n")
        for item in report_list:
            file.write(item)

    # printout today's forecast comment out the values that you don't want in your report with # 
    forecast_location = f'{current_location}/{today} forecast.txt'
    if max_temp == None:
        return None
    elif choice == 'f':
        with open(forecast_location, 'w') as file:
            file.write(today + f"'s forecast in {city}, {state}: \n")
            file.write(f'Max Temperature: {max_temp} F \n')
            file.write(f'Avg Temperature: {avg_temp} F \n')
            file.write(f'Min Temperature: {min_temp} F \n')
            file.write(f'Max Dew Point: {max_dewP} F \n')
            file.write(f'Avg Dew Point: {avg_dewP} F \n')
            file.write(f'Min Dew Point: {min_dewP } F \n')    
            file.write(f'Max Humidity: {max_humid}% \n')
            file.write(f'Avg Humidity: {avg_humid}% \n')
            file.write(f'Min Humidity: {min_humid}% \n')
            file.write(f'Max wind speed: {max_windS} m/hr \n')
            file.write(f'Avg wind speed: {avg_windS} m/hr \n')
            file.write(f'Min wind speed: {min_windS} m/hr \n')
            file.write(f'precipitation: {actualPrecipitation} inch \n')
            file.write(f'snow amount: {snowAmount} mm\n')
            file.write(f'Forecast: {forcast} \n')
    elif choice == 'c':
        with open(forecast_location, 'w') as file:
            file.write(today + f"'s forecast in {city}, {state}: \n")
            file.write(f'Max Temperature: {round((max_temp - 32) * 5/9)} C \n')
            file.write(f'Avg Temperature: {round((avg_temp - 32) * 5/9)} C \n')
            file.write(f'Min Temperature: {round((min_temp - 32) * 5/9)} C \n')
            file.write(f'Max Dew Point: {round((max_dewP - 32) * 5/9)} C \n')
            file.write(f'Avg Dew Point: {round((avg_dewP - 32) * 5/9)} C \n')
            file.write(f'Min Dew Point: {round((min_dewP - 32) * 5/9)} C \n')    
            file.write(f'Max Humidity: {max_humid}% \n')
            file.write(f'Avg Humidity: {avg_humid}% \n')
            file.write(f'Min Humidity: {min_humid}% \n')
            file.write(f'Max wind speed: {max_windS} m/hr \n')
            file.write(f'Avg wind speed: {avg_windS} m/hr \n')
            file.write(f'Min wind speed: {min_windS} m/hr \n')
            file.write(f'precipitation: {actualPrecipitation} inch \n')
            file.write(f'snow amount: {snowAmount} mm\n')
            file.write(f'Forecast: {forcast} \n')

def main():
    global zipcode

    # Ask the user to enter a zipcode and choice for celsius or fahrenheit
    print('Enter your zipcode:')
    zipcode = str(input()).strip()
    while not (zipcode.isdigit() and len(zipcode) == 5):
        zipcode = input("Please enter a 5-digit zipcode: ")

    print('Enter C for celsius or F for fahrenheit')
    choice = input().strip().lower()
    while choice not in ['c', 'f']:
        choice = input("Please enter c or f: ").strip().lower()
    # start the program
    run_application(zipcode, choice)

if __name__ == "__main__":
    main()

