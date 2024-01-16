import webbrowser
import requests
import speech_recognition as sr
import os
import time
import datetime
import openai
from keys import apikey
import subprocess
from webapps import open_webapp
from apps import open_app
from instagram import login_instagram
from news import get_news
from weather import get_weather_for_place
from weather import get_weather_forecast_for_place

chatStr = ""

def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"Abdullah: {query}Abdullah's Assistant: "

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    assistant_response = response["choices"][0]["text"]
    chatStr += f"{assistant_response}"
    print(assistant_response)
    return assistant_response


def ai(prompt):
    openai.api_key = apikey
    s = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    s += response["choices"][0]["text"]

    if not os.path.exists("ai"):
        os.mkdir("ai")
    with open(f"ai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(s)


def say(text):
    subprocess.call(["say", text])


def take():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 900
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language="en-PK")
        print("User said: " + query)
        return query
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand you.")
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")

    return None


if __name__ == '__main__':
    say("Hello Abdullah, I am your personal Assistant ")
    while True:
        print("\nListening...")
        query = take()

        if query is not None:
            if "open my instagram" in query.lower():
                login_instagram()
            elif "goodbye assistant" in query.lower():
                say("Goodbye Abdullah, shutting down.")
                break
            elif "reset chat" in query.lower():
                chatStr = ""
            elif "the time" in query.lower():
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                say(f"Abdullah, the time is {hour}:{min}")
            elif "artificial intelligence" in query.lower():
                ai(prompt=query)
                print("done")

            elif "tell me the weather for" in query.lower():
                place_name = query.lower().split("tell me the weather for ")[1]
                weather_data = get_weather_for_place(place_name)
                if weather_data:
                    say(weather_data)

            elif "give me the weather forecast for" in query.lower():
                place_name_forecast = query.lower().split("give me the weather forecast for ")[1]
                try:
                    say("How many days weather forecast would you like to see? Type the number in the chat")
                    num_days = int(input())
                except ValueError:
                    say("Invalid input for the number of days.")
                    continue
                weather_data_forecast = get_weather_forecast_for_place(place_name_forecast,num_days)
                if weather_data_forecast:
                    say(weather_data_forecast)


            elif "news" in query.lower():
                try:
                    say("How many news headlines would you like to see? Type the number in the chat")
                    num_headlines = int(input())
                except ValueError:
                    say("Invalid input for the number of headlines.")
                    continue

                say("Which country's news are you interested in? Type in the ISO 3166-1 code for the country, such as for USA it would be 'us', and for Canada it would be 'ca'")
                country = input().lower()

                news_data = get_news(country, num_headlines)
                if news_data:
                    say(news_data)


            else:

                if "open " in query.lower():
                    open_app(query, say)
                    open_webapp(query, say)
                else:
                    response = chat(query)
                    say(response)
        else:
            say("Sorry, I couldn't understand you.")