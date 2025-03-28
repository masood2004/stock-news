# 📈 Stock News Alert 🚨

A Python application that monitors stock price changes and sends relevant news alerts via WhatsApp using Twilio.

## 🌟 Features

- 📉 Fetches hourly stock data using **Alpha Vantage API**
- 📰 Retrieves latest news headlines with **News API**
- 💬 Sends automated alerts via **WhatsApp** using Twilio
- 🔔 Notifies users about significant price changes (±%)


## ⚙️ Prerequisites

- [Python 3.8+](https://www.python.org/)
- [Alpha Vantage API Key](https://www.alphavantage.co/)
- [News API Key](https://newsapi.org/)
- [Twilio Account](https://www.twilio.com/)
- Enable WhatsApp Sandbox in [Twilio Console](https://console.twilio.com/)


## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/masood2004/stock-news.git
   cd stock-news
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```env
   API_KEY=your_alpha_vantage_key
   NEWS_API=your_news_api_key
   ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   ```


## ⚡ Configuration

| Environment Variable | Description                          |
|----------------------|--------------------------------------|
| `API_KEY`            | Alpha Vantage API key                |
| `NEWS_API`           | News API key                         |
| `ACCOUNT_SID`        | Twilio Account SID                   |
| `TWILIO_AUTH_TOKEN`  | Twilio Authentication Token          |

**Note:** Replace `TWILIO_TO` in `main.py` with your WhatsApp number in international format.


## 🚀 Usage

Run the script:
```bash
python main.py
```

The script will:
1. Check Tesla's (TSLA) stock price change between two consecutive trading days
2. Fetch top 3 related news articles
3. Send formatted WhatsApp message with:
   - Stock symbol and percentage change (🔺/🔻)
   - News headlines and brief descriptions

**Example Message:**
```
TSLA: 🔺 5.23%
Headline: Tesla Announces Breakthrough Battery Technology
Brief: Tesla reveals new battery design promising 50% longer range...
```


## 🔧 Customization

1. Change target stock:
   ```python
   # In main.py
   STOCK = "AAPL"  # Apple stock
   COMPANY_NAME = "Apple Inc"
   ```

2. Adjust time series interval (currently 60min):
   ```python
   params = {
       "interval": "30min",  # Change interval
   }
   ```


## 🛑 Limitations

- Alpha Vantage's free tier has 5 API calls/minute limit
- News API free plan provides articles up to 1 month old
- Requires consistent 19:00:00 market close data points


## 🧰 Built With

- [Python](https://www.python.org/)
- [Alpha Vantage API](https://www.alphavantage.co/)
- [News API](https://newsapi.org/)
- [Twilio API](https://www.twilio.com/)


## 📜 License

MIT License - See [LICENSE](LICENSE) for details.


## 🙏 Acknowledgements

- Alpha Vantage for financial data
- NewsAPI.org for news aggregation
- Twilio for WhatsApp integration
