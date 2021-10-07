from datetime import date

import yfinance as yf
from identify_pattern import search

# date range for collecting data from START to TODAY
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

patterns = ['hammer', 'inv_hammer', 'engulfing', 'piercing_line', 'morning_star', 'white_soldiers', 'rising_method']
# patterns_df = dict.fromkeys(patterns)
identified_data = {pattern: [] for pattern in patterns}
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

    for pattern in identified_data.keys():
        for company_name, df in stock_data.items():
            identified_data[pattern].extend(search(company_name, df, pattern))
            print(pattern, company_name)


    print(identified_data['inv_hammer'])

if __name__ == "__main__":
    main()
