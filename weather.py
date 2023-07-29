import requests
from keys import weatherapikey


def get_weather_for_place(place):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={place}&apikey={weatherapikey}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data.get("data") and data["data"].get("values"):
            temperature = data["data"]["values"]["temperature"]
            apparent_temperature = data["data"]["values"]["temperatureApparent"]
            dew_point = data["data"]["values"]["dewPoint"]
            humidity = data["data"]["values"]["humidity"]
            wind_speed = data["data"]["values"]["windSpeed"]
            wind_direction = data["data"]["values"]["windDirection"]
            wind_gust = data["data"]["values"]["windGust"]

            return (

                f"The current temperature is {temperature}°C, and it feels like {apparent_temperature}°C. "
                f"The dew point is {dew_point}°C, humidity is {humidity}%, "
                f"wind speed is {wind_speed} m/s, wind direction is {wind_direction} degrees, and wind gust is {wind_gust} m/s."
            )
        else:
            return f"Sorry, couldn't find weather data for {place}."
    else:
        return f"Failed to fetch weather data for {place}."



import requests
from keys import weatherapikey

def get_weather_forecast_for_place(place):
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={place}&timesteps=1d&apikey={weatherapikey}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data.get("timelines") and data["timelines"].get("daily"):
            forecast_intervals = data["timelines"]["daily"]

            forecast_info = ""
            for interval in forecast_intervals:
                time = interval["time"]
                temperature_avg = interval["values"]["temperatureAvg"]
                temperature_max = interval["values"]["temperatureMax"]
                temperature_min = interval["values"]["temperatureMin"]
                apparent_temperature_avg = interval["values"]["temperatureApparentAvg"]
                apparent_temperature_max = interval["values"]["temperatureApparentMax"]
                apparent_temperature_min = interval["values"]["temperatureApparentMin"]
                dew_point_avg = interval["values"]["dewPointAvg"]
                dew_point_max = interval["values"]["dewPointMax"]
                dew_point_min = interval["values"]["dewPointMin"]
                humidity_avg = interval["values"]["humidityAvg"]
                humidity_max = interval["values"]["humidityMax"]
                humidity_min = interval["values"]["humidityMin"]
                wind_speed_avg = interval["values"]["windSpeedAvg"]
                wind_speed_max = interval["values"]["windSpeedMax"]
                wind_speed_min = interval["values"]["windSpeedMin"]
                wind_direction_avg = interval["values"]["windDirectionAvg"]
                wind_gust_avg = interval["values"]["windGustAvg"]
                wind_gust_max = interval["values"]["windGustMax"]
                wind_gust_min = interval["values"]["windGustMin"]

                forecast_info += (
                    f"At {time} - "
                    f"The average temperature is {temperature_avg}°C, with a maximum of {temperature_max}°C and a minimum of {temperature_min}°C. "
                    f"The average apparent temperature is {apparent_temperature_avg}°C, with a maximum of {apparent_temperature_max}°C and a minimum of {apparent_temperature_min}°C. "
                    f"The average dew point is {dew_point_avg}°C, with a maximum of {dew_point_max}°C and a minimum of {dew_point_min}°C. "
                    f"The average humidity is {humidity_avg}%, with a maximum of {humidity_max}% and a minimum of {humidity_min}%. "
                    f"The average wind speed is {wind_speed_avg} m/s, with a maximum of {wind_speed_max} m/s and a minimum of {wind_speed_min} m/s. "
                    f"The average wind direction is {wind_direction_avg} degrees. "
                    f"The average wind gust is {wind_gust_avg} m/s, with a maximum of {wind_gust_max} m/s and a minimum of {wind_gust_min} m/s.\n"
                )

            return forecast_info
        else:
            return f"Sorry, couldn't find weather forecast for {place}."
    else:
        return f"Failed to fetch weather forecast for {place}."

if __name__ == '__main__':
    query = input("Enter the location for weather forecast: ")
    forecast = get_weather_forecast_for_place(query)
    print(forecast)