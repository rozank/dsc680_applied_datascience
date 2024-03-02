# File:         weather_final_project.py
# Name:         Rojan Khatri
# Date:         02/25/2020
# Course:       Intro to Programming DSC510
# Description:  Create WeatherPP using OpenWeatherMap API
# Usage:        App takes in zip code or city name to obtain weather forecast from OpenWeatherMap.
#               Displays the weather forecast in a readable format to the user.
#               Used functions including a main function.
#               Allows the user to run the program multiple times to allow them to look up weather
#               conditions for multiple locations.
#               Validate whether the user entered valid data.
#               If valid data isn’t presented notify the user.


import datetime
import urllib.parse
import re

import pytemperature
import requests


# Function to convert timestamp to time in correct time zone
def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


# function to build a URL
def get_uri(user_input):
    base_uri = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = "bd7e9461be1f8e389ae7b1269e3aae81"
    # check to see if user entered ZipCode or City and build the uri parameters based on that
    if re.match("^[0-9]{5}(?:-[0-9]{4})?$", user_input):
        params = {"appid": api_key , "zip": user_input}
    else:
        params = {"appid": api_key , "q": user_input}
    # Now append the URL
    query_path = urllib.parse.urlencode(params)
    url = base_uri + query_path
    return url


# Function to query and display weather data
def get_weather_data(url):
    json_data = requests.get(url).json()  # converted data received to json
    return json_data


def print_weather_data(json_data, user_response):
    # extracting data from json format
    desc = json_data['weather'][0]['description']
    temp = json_data['main']['temp']
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    temp_min = json_data['main']['temp_min']
    temp_max = json_data['main']['temp_max']
    sunrise = json_data['sys']['sunrise']
    sunset = json_data['sys']['sunset']
    wind_speed = json_data['wind']['speed']
    name = json_data['name']

    # print weather data received from API call
    print(f'\nHere is your Weather Condition for {user_response} \n'
          '===================================================\n'
          f'City : {name}\n'
          f'Temperature : {pytemperature.k2f(temp)} F\n'
          f'Max Temperature : {pytemperature.k2f(temp_max)} F\n'
          f'Max Temperature : {pytemperature.k2f(temp_max)} F\n'
          f'Min Temperature : {pytemperature.k2f(temp_min)} F\n'
          f'Description : {desc}\n'
          f'Wind : {wind_speed} m/s\n'
          f'Pressure : {pressure}\n'
          f'Humidity : {humidity}%\n'
          f'Sunrise : {time_converter(sunrise)}\n'
          f'Sunset : {time_converter(sunset)}\n'
          '===================================================\n'
          )


def error_message(json_response, user_response):  # error handling
    message = json_response['message']
    error_code = json_response['cod']
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
          f'There was problem processing your weather inquiry request for {user_response}\n'
          f'Code : {error_code}\n'
          f'Description : {message}\n'
          '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
          )


def internal_error():
    print('Sorry for inconvenience. Please try again later.'
          '\nThank you for trying A2Z WeatherApp.')


# main function
def main():
    print('======================= Welcome to A2Z WeatherApp =======================')
    choice = 'y'
    while choice.lower() == 'y':  # loop until y is pressed to continue
        user_input = input(
            "\nPlease enter City or Zip code. "
            "If you are entering non US cities please use 'city, country' format :\n")
        url = get_uri(user_input)
        try:
            json_response = get_weather_data(url)
            error_code = json_response['cod']
            if error_code == 200:
                print_weather_data(json_response, user_input)
            elif error_code == 401:  # Invalid API Key. User cannot do anything so exit application
                error_message(json_response, user_input)
                internal_error()
                break
            elif error_code == 500:  # internal server error. User cannot do anything so exit application
                error_message(json_response, user_input)
                internal_error()
                break
            else:
                error_message(json_response, user_input)
            choice = input('Do you wish to continue? Press y or Y to continue or anything else to exit.\n')
        # When there is error like wrong URL or missing parameters that requires a developer to look into the code
        # print error message and exit out of code as there is no reason why they should be given second chance.
        except Exception as e:
            print('There was an internal error occurred.' + str(e))
            internal_error()
            break

    else:
        print('\n\nThank you for trying A2Z WeatherApp.')


if __name__ == "__main__":
    main()
