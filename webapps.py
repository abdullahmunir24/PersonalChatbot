import webbrowser
import subprocess

def open_webapp(query,say):
    web = [
        ["google", "https://www.google.com/?client=safari"],
        ["facebook", "https://www.facebook.com"],
        ["youtube", "https://www.youtube.com"],
        ["amazon", "https://www.amazon.com"],
        ["twitter", "https://www.twitter.com"],
        ["instagram", "https://www.instagram.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["reddit", "https://www.reddit.com"],
        ["stackoverflow", "https://www.stackoverflow.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["ebay", "https://www.ebay.com"],
        ["netflix", "https://www.netflix.com"],
        ["github", "https://www.github.com"],
        ["pinterest", "https://www.pinterest.com"],
        ["spotify", "https://www.spotify.com"],
        ["yahoo", "https://www.yahoo.com"],
        ["bing", "https://www.bing.com"],
        ["craigslist", "https://www.craigslist.org"],
        ["tumblr", "https://www.tumblr.com"],
        ["imdb", "https://www.imdb.com"],
        ["aliexpress", "https://www.aliexpress.com"],
        ["wordpress", "https://www.wordpress.com"],
        ["hulu", "https://www.hulu.com"],
        ["dropbox", "https://www.dropbox.com"],
        ["quora", "https://www.quora.com"],
        ["etsy", "https://www.etsy.com"],
        ["microsoft", "https://www.microsoft.com"],
        ["apple", "https://www.apple.com"],
        ["bbc", "https://www.bbc.co.uk"],
        ["cnn", "https://www.cnn.com"],
        ["nytimes", "https://www.nytimes.com"],
        ["instagram", "https://www.instagram.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["pinterest", "https://www.pinterest.com"],
        ["tiktok", "https://www.tiktok.com"],
        ["snapchat", "https://www.snapchat.com"],
        ["walmart", "https://www.walmart.com"],
        ["target", "https://www.target.com"],
        ["bestbuy", "https://www.bestbuy.com"],
        ["nike", "https://www.nike.com"],
        ["adidas", "https://www.adidas.com"],
        ["spotify", "https://www.spotify.com"],
        ["uber", "https://www.uber.com"],
        ["airbnb", "https://www.airbnb.com"]
    ]

    for w in web:
        if f"open {w[0].lower()}" in query.lower():
            say(f"Opening {w[0]} sir..")
            webbrowser.open(w[1])



# You can call the `open_webapp` function with your query to open the respective web app.
