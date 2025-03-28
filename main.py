from dotenv import load_dotenv
import os
import requests
from datetime import datetime as dt, timedelta
from twilio.rest import Client

# Load environment variables
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API")
TWILIO_SID = os.getenv("ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = 'whatsapp:+14155238886'
TWILIO_TO = 'whatsapp:+923103288291'

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_URL = "https://www.alphavantage.co/query"
NEWS_URL = "https://newsapi.org/v2/everything"


def fetch_stock_prices(symbol):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "60min",
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(ALPHA_URL, params=params)
    response.raise_for_status()
    data = response.json()["Time Series (60min)"]

    # Extract the latest two available closing prices at 19:00:00
    timestamps = sorted([ts for ts in data if ts.endswith("19:00:00")], reverse=True)
    if len(timestamps) < 2:
        raise ValueError("Not enough data points for comparison")

    latest_close = float(data[timestamps[0]]["4. close"])
    previous_close = float(data[timestamps[1]]["4. close"])
    percentage_change = round(((latest_close - previous_close) / previous_close) * 100, 2)
    return percentage_change


def fetch_news(query, limit=3):
    params = {
        "apiKey": NEWS_API_KEY,
        "q": query,
        "sortBy": "publishedAt",
        "language": "en"
    }
    response = requests.get(NEWS_URL, params=params)
    response.raise_for_status()
    articles = response.json()["articles"][:limit]
    return [(a["title"], a["description"]) for a in articles]


def format_message(stock, change, news_articles):
    symbol = "🔺" if change >= 0 else "🔻"
    message = [f"*{stock}:* {symbol} {abs(change)}%"]

    for title, desc in news_articles:
        message.append(f"\n*Headline:* {title}\n*Brief:* {desc}")

    return "\n".join(message)


def send_whatsapp_message(body):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        print(f"Message sent successfully. SID: {message.status}")
    except Exception as e:
        print(f"Failed to send message: {e}")


def main():
    try:
        change = fetch_stock_prices(STOCK)
        news = fetch_news(STOCK)
        message = format_message(STOCK, change, news)
        send_whatsapp_message(message)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
