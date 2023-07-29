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
from weather import process_query

chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Abdullah: {query}\n Abdullah's Assistant: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    assistant_response = response["choices"][0]["text"]
    chatStr += f"{assistant_response}\n"
    return assistant_response


def ai(prompt):
    openai.api_key = apikey
    s = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
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
    say("Hello boss, I am your personal Assistant ")
    while True:
        print("Listening...")
        query = take()

        if query is not None:
            if "open my instagram" in query.lower():
                login_instagram()
            elif "goodbye assistant" in query.lower():
                say("Goodbye boss, shutting down.")
                break  # Exit the while loop and stop listening
            elif "reset chat" in query.lower():
                chatStr = ""
            elif "the time" in query.lower():
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                say(f"Boss, the time is {hour}:{min}")
            elif "artificial intelligence" in query.lower():
                ai(prompt=query)
                print("done")

            elif "Tell me the weather for" in query.lower():
                weather_data = process_query(query)
                if weather_data:
                    say(weather_data)
                    print("actual")

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
                    # Use chat() function for general queries
                    response = chat(query)
                    say(response)
        else:
            say("Sorry, I couldn't understand you.")