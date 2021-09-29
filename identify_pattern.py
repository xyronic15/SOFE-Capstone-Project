"""
1.) iterate through the dataframe
2.) identify a hammer candlestick
    2-1.) If it is a hammer -> check for downtrend 15 stocks before
    2-2.) Check direction of stock price for next 5 days
3.) Update whether after hammer price goes up or down
    3-1.) keep track of number times a hammer occurs
    3-2.) keep track of number of times price goes up in the upcoming 5 days
    3-3.) keep track of number of times price goes down in the upcoming 5 days
"""

# depth for determining previous trend direction
PREV_DEPTH = 15
# depth for determining upcoming trend direction
FUTURE_DEPTH = 5


def search(df):
    hammer_count = 0
    for idx in range(len(df)):
        if idx < PREV_DEPTH:
            continue
        print(df.iloc[idx, 'Close'])
        if (df.iloc[idx, 4] < sma(idx, df, PREV_DEPTH)).all():
            print('Checking for hammer')
            if hammer(idx, df.iloc[idx], sma(idx, df)):
                hammer_count += 1
                if sma(idx, )


# checks if candlestick matches hammer pattern
def hammer(i, data, body_avg):
    body_hi = max(data['Close'], data['Open'])
    body_lo = min(data['Close'], data['Open'])
    body = body_hi - body_lo
    small_body = bool(body < body_avg)
    down_shadow = data['Low'] - body_lo
    up_shadow = data['High'] - body_hi
    factor = 2.0
    shadow_percent = 5.0
    has_up_shadow = up_shadow > shadow_percent / 100 * body

    if (small_body and body and body_lo > (data['High'] + data['Low']) / 2
            and down_shadow >= factor * body and not has_up_shadow):
        print('HAMMER FOUND')


# checks if candlestick matches inverse hammer pattern
def inverse_hammer(i, data, body_avg):
    body_hi = max(data['Close'], data['Open'])
    body_lo = min(data['Close'], data['Open'])
    body = body_hi - body_lo
    small_body = bool(body < body_avg)
    down_shadow = data['Low'] - body_lo
    up_shadow = data['High'] - body_hi
    factor = 2.0
    shadow_percent = 5.0
    has_up_shadow = up_shadow > shadow_percent / 100 * body


# returns the moving average of the last n candlesticks
def sma(i, data, depth):
    cur = data.iloc[i - depth: i]
    trend_sum = 0.0

    for idx, row in cur.iterrows():
        trend_sum += row['Close']

    return trend_sum / depth
