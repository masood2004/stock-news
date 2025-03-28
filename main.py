from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from twilio.rest import Client

load_dotenv()

# Constants
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_URL = "https://www.alphavantage.co/query"
NEWS_API_URL = "https://newsapi.org/v2/everything"
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"
TWILIO_WHATSAPP_TO = "whatsapp:+923103288291"

# Load credentials
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
alpha_api_key = os.getenv("API_KEY")
news_api_key = os.getenv("NEWS_API")

# Function to fetch stock prices


def fetch_stock_prices():
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": STOCK,
        "interval": "60min",
        "apikey": alpha_api_key,
    }

    response = requests.get(ALPHAVANTAGE_URL, params=params)
    response.raise_for_status()
    data = response.json().get("Time Series (60min)", {})

    if not data:
        raise ValueError("No stock data returned.")

    sorted_timestamps = sorted(data.keys(), reverse=True)
    prices = {}

    for timestamp in sorted_timestamps:
        date_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        hour = date_obj.hour
        if hour == 19:
            date_str = date_obj.date().isoformat()
            if date_str not in prices:
                prices[date_str] = float(data[timestamp]["4. close"])
            if len(prices) >= 2:
                break

    if len(prices) < 2:
        raise ValueError("Insufficient historical data.")

    dates = sorted(prices.keys(), reverse=True)
    return prices[dates[0]], prices[dates[1]]

# Function to calculate percentage change


def calculate_percentage_change(new, old):
    return round(((new - old) / old) * 100, 2)

# Function to fetch news articles


def fetch_news():
    params = {
        "apiKey": news_api_key,
        "qInTitle": COMPANY_NAME,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 3
    }

    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    articles = response.json().get("articles", [])

    if not articles:
        raise ValueError("No news articles found.")

    return articles[:3]

# Function to format the message


def format_message(percentage, articles):
    symbol = "🔺" if percentage >= 0 else "🔻"
    message = f"*{STOCK}:* {symbol} {abs(percentage)}%\n\n"
    for article in articles:
        title = article.get("title", "No Title")
        description = article.get("description", "No Description")
        message += f"*Headline:* {title}\n*Brief:* {description}\n\n"
    return message.strip()

# Function to send WhatsApp message


def send_whatsapp_message(body):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=TWILIO_WHATSAPP_FROM,
        to=TWILIO_WHATSAPP_TO
    )
    print(f"Message sent. Status: {message.status}")

# Main execution


def main():
    try:
        yesterday_price, day_before_price = fetch_stock_prices()
        change = calculate_percentage_change(yesterday_price, day_before_price)
        articles = fetch_news()
        message_body = format_message(change, articles)
        send_whatsapp_message(message_body)
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
