import requests
import json
from datetime import datetime

def refresh_token():
    #Read apiKey and previous refresh_token from text files
    with open('apiKey.txt') as a:
        apiKey = a.read().splitlines()
    with open('refresh_token.txt') as r:
        refresh_token = r.read().splitlines()

    #Generate a new token via the ecobee api
    newtoken = requests.post(
        'https://api.ecobee.com/token?grant_type=refresh_token&refresh_token=' + refresh_token[0] + '&client_id=' + apiKey[0]).json()

    #Update the access_token and refresh_token files with new values
    with open('access_token.txt', 'w') as a:
        a.write(newtoken['access_token'])
    with open('refresh_token.txt', 'w') as r:
        r.write(newtoken['refresh_token'])

def get_temps():
    #Read previously defined access_token from file
    with open('access_token.txt') as a:
        access_token = a.read()

    #Define headers and Urls that will be used
    headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': 'Bearer ' + access_token}
    weatherUrl = 'https://api.ecobee.com/1/thermostat?json={"selection":{"selectionType":"thermostats","selectionMatch":"521761791881","includeWeather":True}}'
    sensorUrl = 'https://api.ecobee.com/1/thermostat?json={"selection":{"selectionType":"thermostats","selectionMatch":"521761791881","includeSensors":True}}'

    #Call the ecobee api for temperature info
    weatherInfo = requests.get(weatherUrl, headers=headers).json()
    sensorInfo = requests.get(sensorUrl, headers=headers).json()

    #Extract temps from responses
    outside = weatherInfo['thermostatList'][0]['weather']['forecasts'][0]['temperature']
    floor2 = sensorInfo['thermostatList'][0]['remoteSensors'][0]['capability'][0]['value']
    floor3 = sensorInfo['thermostatList'][0]['remoteSensors'][1]['capability'][0]['value']

    #Convert to celcius with only two decimal places
    outsideC = round((((outside/10)-32) * 5/9) ,2)
    floor2C = round((((int(floor2)/10)-32) * 5/9) ,2)
    floor3C = round((((int(floor3)/10)-32) * 5/9) ,2)

    #Get date and time
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M")

    #write temp information to file
    with open('temps.txt', 'a') as t:
        t.write(date + ',' + str(outsideC) + ',' + str(floor2C) + ',' + str(floor3C) + '\n')
