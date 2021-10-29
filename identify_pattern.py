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


# iterating through stock data to identify paterns
def search(df):

    # dictionary to hold candlesticks that fit a pattern
    classified = {}
    hammer_count = 0
    morning_star_count = 0
    three_white_soldiers_count = 0
    hanging_man_count = 0
    doji_count = 0


    for idx in range(len(df)):
        if idx < PREV_DEPTH:
            continue

        downtrend = df.iloc[idx, 4] < sma(idx, df, PREV_DEPTH)
        is_hammer = hammer(idx, df.iloc[idx], sma(idx, df, PREV_DEPTH))
        is_morning_star = morning_star(idx, df.iloc[idx], sma(idx, df, PREV_DEPTH))
        is_three_white_soldiers = three_white_soldiers(idx, df.iloc[idx], sma(idx, df, PREV_DEPTH))

        if downtrend:
            if is_hammer:
                hammer_count += 1
                #df['Pattern'] = 'Hammer'
                #classified[idx] = 'Hammer'

            if is_morning_star:
                morning_star_count += 1

            if  is_three_white_soldiers:
                 three_white_soldiers_count += 1

        if uptrend:
            if  hanging_man:
                hanging_man_count += 1

            if  doji:
                doji_count += 1

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

# checks if candlestick matches morning star pattern
def morning_star(i, data):

    for n in range(3):

        body_hi = max(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body_lo = min(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body = body_hi - body_lo
        body_avg = body_sma(i-n, data, PREV_DEPTH_BODY_AVG)
        long_body[n] = body > body_avg
        prev_downtrend[n] = data ['Close'] < body_avg
        small_body[n] = body < body_avg
        white_body = data.iloc[i-n, 1] < data.iloc[i-n, 4]
        prev_black_body[n] = data.iloc[i-n, 1] > data.iloc[i-n, 4]
        body_middle[n] = body / 2 + body_lo

        if (long_body[2] and small_body[1] and long_body and prev_downtrend and prev_black_body[2] and
                body_hi[1] < body_lo[2] and white_body and body_hi >= body_middle[2] and body_hi < body_hi[2] and
                body_hi[1] < body_lo):
            return True

        return False

# checks if candlestick matches three white soldiers pattern
def three_white_soldiers(i, data):

    long_body = [None] * 3
    white_body = [None] * 3
    ranges = [None] * 3
    up_shadows = [None] * 3
    wsld_no_up_sh = [None] * 3
    up_shadow_percent = 5.0
    open = [None] * 3
    close = [None] * 3

    for n in range(3):

        body_hi = max(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body_lo = min(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body = body_hi - body_lo
        body_avg = body_sma(i-n, data, PREV_DEPTH_BODY_AVG)
        long_body[n] = body > body_avg
        white_body = data.iloc[i-n, 1] < data.iloc[i-n, 4]
        ranges[n] = data.iloc[i-n, 2] - data.iloc[i-n, 3]
        up_shadows[n] = data.iloc[i-n, 2] - body_hi
        wsld_no_up_sh[n] = (ranges[n] * (up_shadow_percent / 100)) > up_shadows[n]
        open[n] = data.iloc[i-n, 1]
        close[n] = data.iloc[i-n, 4]

        if (long_body and long_body[1] and long_body[2] and white_body and white_body[1] and white_body[2] and
                close > close[1] and close[1] > close[2] and open < close[1] and open > open[1] and open[1] < close[2] and
                open[1] > open[2] and wsld_no_up_sh and wsld_no_up_sh[1] and wsld_no_up_sh[2]):
            return True

        return False

# checks if candlestick matches hanging man pattern
def hanging_man(i, data, body_avg):

    body_hi = max(data.iloc[i, 1], data.iloc[i, 4])
    body_lo = min(data.iloc[i, 1], data.iloc[i, 4])
    body = body_hi - body_lo
    shadow_percent = 5
    factor = 2.0
    small_body = body < body_avg
    down_shadow = body_lo - data['Low']
    uptrend = data ['Close'] > body_avg
    up_shadow = data ['High'] - body_hi
    has_up_shadow = up_shadow > shadow_percent / 100 * body

    if uptrend and (small_body and body > 0 and body_lo > hl2 and down_shadow >= factor * body and not has_up_shadow):
        return True

    return False

# checks if candlestick matches doji pattern
def doji(i, data):

    body_hi = max(data.iloc[i, 1], data.iloc[i, 4])
    body_lo = min(data.iloc[i, 1], data.iloc[i, 4])
    body = body_hi - body_lo
    up_shadow = data ['High'] - body_hi
    down_shadow = body_lo - data['low']
    ranges = data['High'] - data['Low']
    doji_body_percent = 5.0
    shadow_equals_percent = 100.0
    shadow_equals = up_shadow == down_shadow or (abs(up_shadow - down_shadow) / down_shadow * 100) < shadow_equals_percent and (abs(down_shadow - up_shadow) / up_shadow * 100) < shadow_equals_percent
    is_doji_body = ranges > 0 and body <= ranges * doji_body_percent / 100
    dragonfly_doji = is_doji_body and up_shadow <= body
    gravestone_doji_one = is_doji_body and down_shadow <= body
    doji = is_doji_body and shadow_equals

    if doji and not dragonfly_doji and not gravestone_doji_one:
        return True

    return False

# returns the moving average of the last n candlesticks
def sma(i, data, depth):

    cur = data.iloc[i - depth: i]
    trend_sum = 0.0

    for idx, row in cur.iterrows():
        trend_sum += row['Close']

    return trend_sum / depth
