from dotenv import load_dotenv
import os
import requests
from datetime import datetime as dt
from twilio.rest import Client

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

alphavantage_url = "https://www.alphavantage.co/query"
current_date = int(str(dt.now().date()).split("-")[2])

# Fetch STOCK price increase/decreases by 5% between yesterday and the day before yesterday

alphavantage_parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": "TSLA",
    "interval": "60min",
    "apikey": os.getenv("API_KEY"),
}

response = requests.get(url=alphavantage_url, params=alphavantage_parameters)
response.raise_for_status()
data = response.json()

price_yesterday = float(data["Time Series (60min)"][f"2025-03-{current_date - 2} 19:00:00"]["4. close"])
price_day_before_yesterday = float(data["Time Series (60min)"][f"2025-03-{current_date - 3} 19:00:00"]["4. close"])

percentage_change = round(((price_yesterday-price_day_before_yesterday)/price_day_before_yesterday)*100, 2)


# get the first 3 news pieces for the TSLA.

news_parameters = {
    "apiKey": os.getenv("NEWS_API"),
    "q": "TSLA",
}

response = requests.get(
    url="https://newsapi.org/v2/everything", params=news_parameters)
response.raise_for_status()
data = response.json()["articles"]

article1_title = data[0]["title"]
article1_description = data[0]["description"]

article2_title = data[1]["title"]
article2_description = data[1]["description"]

article3_title = data[2]["title"]
article3_description = data[2]["description"]


# Send a seperate message with the percentage change and each article's title and description to your phone number.

def symbol(percentage):
    if percentage < 0:
        return "🔻"
    else:
        return "🔺"


message_body = f"""*TSLA:* {symbol(percentage_change)} {abs(percentage_change)}%

*Headline:* {article1_title}
*Brief:* {article1_description}

*Headline:* {article2_title}
*Brief:* {article2_description}

*Headline:* {article3_title}
*Brief:* {article3_description}"""

client = Client(account_sid, auth_token)

try:
    message = client.messages.create(
        body=message_body,
        from_='whatsapp:+14155238886',
        to='whatsapp:+923103288291'
    )
    print(f"Message sent: {message.status}")
except Exception as e:
    print(f"Error sending message: {e}")
