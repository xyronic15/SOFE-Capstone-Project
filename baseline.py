from datetime import date
import pandas as pd
import yfinance as yf
from dataloader import load_data

# date range for collecting data from START to TODAY
START = "2019-03-24"
END = "2019-04-25"

stock_data = {}

def load_all():
    
    companies = pd.read_csv('bats_symbols.csv', sep=",")
    for i in range(len(companies)):
        print("Loading stock " + companies.iloc[i,0])
        stock_data[companies.iloc[i,0]] = load_data(companies.iloc[i,0], START, END)

def get_data(df):

    # dict to be exported to csv
    data = []

    idx = 0

    data.append({'Date': df.iloc[idx, 0], 'Closing Price': df.iloc[idx, 4],
                'High after 1 day': df.iloc[min(idx+1, len(df)-1), 2], 'High after 2 days': df.iloc[min(idx+2, len(df)-1), 2],
                'High after 3 days': df.iloc[min(idx+3, len(df)-1), 2], 'High after 4 days': df.iloc[min(idx+4, len(df)-1), 2],
                'High after 5 days': df.iloc[min(idx+5, len(df)-1), 2], 'High after 6 days': df.iloc[min(idx+6, len(df)-1), 2],
                'High after 7 days': df.iloc[min(idx+7, len(df)-1), 2], 'High after 8 days': df.iloc[min(idx+8, len(df)-1), 2],
                'High after 9 days': df.iloc[min(idx+9, len(df)-1), 2], 'High after 10 days': df.iloc[min(idx+10, len(df)-1), 2],
                'High after 15 days': df.iloc[min(idx+15, len(df)-1), 2], 'High after 20 days': df.iloc[min(idx+20, len(df)-1), 2],
                'High after 25 days': df.iloc[min(idx+25, len(df)-1), 2], 'High after 30 days': df.iloc[min(idx+30, len(df)-1), 2],})
    
    return data


def main():

    load_all()

    data = []

    for company_name, df in stock_data.items():
        if not df.empty:
            data.extend(get_data(df))
            print("Processing " + company_name + "...")
    
    final_data = pd.DataFrame(data)
    final_data.to_csv("baseline.csv")



if __name__ == '__main__':
    main()