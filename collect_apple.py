import pandas as pd

from dataloader import load_data

# get pandas dataframe of apple history
apple = load_data('AAPL')

# Get moving average for closing prices
apple['SMA-Close'] = apple.iloc[:,4].rolling(window=50).mean()
apple['SMA-Adj Close'] = apple.iloc[:,5].rolling(window=50).mean()
apple['Dtrend-Close'] = apple.iloc[:,3] < apple.iloc[:,7]
apple['Dtrend-Adj Close'] = apple.iloc[:,3] < apple.iloc[:,8]

# get information on body of the candlestick
apple['Body Hi'] = apple[['Open', 'Close']].max(axis=1)
apple['Body Lo'] = apple[['Open', 'Close']].min(axis=1)
apple['Body'] = apple['Body Hi'] - apple['Body Lo']
apple['EMA-Body'] = apple.iloc[:,11].ewm(span=14).mean()

# trackers
hammer_count = 0
# is_hammer = False

for i in range(len(apple)):

    if apple.iloc[i, 9]:
        # get values
        c_smallbody = apple.iloc[i, 13] < apple.iloc[i, 14]
        c_body = apple.iloc[i, 13]
        c_bodylo = apple.iloc[i, 12]
        c_low = apple.iloc[i, 3]
        c_bodyhi = apple.iloc[i, 11]
        c_hi = apple.iloc[i, 2]
        c_mid = (apple.iloc[i, 2] + apple.iloc[i, 3]) / 2
        c_factor = 2
        c_tail = c_bodylo - c_low
        c_head = c_hi - c_bodyhi
        c_has_head = c_head > (0.05 * c_body)

        # final check if it is a hammer
        if c_smallbody and c_body > 0 and c_body > c_mid and c_tail > c_factor * c_body and not c_has_head:
            hammer_count += 1

# print num of hammers
print("Number of hammers in list: " + str(hammer_count))


# display last 50 rows
# print(apple['Dtrend-Close'].tail(50))