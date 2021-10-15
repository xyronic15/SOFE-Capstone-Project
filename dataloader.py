from datetime import date
import pandas as pd
import yfinance as yf
from identify_pattern import search

# date range for collecting data from START to TODAY
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# patterns_bullish = ['hammer', 'inv_hammer', 'engulfing_bullish', 'piercing', 'morning_star', 'white_soldiers', 'rising_method']
patterns_bullish = ['hammer', 'inv_hammer', 'engulfing_bullish', 'piercing']
patterns_bearish = ['evening_star', 'three_black_crows']
# patterns_df = dict.fromkeys(patterns)
identified_data_bullish = {pattern: [] for pattern in patterns_bullish}
identified_data_bearish = {pattern: [] for pattern in patterns_bearish}
stock_data = {}


def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


def load_all():
    stock_data['Apple'] = load_data('AAPL')
    stock_data['Google'] = load_data('GOOGL')
    stock_data['Amazon'] = load_data('AMZN')
    stock_data['Tesla'] = load_data('TSLA')

def main():

    load_all()

    pattern_data_bullish = []
    pattern_data_bearish = []

    for pattern in identified_data_bullish.keys():
        for company_name, df in stock_data.items():
            identified_data_bullish[pattern].extend(search(company_name, df, pattern))
            print(pattern, company_name)
        pattern_data_bullish.extend(identified_data_bullish[pattern])
    
    for pattern in identified_data_bearish.keys():
        for company_name, df in stock_data.items():
            identified_data_bearish[pattern].extend(search(company_name, df, pattern))
            print(pattern, company_name)
        pattern_data_bearish.extend(identified_data_bearish[pattern])
        
    # print(pattern_data_bullish)

    final_data_bullish = pd.DataFrame(pattern_data_bullish)
    final_data_bullish.to_csv("bullish_patterns.csv")
    final_data_bearish = pd.DataFrame(pattern_data_bearish)
    final_data_bearish.to_csv("bearish_patterns.csv")


if __name__ == "__main__":
    main()
