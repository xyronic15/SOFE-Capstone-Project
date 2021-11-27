import datetime
import pandas as pd
import yfinance as yf
from dataloader import load_data
import random
import numpy as np

# date range for collecting data from START to TODAY
START = datetime.date(2015, 1, 1)
END = datetime.date.today()

stock_data = {}
dates = []

def load_all():
    
    companies = pd.read_csv('bats_symbols.csv', sep=",")
    for i in range(len(companies)):
        print("Loading stock " + companies.iloc[i,0])
        stock_data[companies.iloc[i,0]] = load_data(companies.iloc[i,0], START.strftime("%Y-%m-%d"), END.strftime("%Y-%m-%d"))

def get_data(df, start):

    # dict to be exported to csv
    data = []

    if df.loc[df['Date']==np.datetime64(start)].any().all():
        idx = int(df.index[df['Date']==np.datetime64(start)][0])
        print(idx)
    else:
        return data

    data.append({'Date': df.iloc[idx, 0], 'Closing Price': df.iloc[idx, 4],
                'High after 1 day': df.iloc[min(idx+1, len(df)-1), 2], 'High after 2 days': df.iloc[min(idx+2, len(df)-1), 2],
                'High after 3 days': df.iloc[min(idx+3, len(df)-1), 2], 'High after 4 days': df.iloc[min(idx+4, len(df)-1), 2],
                'High after 5 days': df.iloc[min(idx+5, len(df)-1), 2], 'High after 6 days': df.iloc[min(idx+6, len(df)-1), 2],
                'High after 7 days': df.iloc[min(idx+7, len(df)-1), 2], 'High after 8 days': df.iloc[min(idx+8, len(df)-1), 2],
                'High after 9 days': df.iloc[min(idx+9, len(df)-1), 2], 'High after 10 days': df.iloc[min(idx+10, len(df)-1), 2],
                'High after 15 days': df.iloc[min(idx+15, len(df)-1), 2], 'High after 20 days': df.iloc[min(idx+20, len(df)-1), 2],
                'High after 25 days': df.iloc[min(idx+25, len(df)-1), 2], 'High after 30 days': df.iloc[min(idx+30, len(df)-1), 2],})
    
    return data

def generate_dates():

    time_between_dates = END - START
    days_between_dates = time_between_dates.days

    for i in range(500):
        random_number_days = random.randrange(days_between_dates)
        random_start_date = START + datetime.timedelta(days=random_number_days)
        random_end_date = random_start_date + datetime.timedelta(days=31)

        dates.append((random_start_date, random_end_date))

def main():

    data = []

    load_all()
    generate_dates()

    for start, end in dates:
        for company_name, df in stock_data.items():
            if not df.empty:
                print("Processing " + company_name + " from date " + start.strftime("%Y-%m-%d"))
                new_data = get_data(df, start)
                if new_data:
                    data.extend(new_data)
                else:
                    print("Could not get data...")

    print("Saving CSV file...")
    
    final_data = pd.DataFrame(data)
    final_data.to_csv("baseline.csv")



if __name__ == '__main__':
    main()