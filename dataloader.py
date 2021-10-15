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

    for pattern in identified_data_bullish.keys():
        for company_name, df in stock_data.items():
            identified_data_bullish[pattern].extend(search(company_name, df, pattern))
            print(pattern, company_name)

    # for i in range(len(identified_data['inv_hammer'])):

    #     print(identified_data['inv_hammer'][i])

    pattern_data_bullish = []
    for pattern in identified_data_bullish.keys():

        # file_name = pattern + "_pattern.csv"
        # pattern_data_bullish = pd.DataFrame(identified_data_bullish[pattern])
        # pattern_data.to_csv(file_name)

        pattern_data_bullish.extend(identified_data_bullish[pattern])
    
    # print(pattern_data_bullish)

    final_data_bullish = pd.DataFrame(pattern_data_bullish)
    final_data_bullish.to_csv("bullish_patterns.csv")


if __name__ == "__main__":
    main()
