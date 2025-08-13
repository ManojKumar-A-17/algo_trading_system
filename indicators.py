# indicators.py

import pandas as pd
from ta.momentum import RSIIndicator

def calculate_indicators(df):
    # Calculate RSI (14-day)
    rsi = RSIIndicator(close=df['Close'], window=14)
    df['RSI'] = rsi.rsi()
    
    # Calculate moving averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    return df
