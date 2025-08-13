# logger_google_sheets.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = "Trading_Log"

def connect_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME)

def log_trades(symbol, trades_df):
    try:
        sheet = connect_google_sheet()
        trade_tab = sheet.worksheet("Trades")

        # Add header if sheet is empty
        if not trade_tab.get_all_values():
            trade_tab.append_row(["Stock", "Buy Date", "Buy Price", "Sell Date", "Sell Price", "P&L", "Win"])

        for _, row in trades_df.iterrows():
            trade_tab.append_row([
                str(symbol),  # Convert to string
                str(row['Buy Date']),  # Convert Timestamp to string
                float(row['Buy Price']),  # Convert to float
                str(row['Sell Date']),  # Convert Timestamp to string
                float(row['Sell Price']),  # Convert to float
                float(row['P&L']),  # Convert to float
                int(row['Win'])  # Convert to int
            ])
        print(f"Trades for {symbol} logged successfully.")

    except Exception as err:
        print(f" Could not log trades for {symbol}: {str(err)}")

def log_summary(symbol, total_trades, wins, win_rate, avg_pnl):
    try:
        sheet = connect_google_sheet()
        summary_tab = sheet.worksheet("Summary")

        # Add header if sheet is empty
        if not summary_tab.get_all_values():
            summary_tab.append_row(["Stock", "Total Trades", "Wins", "Win Rate", "Average P&L"])

        summary_tab.append_row([
            str(symbol),  # Convert to string
            int(total_trades),  # Convert to int
            int(wins),  # Convert to int
            f"{win_rate:.2%}",  # Already a string
            float(round(avg_pnl, 2))  # Convert to float
        ])
        print(f"Summary for {symbol} logged successfully.")

    except Exception as err:
        print(f" Could not log summary for {symbol}: {str(err)}")