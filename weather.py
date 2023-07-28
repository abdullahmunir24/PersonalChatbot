import requests
from keys import weatherapikey

def process_query(query):
    place = query.lower().split("tell me the weather for ")[1]
    weatherloc(place)

def weatherloc(place):
    apiikey = weatherapikey
    url = 'http://api.openweathermap.org/geo/1.0/direct?}'

    p = {
        'q': place,
        'appid': apiikey
    }

    a = requests.get(url, params=p)

    if a.status_code == 200:
        data = a.json()
        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            weather(place, lat, lon)
        else:
            print("Can't find location")


def weather(place, lat, lon):
    apiikkey = weatherapikey
    url = 'https://api.openweathermap.org/data/3.0/onecall'

    pm = {
        'lat': lat,
        'lon': lon,
        'appid': apiikkey
    }

    b = requests.get(url, params=pm)

    if b.status_code == 200:
        d = b.json()
        if d:
            weather_description = d['current']['weather'][0]['description']
            return f"The weather for {place} is {weather_description}"
        else:
            print("Hello")
