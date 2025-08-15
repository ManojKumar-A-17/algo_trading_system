# Algo Trading System with ML + Automation

This is a Python-based mini algo-trading project I built as part of an assignment.  
It fetches stock market data, applies a basic trading strategy, backtests it, logs results to Google Sheets, predicts next-day movement using ML, and even sends Telegram alerts.  

---

## What it does
- Gets stock data (currently for 3 NIFTY 50 stocks) using yfinance
- Calculates RSI, Moving Averages, MACD
- Uses RSI < 30 + MA20 > MA50 as buy signal
- Backtests the strategy for the past 6 months
- Logs trades + summary into Google Sheets automatically
- Runs a Decision Tree model to predict next day up/down movement
- Can run daily using a scheduler
- Sends Telegram alerts for buy signals

---

## Tools / Libraries
- Python 3.x
- yfinance  
- pandas, numpy  
- ta (technical analysis)  
- scikit-learn  
- gspread, oauth2client (Google Sheets API)  
- requests (for Telegram alerts)  
- schedule (for automation)

---

## How the project is structured

algo_trading_system/
│

├── main.py # Runs the full workflow

├── config.py # Stock list, API keys, settings

├── data_fetcher.py # Download stock data

├── indicators.py # RSI, MA, MACD

├── strategy.py # Buy signal logic

├── backtest.py # Backtesting function

├── logger_google_sheets.py # Save results to Google Sheets

├── ml_model.py # ML prediction logic

├── telegram_alerts.py # Send Telegram messages

├── automation.py # Scheduler to auto-run daily

├── credentials/
│ └── credentials.json # Google API credentials

└── data/ # CSV data storage

---

## GOOGLE SHEETS

1.Enable Google Sheets API in Google Cloud Console
2.Create a service account and download credentials.json
3.Put it in the credentials/ folder
4.Share your Google Sheet with the service account email

---

## TELEGRAM BOT

1.Create a bot with BotFather and get the bot token
2.Get your chat ID from @userinfobot
3.Put both in config.py

---

## How to set it up

**DEPENDENCIES**

pandas>=1.5.0              # Data manipulation and analysis
yfinance>=0.2.0            # Yahoo Finance API for stock data
scikit-learn>=1.3.0        # Machine learning algorithms
schedule>=1.2.0            # Task scheduling
requests>=2.31.0           # HTTP requests for APIs
gspread>=5.10.0            # Google Sheets integration
oauth2client>=4.1.3        # Google API authentication
numpy>=1.24.0              # Numerical computing
matplotlib>=3.7.0          # Data visualization (optional)

**Clone the repo**
   
```
pip install -r requirements.txt
git clone https://github.com/Manojkumar-A-17/algo_trading_system.git
cd algo_trading_system
```
---

## DISCLAIMER

Important: This software is for educational and research purposes only.

Not Financial Advice: All signals and predictions are algorithmic outputs
Risk Warning: Trading involves substantial risk of loss
Use Responsibly: Always conduct your own research before trading
Compliance: Ensure compliance with local financial regulations

---

## LICENSE

This project is licensed under the MIT License - see the LICENSE file for details.

---
