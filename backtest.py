# backtest.py

import pandas as pd

def simple_backtest(df, holding_days=5):
    trades = []

    for i in range(len(df)):
        if df.loc[i, 'Signal'] == 1:
            buy_date = df.loc[i + 1, 'Date'] if i + 1 < len(df) else None
            buy_price = df.loc[i + 1, 'Close'] if i + 1 < len(df) else None
            sell_index = i + 1 + holding_days

            if sell_index < len(df):
                sell_date = df.loc[sell_index, 'Date']
                sell_price = df.loc[sell_index, 'Close']
                pnl = sell_price - buy_price
                win = 1 if pnl > 0 else 0

                trades.append({
                    'Buy Date': buy_date,
                    'Buy Price': round(buy_price, 2),
                    'Sell Date': sell_date,
                    'Sell Price': round(sell_price, 2),
                    'P&L': round(pnl, 2),
                    'Win': win
                })

    return pd.DataFrame(trades)
