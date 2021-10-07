import pandas as pd

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
# depth for determining previous body average
PREV_DEPTH_BODY_AVG = 14

# depth for determining the trend direction
PREV_DEPTH_TREND = 50

<<<<<<< HEAD
# depth for determining previous trend direction
PREV_DEPTH = 14
=======
>>>>>>> main
# depth for determining upcoming trend direction
FUTURE_DEPTH = 10


# iterating through stock data to identify patterns
def search(name, df, pattern_type):

<<<<<<< HEAD
    # dictionary to hold candlesticks that fit a pattern
    # classified = {}
    dates = pd.DataFrame(columns=['Date'])
    hammer_count = 0
    engulfing_count = 0
    piercing_count = 0

    for idx in range(len(df)):
        if idx < PREV_DEPTH + 1:
            continue

        downtrend = df.iloc[idx, 4] < sma(idx, df, 50)
        is_hammer = hammer(idx, df.iloc[idx], sma(idx, df, PREV_DEPTH))
        # is_engulfing = engulfing_bullish(idx, df, body_ema(idx, df, PREV_DEPTH))
        is_piercing = piercing_line(idx, df)

        if downtrend:
            if is_hammer:
                hammer_count += 1
                #df['Pattern'] = 'Hammer'
                #classified[idx] = 'Hammer'
            # if is_engulfing:
            #     engulfing_count += 1
            #     dates = dates.append({'Date': df.iloc[idx, 0]}, ignore_index=True)        
        
        if is_piercing:
            piercing_count += 1
            dates = dates.append({'Date': df.iloc[idx, 0]}, ignore_index=True)

    return dates



=======
    # dataframe to hold identified candlesticks to be exported to csv after
    classified = []

    for idx in range(len(df)):
        downtrend = df.iloc[idx, 4] < sma(idx, df, PREV_DEPTH_TREND)
        is_match = False
        if downtrend:
            if pattern_type == 'hammer':
                is_match = hammer(idx, df.iloc[idx], sma(idx, df, PREV_DEPTH_BODY_AVG))
            if pattern_type == 'inv_hammer':
                is_match = inv_hammer(idx, df.iloc[idx], sma(idx, df, PREV_DEPTH_BODY_AVG))

            if is_match:
                classified.append({'Name': name, 'Date': df.iloc[idx, 0], 'Closing Price': df.iloc[idx, 4]})

    return classified
>>>>>>> main


# checks if candlestick matches hammer pattern
def hammer(i, data, body_avg):

    body_hi = max(data['Close'], data['Open'])
    body_lo = min(data['Close'], data['Open'])
    body = body_hi - body_lo
    small_body = bool(body < body_avg)
    down_shadow = body_lo - data['Low']
    up_shadow = data['High'] - body_hi
    factor = 2.0
    shadow_percent = 5.0
    has_up_shadow = up_shadow > shadow_percent / 100 * body

    if (small_body and body and body_lo > (data['High'] + data['Low']) / 2
            and down_shadow >= factor * body and not has_up_shadow):
        return True

    return False

# checks if candlestick matches the engulfing bullish pattern
def engulfing_bullish(i, data, body_avg):

    white_body = data.iloc[i, 1] < data.iloc[i, 4]
    body_hi = max(data.iloc[i, 1], data.iloc[i, 4])
    body_lo = min(data.iloc[i, 1], data.iloc[i, 4])
    body = body_hi - body_lo
    long_body = body > body_avg
    prev_black_body = data.iloc[i-1, 1] > data.iloc[i-1, 4]
    prev_body_hi = max(data.iloc[i-1, 1], data.iloc[i-1, 4])
    prev_body_lo = min(data.iloc[i-1, 1], data.iloc[i-1, 4])
    prev_body = prev_body_hi - prev_body_lo
    prev_body_avg = body_ema(i-1, data, PREV_DEPTH)
    prev_small_body = prev_body < prev_body_avg

    if (white_body and long_body and prev_black_body and prev_small_body 
            and data.iloc[i, 4] >= data.iloc[i-1, 1] and data.iloc[i, 1] <= data.iloc[i-1, 4]
            and (data.iloc[i, 4] > data.iloc[i-1, 1] or data.iloc[i, 1] < data.iloc[i-1, 4])):
        return True

    return False

# checks if candlestick matches the piercing line pattern
def piercing_line(i, data):
    
    prev_downtrend = data.iloc[i-1, 4] < sma(i-1, data, PREV_DEPTH)
    prev_black_body = data.iloc[i-1, 1] > data.iloc[i-1, 4]
    prev_body_hi = max(data.iloc[i-1, 1], data.iloc[i-1, 4])
    prev_body_lo = min(data.iloc[i-1, 1], data.iloc[i-1, 4])
    prev_body = prev_body_hi - prev_body_lo
    prev_long_body = prev_body > body_ema(i-1, data, PREV_DEPTH)
    white_body = data.iloc[i, 1] < data.iloc[i, 4]
    prev_mid = (prev_body / 2) + prev_body_lo

    if ((prev_downtrend and prev_black_body and prev_long_body) and 
            (white_body and data.iloc[i, 1] <= data.iloc[i-1, 3] and 
            data.iloc[i, 4] > prev_mid and data.iloc[i, 4] < data.iloc[i-1, 1])):
        return True
    
    return False

# checks if candlestick matches inverted hammer pattern
def inv_hammer(i, data, body_avg):

    body_hi = max(data['Close'], data['Open'])
    body_lo = min(data['Close'], data['Open'])
    body = body_hi - body_lo
    small_body = bool(body < body_avg)
    down_shadow = body_lo - data['Low']
    up_shadow = data['High'] - body_hi
    factor = 2.0
    shadow_percent = 5.0
    has_up_shadow = up_shadow > shadow_percent / 100 * body

    if (small_body and body and body_hi < (data['High'] + data['Low']) / 2
            and up_shadow >= factor * body and not down_shadow):
        return True

    return False


# returns the moving average of the last n candlesticks for finding downtrend
def sma(i, data, depth):

    cur = data.iloc[i - depth: i]
    trend_sum = 0.0

    for idx, row in cur.iterrows():
        trend_sum += row['Close']

    return trend_sum / depth


def body_sma(i, data, depth):
    
    cur = data.iloc[i - depth: i]
    # print(cur.head(5))
    trend_sum = 0.0

    for idx, row in cur.iterrows():

        body_hi = max(row['Close'], row['Open'])
        body_lo = min(row['Close'], row['Open'])
        body = body_hi - body_lo

        trend_sum += body

    return trend_sum / depth

def body_ema(i, data, depth):
    
    cur = data.iloc[i - depth: i]
    # print(data.iloc[i - depth: i])
    body_list = []
    trend_sum = 0.0

    for idx, row in cur.iterrows():

        body_hi = max(row['Close'], row['Open'])
        body_lo = min(row['Close'], row['Open'])
        body = body_hi - body_lo

        body_list.append(body)
    
    # print(body_list)
    bodies = pd.DataFrame({'Body': body_list})

    return bodies['Body'].ewm(span=len(body_list)).mean()[len(body_list)-1]