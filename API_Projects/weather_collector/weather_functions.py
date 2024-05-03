import requests
import os
import sys
import re
import psycopg2 
from datetime import datetime, timedelta
from collections import Counter
from psycopg2 import Error
from uszipcode import SearchEngine

# GLOBAL VARIABLES
search = SearchEngine()
report_list = []
attempt = 0 

# get today date:
today = datetime.now().strftime('%Y-%m-%d')

# identify wind speed in a string
pattern = r'\d+'

# get user's lattitude and longitude then convert to link for noa api
def getCityLink(zipcode, MAX_ATTEMPT):
    global attempt

    # get lat and long from user's zipcode and predict if zipcode is invalid
    try: 
        zipcode_info = search.by_zipcode(zipcode)
        lat = zipcode_info.lat
        lng = zipcode_info.lng
        city = zipcode_info.major_city
        state = zipcode_info.state
        search.close()
    except Exception as e:
        print("Zipcode doesn't exists or not in forecast zone")
        search.close()
        return None, None, None, None
    
    # create link to user's weather location
    weather = requests.get(f'https://api.weather.gov/points/{lat},{lng}')
    for attempt in range(MAX_ATTEMPT):
        if weather.status_code == 200: 
            weatherLink = weather.json()
            temp_url = weatherLink['properties']['forecast']
            precipitation_url = weatherLink['properties']['forecastGridData']   
            return temp_url, precipitation_url, city, state 
    return None, None, None, None

# get weather from weather Link
def get_weather(searchStartWeather, POPSdata):
        # get temperature
        max_temp = float('-inf')
        avg_temp = 0
        min_temp = float('inf')
        total_temp = 0
        tcount = 0
        for entry in searchStartWeather:
            startTime = entry['startTime']
            endTime = entry['endTime']
            temperature = entry['temperature']
            if startTime.startswith(today) or endTime.startswith(today):
                max_temp = int(round(max(max_temp, temperature) + 0.1))
                min_temp = int(round(min(min_temp, temperature) + 0.1))
                total_temp += temperature
                tcount += 1
        if tcount > 0:
            avg_temp = total_temp / tcount
            avg_temp = int(round(avg_temp + 0.1))
        else:
            avg_temp = 0 

        # get dew point
        max_dewP = float('-inf')
        avg_dewP = 0
        min_dewP = float('inf')
        total_dewP = 0
        dcount = 0
        for entry in searchStartWeather:
            startTime = entry['startTime']
            endTime = entry['endTime']
            dewPoint = (entry['dewpoint']['value'] * 9/5) + 32
            if startTime.startswith(today) or endTime.startswith(today):       
                max_dewP = round(max(max_dewP, dewPoint), 2)
                min_dewP = round(min(min_dewP, dewPoint), 2)
                total_dewP += dewPoint
                dcount += 1
        if dcount > 0:
            avg_dewP = total_dewP / dcount
            avg_dewP = round(avg_dewP, 2)
        else:
            avg_dewP = 0 

        # get humidity
        max_humid = float('-inf')
        avg_humid = 0
        min_humid = float('inf')  
        total_humid = 0
        hcount = 0
        for entry in searchStartWeather:
            startTime = entry['startTime']
            endTime = entry['endTime']
            humidity = entry['relativeHumidity']['value']
            if startTime.startswith(today) or endTime.startswith(today):       
                max_humid = int(round(max(max_humid, humidity) + 0.1))
                min_humid = int(round(min(min_humid, humidity) + 0.1))
                total_humid += humidity
                hcount += 1
        if hcount > 0:
            avg_humid = total_humid / hcount
            avg_humid = int(round(avg_humid + 0.1))
        else:
            avg_humid = 0 

        # get wind speed
        max_windS = float('-inf')
        avg_windS = 0
        min_windS = float('inf')
        listWindSpeed = []
        for entry in searchStartWeather:
            startTime = entry['startTime']
            endTime = entry['endTime']
            windSpeed = entry['windSpeed']
            if startTime.startswith(today) or endTime.startswith(today):   
                numbers = re.findall(pattern, windSpeed)
                listWindSpeed.extend(numbers)
                listWindSpeed = list((map(float, listWindSpeed)))
        for i in range(len(listWindSpeed)):
            max_windS = round(max(max_windS, listWindSpeed[i]), 2)
            min_windS = round(min(min_windS, listWindSpeed[i]), 2)
        avg_windS = round((max_windS + min_windS)/2, 2)

        #calculating precipitation
        mmPrecipitation = 0 
        precipitation = POPSdata['properties']['quantitativePrecipitation']['values']
        for entry in precipitation:
            validTime = entry['validTime']
            value = entry['value']
            if validTime.startswith(today):
                mmPrecipitation = mmPrecipitation + entry['value']
        actualPrecipitation = round(mmPrecipitation / 25.4, 2)

        # get snow 
        snowAmount = 0 
        precipitation = POPSdata['properties']['snowfallAmount']['values']
        for entry in precipitation:
            validTime = entry['validTime']
            value = entry['value']
            if validTime.startswith(today):
                snowAmount = snowAmount + entry['value']
        snowAmount = round(snowAmount, 2)

        # get forcast
        forcastInfo = []
        for entry in searchStartWeather:
            startTime = entry['startTime']
            endTime = entry['endTime']
            forcastDescription = entry['shortForecast']
            if startTime.startswith(today) or endTime.startswith(today):       
                forcastInfo.append(forcastDescription)
        forcast = ', '.join(forcastInfo)
        return max_temp, avg_temp, min_temp, max_dewP, avg_dewP, min_dewP, max_humid, avg_humid, min_humid, max_windS, avg_windS, min_windS, actualPrecipitation, snowAmount, forcast



# data base upload function
def database_upload( username, password, hostname, database_name, max_temp, avg_temp, min_temp, max_dewP, 
                            avg_dewP, min_dewP, max_humid, avg_humid, 
                            min_humid, max_windS, avg_windS, min_windS, 
                            actualPrecipitation, snowAmount, forcast):
    # insert into pgadmin database into the Daily_Weather table
    try:
        connection = psycopg2.connect(
            user=username,
            password=password,
            host=hostname,
            port="5432",
            database=database_name
        )

        cursor = connection.cursor()

        # Define the INSERT statement
        postgres_insert_query = """ INSERT INTO DAILY_WEATHER (_date, max_temperature, avg_temperature, min_temperature,
        max_dew_point, avg_dew_point, min_dew_point, max_humidity, avg_humidity, min_humidity, max_wind_speed, avg_wind_speed, min_wind_speed, precipitation, snow_amount, forecast) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        # Example data to insert
        record_to_insert = (today, max_temp, avg_temp, min_temp, max_dewP, 
                            avg_dewP, min_dewP, max_humid, avg_humid, 
                            min_humid, max_windS, avg_windS, min_windS, 
                            actualPrecipitation, snowAmount, forcast)

        # Execute the INSERT statement
        cursor.execute(postgres_insert_query, record_to_insert)

        # Commit the transaction
        connection.commit()

        # Print success message
        report_list.insert(1, 'Record inserted successfully\n')

    except (Exception, Error) as error:
        report_list.insert(1, f'Error while connecting to PostgreSQL: {error}\n')

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            report_list.insert(2, 'PostgreSQL connection is closed\n')
            return report_list