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

# depth for determining upcoming trend direction
FUTURE_DEPTH = 10


# iterating through stock data to identify patterns
def search(name, df, pattern_type):

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
