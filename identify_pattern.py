"""
Data Frame:
    0 => date
    1 => open
    2 => high
    3 => low
    4 => close
    5 => adj close
"""
import pandas
from hammer_pattern import hammer
from inverse_hammer_pattern import inv_hammer

# depth for determining previous trend direction
PREV_DEPTH = 14
# depth for determining upcoming trend direction
FUTURE_DEPTH = 5


# iterating through stock data to identify paterns
def search(df):

    # dictionary to hold candlesticks that fit a pattern
    classified = {}
    hammer_count = 0
    inv_hammer_count = 0

    for idx in range(len(df)):
        if idx < PREV_DEPTH:
            continue

        downtrend = df.iloc[idx, 4] < sma(idx, df, PREV_DEPTH)
        is_hammer = hammer(idx, df.iloc[idx], sma(idx, df, PREV_DEPTH))
        is_inv_hammer = inv_hammer(idx, df.iloc[idx], sma(idx, df, PREV_DEPTH))

        if downtrend:
            if is_hammer:
                hammer_count += 1
            if is_inv_hammer:
                inv_hammer_count += 1


# returns the moving average of the last n candlesticks
def sma(i, data, depth):

    cur = data.iloc[i - depth: i]
    trend_sum = 0.0

    for idx, row in cur.iterrows():
        trend_sum += row['Close']

    return trend_sum / depth
