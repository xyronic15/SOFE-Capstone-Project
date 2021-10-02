"""
Data Frame:
    0 => date
    1 => open
    2 => high
    3 => low
    4 => close
    5 => adj close
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

        downtrend = df.iloc[idx, 4] < sma(idx, df, PREV_DEPTH)
        is_hammer = hammer(idx, df.iloc[idx], sma(idx, df, PREV_DEPTH))

        if downtrend:
            if is_hammer:
                hammer_count += 1
                df['Pattern'] = 'Hammer'

    print(hammer_count)


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


# returns the moving average of the last n candlesticks
def sma(i, data, depth):
    cur = data.iloc[i - depth: i]
    trend_sum = 0.0

    for idx, row in cur.iterrows():
        trend_sum += row['Close']

    return trend_sum / depth
