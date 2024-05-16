import webbrowser
import requests
import speech_recognition as sr
import os
import time
import datetime
import subprocess
from keys import gemini_apikey
import subprocess
from webapps import open_webapp
from apps import open_app
from instagram import login_instagram
from news import get_news
from weather import get_weather_for_place
from weather import get_weather_forecast_for_place
import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException
import re

genai.configure(api_key=gemini_apikey)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

chatStr = ""


def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F700-\U0001F77F"  
        u"\U0001F780-\U0001F7FF"  
        u"\U0001F800-\U0001F8FF"  
        u"\U0001F900-\U0001F9FF"  
        u"\U0001FA00-\U0001FA6F"  
        u"\U0001FA70-\U0001FAFF"  
        u"\U00002702-\U000027B0"  
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)


def chat(query):
    global chatStr
    chatStr += f"Abdullah: {query}\nAbdullah's Assistant: "

    try:
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [query],
                }
            ]
        )

        response = chat_session.send_message(query)
        assistant_response = remove_emojis(response.text)
        chatStr += f"{assistant_response}"
        print(assistant_response)
        return assistant_response
    except StopCandidateException as e:
        print(f"Generation stopped: {e}")
        assistant_response = "I'm sorry, I can't continue the conversation."
        chatStr += f"{assistant_response}"
        return assistant_response


def ai(prompt):
    try:
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [prompt],
                }
            ]
        )

        response = chat_session.send_message(prompt)
        s = f"Gemini response for Prompt: {prompt} \n *************************\n\n"
        s += remove_emojis(response.text)

        if not os.path.exists("ai"):
            os.mkdir("ai")
        with open(f"ai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(s)
    except StopCandidateException as e:
        print(f"Generation stopped: {e}")
        s = "I'm sorry, I can't continue the conversation."
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
                weather_data_forecast = get_weather_forecast_for_place(place_name_forecast, num_days)
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

