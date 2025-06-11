import requests
import json
from datetime import datetime
import os
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Your tiingo API TOKEN
API_KEY = '5296eb9cb95697ef016ac7de004f18c24ecfad7c'

def fetch_news(ticker):
    url = f"https://api.tiingo.com/tiingo/news?tickers={ticker}"
    headers = {
     "Content-Type": "application/json",
     "Authorization": f"Token {API_KEY}"
 # fetches the news from a specific company   
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        news_data = response.json()
        headlines = [article['title'] for article in news_data]
        return headlines
#gets the headlines of the news articles
    else:
        print('Error fetching news.')
        return []
   
TICKER = input('TICKER = ')
news_headlines = fetch_news(TICKER)
news_headlines = json.dumps(news_headlines, indent=4)

analyzer = SentimentIntensityAnalyzer()
sentiment_scores = analyzer.polarity_scores(news_headlines)
# use the vader sentiment analyzer to analyse news headlines on the company to see if it is doing well
compound = sentiment_scores['compound']
print(sentiment_scores['compound'])
# print out the overall score of the company, then comments on if it is doing well
if compound > 0:
    print(f'{TICKER} is doing well')
elif compound == 0:
    print(f'{TICKER} is so-so')
elif compound < 0:
    print(f'{TICKER} is not doing well')
else:
    print('Sorry, the analyzer did not work.')


# Parameters, company symbol, date range, and shares bought
symbol = input("Enter company symbol: ") 
start_date = input("Enter the start date (YYYY-MM-DD): ") 
end_date = input("Enter the end date (YYYY-MM-DD): ") # Ensure the dates are working days
shares_bought = int(input("Enter the shares you bought: ")) #Enter the amount of shares you invested
# define the URL and headers for the Tiingo API request
url = f"https://api.tiingo.com/tiingo/daily/{symbol}/prices"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {API_KEY}"
}
params = {
    "startDate": start_date,
    "endDate": end_date,
    "resampleFreq": "daily" 
}
# Make the request
response = requests.get(url, headers=headers, params=params)
data = response.json()
# Extract dates and closing prices
dates = [entry["date"][:10] for entry in data]
closes = [entry["close"] for entry in data]
# Simplify x-axis: show only every Nth date label
N = max(1, len(dates) // 12)  # Show about 12 labels
xticks = [i for i in range(0, len(dates), N)]
xtick_labels = [dates[i] for i in xticks]
# Plotting
plt.figure(figsize=(20, 5))
plt.plot(dates, closes, marker=None)
plt.title(f"{symbol} Closing Prices from {start_date}")
plt.xlabel("Date")
plt.ylabel("Close Price (USD)")
plt.xticks(xticks, xtick_labels, rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
plt.tight_layout()
plt.savefig("stock_chart_tiingo.png")

for entry in data:
    date_str = entry["date"][:10]
    if date_str == start_date:
        close_start = entry["close"]
    if date_str == end_date:
        close_end = entry["close"]
        
# Calculate the price spent and shares holding
price_spent = shares_bought * close_start
share_holdings = shares_bought * close_end
# Print the results with colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
print(f"{GREEN}Close price on {start_date}: {close_start}{RESET}")
print(f"{GREEN}Close price on {end_date}: {close_end}{RESET}")
print(f"{GREEN}Price spent: {price_spent} USD{RESET}")
print(f"{GREEN}Shares hloding on end_date: {share_holdings} USD{RESET}")
price_change = round(share_holdings - price_spent, 2) # Calculate the price change
if price_change > 0:
    print(f"{GREEN}Profit: {price_change} USD{RESET}")
else:
    print(f"{RED}Loss: {abs(price_change)} USD{RESET}")