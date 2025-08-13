# Function to generate buy trade signals based on:
# 1. RSI < 30 (oversold)
# 2. 20-day MA > 50-day MA (bullish crossover)
# Add a column 'Signal' where 1 = Buy, 0 = No Signal
# strategy.py

def generate_trade_signals(df):
    """
    Generate buy signals where:
    - RSI < 30 (oversold)
    - 20-day MA > 50-day MA (bullish confirmation)
    """
    df['Signal'] = (
        (df['RSI'] < 30) & (df['MA20'] > df['MA50'])
    ).astype(int)
    
    return df
