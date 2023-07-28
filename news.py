import requests
from keys import newsapikey

def get_news(query):
    apikey = newsapikey
    url = f'https://gnews.io/api/v4/search?q=example&lang=en&country=us&max=10&apikey={apikey}'

    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()
        articles = data['articles']

        for article in articles:
            print("Title: " + article['title'])
            print("Description: " + article['description'])
    else:
        print("Error accessing news API. Status Code:", response.status_code)
