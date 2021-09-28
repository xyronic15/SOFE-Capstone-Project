from datetime import date

import yfinance as yf

# date range for collecting data from START to TODAY
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data
