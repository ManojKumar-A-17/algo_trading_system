# main.py

import pandas as pd
import os
from config import STOCKS
from indicators import calculate_indicators
from strategy import generate_trade_signals
from backtest import simple_backtest
from logger_google_sheets import log_trades, log_summary
from ml_model import train_and_evaluate
from telegram_alerts import send_telegram_message, send_trade_summary, send_ml_accuracy

def load_data(symbol):
    filepath = os.path.join('data', f'{symbol}.csv')
    # Skip the malformed second row and ensure proper data types
    df = pd.read_csv(filepath, skiprows=[1])
    
    # Convert numeric columns to proper data types
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convert Date column to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Drop any rows with NaN values that might have been created
    df = df.dropna()
    
    return df

def main():
    for symbol in STOCKS:
        df = load_data(symbol)
        df = calculate_indicators(df)
        df = generate_trade_signals(df)

        # Send alert if buy or sell signals exist
        latest_signal = df.iloc[-1]['Signal']
        if latest_signal == 1:
            latest_date = df.iloc[-1]['Date'].strftime('%Y-%m-%d')
            latest_rsi = df.iloc[-1]['RSI']
            latest_price = df.iloc[-1]['Close']
            
            alert_message = f"""
 <b>BUY SIGNAL DETECTED!</b> 
 Stock: {symbol}
 Date: {latest_date}
 Price: ₹{latest_price:.2f}
 RSI: {latest_rsi:.2f}
 Strategy: RSI < 30 & MA20 > MA50
            """
            send_telegram_message(alert_message.strip())

        # Backtesting
        trades = simple_backtest(df)
        print(f"\n--- {symbol} Backtest Results ---")
        print(trades)

        if not trades.empty:
            total = len(trades)
            wins = trades['Win'].sum()
            avg_pnl = trades['P&L'].mean()
            win_rate = wins / total

            # Log to Google Sheets
            log_trades(symbol, trades)
            log_summary(symbol, total, wins, win_rate, avg_pnl)
            print(f"Logged to Google Sheet.")

            # Send Telegram summary
            send_trade_summary(symbol, total, wins, win_rate, avg_pnl)

            print(f"\nTotal Trades: {total}, Wins: {wins}, Win Rate: {win_rate:.2%}, Avg P&L: {avg_pnl:.2f}")
        else:
            print("No trades to log.")

        # ML Model Evaluation
        model, accuracy = train_and_evaluate(df)
        print(f" ML Prediction Accuracy for {symbol}: {accuracy:.2%}")
        
        # Send ML accuracy to Telegram
        send_ml_accuracy(symbol, accuracy)

if __name__ == "__main__":

    main()
