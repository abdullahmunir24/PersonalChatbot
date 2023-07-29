import requests
from keys import newsapikey

def get_news(country, num_headlines):
    main_url = "https://newsapi.org/v2/top-headlines"
    params = {"country": country, "apiKey": newsapikey}

    response = requests.get(main_url, params=params)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])
        headlines = "\n".join([article["title"] for article in articles[:num_headlines]])
        return headlines
    else:
        print("Failed to fetch news.")
        return None
