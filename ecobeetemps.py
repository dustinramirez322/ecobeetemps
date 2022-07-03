import requests
import json
from datetime import datetime

def authorize():
    try:
        try:
            #Read API key file
            #This file should be manually created by the user
            #Your application's API key must be retrieved from ecobee.com
            with open('apiKey.txt') as a:
                apiKey = a.read().splitlines()

        except FileNotFoundError:
            print("We're having trouble finding your apiKey...check to make sure the apiKey.txt file is "
                  "in the correctplace")
            return

        #Request initial authorization information using the API key
        authorize = requests.get(
            'https://api.ecobee.com/authorize?response_type=ecobeePin&client_id=' + apiKey[0] + '&scope=smartWrite').json()

        #Write the code that will be used in future calls to a text file
        with open('code.txt', 'w') as c:
            c.write(authorize['code'])

        #Notifies the user that their code has been written to the text file
        #Provides the authorization Pin and provides basic instructions required by the user to continue
        print('Your code is ' + authorize['code'] + ' and has been written to the code.txt file. \n \
             Your pin is ' + authorize['ecobeePin'] + ' and expires in 5 minutes.  \n \
             Quickly authorize your app at ecobee.com before moving onto the next step.')

    except requests.exceptions.ConnectionError:
        print("You're unable to reach ecobee's API...check your internet connection")
        #do something for this
        #do something for that

    finally:
        pass
        #do something

def access_token():
    #Retrieve the recently created code and API key
    with open('code.txt') as c:
        code = c.read().splitlines()
    with open('apiKey.txt') as a:
        apiKey = a.read().splitlines()

    #Submits a request for an access and refresh token to be used in future calls
    access_token = requests.post('https://api.ecobee.com/token?grant_type=ecobeePin&code=' + code[0] + '&client_id=' + apiKey[0])

    #Write access and refresh token to files
    with open('access_token.txt', 'w') as at:
        at.write(access_token['access_token'])
    with open('refresh_token.txt', 'w') as r:
        r.write(access_token['refresh_token'])

    #Relay what the function has accomplished
    print('Your access and refresh tokens have been written to access_token.txt and refresh_token.txt')

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
