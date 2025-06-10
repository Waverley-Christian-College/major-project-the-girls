import requests
import json
from datetime import datetime
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

API_KEY = '5296eb9cb95697ef016ac7de004f18c24ecfad7c'

def fetch_news(ticker):
    url = f"https://api.tiingo.com/tiingo/news?tickers={ticker}"
    headers = {
     "Content-Type": "application/json",
     "Authorization": f"Token {API_KEY}"
    
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        news_data = response.json()
        headlines = [article['title'] for article in news_data]
        return headlines
    else:
        print('Error fetching news.')
        return []
   
TICKER = input('TICKER = ')
news_headlines = fetch_news(TICKER)
news_headlines = json.dumps(news_headlines, indent=4)

analyzer = SentimentIntensityAnalyzer()
sentiment_scores = analyzer.polarity_scores(news_headlines)
compound = sentiment_scores['compound']
print(sentiment_scores['compound'])
if compound > 0:
    print('Positive')
elif compound == 0:
    print('Neutral')
elif compound < 0:
    print('Negative')
else:
    print('Sorry, the analyzer did not work.')