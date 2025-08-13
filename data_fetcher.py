# data_fetcher.py

import yfinance as yf
import pandas as pd
from config import STOCKS, DATA_PERIOD, DATA_INTERVAL
import os

def fetch_stock_data(symbol):
    print(f"Fetching data for {symbol}")
    data = yf.download(symbol, period=DATA_PERIOD, interval=DATA_INTERVAL)
    data.reset_index(inplace=True)
    return data

def save_data_locally(symbol, df):
    folder = 'data'
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{symbol}.csv")
    df.to_csv(filepath, index=False)
    print(f"Saved: {filepath}")

def fetch_all():
    for symbol in STOCKS:
        df = fetch_stock_data(symbol)
        save_data_locally(symbol, df)

if __name__ == "__main__":
    fetch_all()
