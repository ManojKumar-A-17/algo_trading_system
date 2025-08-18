# test_signals_analysis.py
from main import load_data
from indicators import calculate_indicators
from strategy import generate_trade_signals

def analyze_signals():
    symbols = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS'] # add your stock , as you mention in config.py.
    
    for symbol in symbols:
        print(f"\n {symbol} Signal Analysis:")
        print("=" * 50)
        
        df = load_data(symbol)
        df = calculate_indicators(df)
        df = generate_trade_signals(df)
        
        # Show last 10 days of data
        recent_data = df[['Date', 'Close', 'RSI', 'MA20', 'MA50', 'Signal']].tail(10)
        print(recent_data)
        
        # Count conditions
        oversold_days = len(df[df['RSI'] < 30])
        bullish_days = len(df[df['MA20'] > df['MA50']])
        signal_days = len(df[df['Signal'] == 1])
        
        print(f"\n Statistics:")
        print(f"Days with RSI < 30 (oversold): {oversold_days}")
        print(f"Days with MA20 > MA50 (bullish): {bullish_days}")
        print(f"Days with BOTH conditions (signals): {signal_days}")
        
        # Show specific signal days if any
        if signal_days > 0:
            signal_data = df[df['Signal'] == 1][['Date', 'Close', 'RSI', 'MA20', 'MA50']]
            print(f"\n Signal Days:")
            print(signal_data)

if __name__ == "__main__":

    analyze_signals()
