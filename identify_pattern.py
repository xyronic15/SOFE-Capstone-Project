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

# depth for determining upcoming trend direction
FUTURE_DEPTH = 10


# iterating through stock data to identify patterns
def search(name, df, pattern_type):

    # dataframe to hold identified candlesticks to be exported to csv after
    classified = []
    # print(pattern_type)


    for idx in range(len(df)):
        downtrend = df.iloc[idx, 4] < sma(idx, df, PREV_DEPTH_TREND)
        uptrend = df.iloc[idx, 4] > sma(idx, df, PREV_DEPTH_TREND)
        is_match = False
        if downtrend:
            if pattern_type == 'hammer':
                is_match = hammer(idx, df.iloc[idx], body_sma(idx, df, PREV_DEPTH_BODY_AVG))
            if pattern_type == 'inv_hammer':
                is_match = inv_hammer(idx, df.iloc[idx], body_sma(idx, df, PREV_DEPTH_BODY_AVG))
            if pattern_type == 'engulfing_bullish':
                is_match = engulfing_bullish(idx, df, body_sma(idx, df, PREV_DEPTH_BODY_AVG))
            if pattern_type == 'morning_star':
                is_match = morning_star(idx, df)

        if uptrend:
            if pattern_type == 'evening_star':
                is_match = evening_star(idx, df, body_sma(idx, df, PREV_DEPTH_BODY_AVG))
            if pattern_type == 'shooting_star':
                is_match = shooting_star(idx, df.iloc[idx], body_sma(idx, df, PREV_DEPTH_BODY_AVG))
            if pattern_type == 'bearish_engulfing':
                is_match = bearish_engulfing(idx, df, body_sma(idx, df, PREV_DEPTH_BODY_AVG))
            if pattern_type == 'hanging_man':
                is_match = hanging_man(idx, df.iloc[idx], body_sma(idx, df, PREV_DEPTH_BODY_AVG))
        
        if pattern_type == 'piercing':
            is_match = piercing_line(idx, df)
        if pattern_type == 'three_black_crows':
            is_match = three_black_crows(idx, df)
        if pattern_type == 'falling_three_methods':
            is_match = falling_three_methods(idx, df)
        if pattern_type == 'rising_three_methods':
            is_match = rising_three_methods(idx, df)
        if pattern_type == 'dark_cloud_cover':
            is_match = dark_cloud_cover(idx, df)
        if pattern_type == 'three_white_soldiers':
            is_match = three_white_soldiers(idx, df)
        if pattern_type == 'doji':
            is_match = doji(idx, df.iloc[idx])


        '''
        if is_match:
            classified.append({'Name': name, 'Date': df.iloc[idx, 0], 'Pattern': pattern_type, 'Closing Price': df.iloc[idx, 4],
                'High after 1 day': df.iloc[min(idx+1, len(df)-1), 2], 'High after 2 days': df.iloc[min(idx+2, len(df)-1), 2],
                'High after 3 days': df.iloc[min(idx+3, len(df)-1), 2], 'High after 4 days': df.iloc[min(idx+4, len(df)-1), 2],
                'High after 5 days': df.iloc[min(idx+5, len(df)-1), 2], 'High after 6 days': df.iloc[min(idx+6, len(df)-1), 2],
                'High after 7 days': df.iloc[min(idx+7, len(df)-1), 2], 'High after 8 days': df.iloc[min(idx+8, len(df)-1), 2],
                'High after 9 days': df.iloc[min(idx+9, len(df)-1), 2], 'High after 10 days': df.iloc[min(idx+10, len(df)-1), 2],})
        '''
        
        if is_match:
            classified.append(
                {'Date': df.iloc[idx, 0]})
        


    return classified


# Bullish patterns
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

    body_hi = [None] * 3
    body_lo = [None] * 3
    long_body = [None] * 3
    small_body = [None] * 3
    white_body = [None] * 3
    black_body = [None] * 3
    body_mid = [None] * 3

    for n in range(3):

        body_hi[n] = max(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body_lo[n] = min(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body = body_hi[n] - body_lo[n]
        body_avg = body_sma(i-n, data, PREV_DEPTH_BODY_AVG)
        long_body[n] = body > body_avg
        small_body[n] = body < body_avg
        white_body[n] = data.iloc[i-n, 1] < data.iloc[i-n, 4]
        black_body[n] = data.iloc[i-n, 1] > data.iloc[i-n, 4]
        body_mid[n] = (body / 2) + body_lo[n]

    if (long_body[2] and small_body[1] and long_body[0] and
            black_body[2] and body_hi[1] < body_lo[2] and white_body[0] and
            body_hi[0] >= body_mid[2] and body_hi[0] < body_hi[2] and
            body_hi[1] < body_lo[0]):
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
        white_body[n] = data.iloc[i-n, 1] < data.iloc[i-n, 4]
        ranges[n] = data.iloc[i-n, 2] - data.iloc[i-n, 3]
        up_shadows[n] = data.iloc[i-n, 2] - body_hi
        wsld_no_up_sh[n] = (ranges[n] * (up_shadow_percent / 100)) > up_shadows[n]
        open[n] = data.iloc[i-n, 1]
        close[n] = data.iloc[i-n, 4]

    if (long_body[0] and long_body[1] and long_body[2] and white_body[0] and white_body[1] and white_body[2] and
            close[0] > close[1] and close[1] > close[2] and open[0] < close[1] and open[0] > open[1] and open[1] < close[2] and
            open[1] > open[2] and wsld_no_up_sh[0] and wsld_no_up_sh[1] and wsld_no_up_sh[2]):
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
    prev_body_avg = body_sma(i-1, data, PREV_DEPTH_BODY_AVG)
    prev_small_body = prev_body < prev_body_avg

    if (white_body and long_body and prev_black_body and prev_small_body 
            and data.iloc[i, 4] >= data.iloc[i-1, 1] and data.iloc[i, 1] <= data.iloc[i-1, 4]
            and (data.iloc[i, 4] > data.iloc[i-1, 1] or data.iloc[i, 1] < data.iloc[i-1, 4])):
        return True

    return False


# checks if candlestick matches the piercing line pattern
def piercing_line(i, data):
    
    prev_downtrend = data.iloc[i-1, 4] < sma(i-1, data, PREV_DEPTH_TREND)
    prev_black_body = data.iloc[i-1, 1] > data.iloc[i-1, 4]
    prev_body_hi = max(data.iloc[i-1, 1], data.iloc[i-1, 4])
    prev_body_lo = min(data.iloc[i-1, 1], data.iloc[i-1, 4])
    prev_body = prev_body_hi - prev_body_lo
    prev_long_body = prev_body > body_sma(i-1, data, PREV_DEPTH_BODY_AVG)
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


# checks if candlestick matches rising three methods pattern
def rising_three_methods(i, data):

    longBody = [None] * 5
    upTrend = [None] * 5
    smallBody = [None] * 5
    black_body = [None] * 5
    white_body = [None] * 5
    open = [None] * 5
    close = [None] * 5
    low = [None] * 5
    high = [None] * 5
    		
    for n in range(5):
    
        body_hi = max(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body_lo = min(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body = body_hi - body_lo
        body_avg = body_sma(i-n, data, PREV_DEPTH_BODY_AVG)
        longBody[n] = body > body_avg
        upTrend[n] = data.iloc[i-n, 4] > body_avg
        smallBody[n] = body < body_avg
        white_body[n] = data.iloc[i-n, 1] < data.iloc[i-n, 4]
        black_body[n] = data.iloc[i-n, 1] > data.iloc[i-n, 4]
        open[n] = data.iloc[i-n, 1]
        close[n] = data.iloc[i-n, 4]
        low[n] = data.iloc[i-n, 3]
        high[n] = data.iloc[i-n, 2]
    
    if (upTrend[4] and (longBody[4] and white_body[4]) and
        (smallBody[3] and black_body[3] and open[3]<high[4] and close[3]>low[4]) and 
        (smallBody[2] and black_body[2] and open[2]<high[4] and close[2]>low[4]) and 
        (smallBody[1] and black_body[1] and open[1]<high[4] and close[1]>low[4]) and 
        (longBody[0] and white_body[0] and close[0]>close[4])):
	    return True
	
    return False


# Bearish patterns
# checks if the candlestick matches dark cloud cover
def dark_cloud_cover(i, data):

    longBody = [None] * 2
    upTrend = [None] * 2
    white_body = [None] * 2
    black_body = [None] * 2
    open = [None] * 2
    close = [None] * 2
    high = [None] * 2
    body_mid = [None] * 2
    		
    for n in range(2):
    
        body_hi = max(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body_lo = min(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body = body_hi - body_lo
        body_avg = body_sma(i-n, data, PREV_DEPTH_BODY_AVG)
        longBody[n] = body > body_avg
        upTrend[n] = data.iloc[i-n, 4] > body_avg
        white_body[n] = data.iloc[i-n, 1] < data.iloc[i-n, 4]
        black_body[n] = data.iloc[i-n, 1] > data.iloc[i-n, 4]
        open[n] = data.iloc[i-n, 1]
        close[n] = data.iloc[i-n, 4]
        high[n] = data.iloc[i-n, 2]
        body_mid[n] = (body_hi + body_lo) / 2
	
    if ((upTrend[1] and white_body[1] and longBody[1]) and 
        (black_body[0] and open[0] >= high[1] and close[0] < body_mid[1]
        and close[0] > open[1])):
        return True
                
    return False

# checks if the candlestick matches falling three methods
def falling_three_methods(i, data):
    
    longBody = [None] * 5
    downTrend = [None] * 5
    smallBody = [None] * 5
    black_body = [None] * 5
    white_body = [None] * 5
    open = [None] * 5
    close = [None] * 5
    low = [None] * 5
    high = [None] * 5
    		
    for n in range(5):
    
        body_hi = max(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body_lo = min(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body = body_hi - body_lo
        body_avg = body_sma(i-n, data, PREV_DEPTH_BODY_AVG)
        longBody[n] = body > body_avg
        downTrend[n] = data.iloc[i-n, 4] < body_avg
        smallBody[n] = body < body_avg
        white_body[n] = data.iloc[i-n, 1] < data.iloc[i-n, 4]
        black_body[n] = data.iloc[i-n, 1] > data.iloc[i-n, 4]
        open[n] = data.iloc[i-n, 1]
        close[n] = data.iloc[i-n, 4]
        low[n] = data.iloc[i-n, 3]
        high[n] = data.iloc[i-n, 2]
    
    if (downTrend[4] and (longBody[4] and black_body[4]) and 
        (smallBody[3] and white_body[3] and open[3]>low[4] and close[3]<high[4]) and 
        (smallBody[2] and white_body[2] and open[2]>low[4] and close[2]<high[4]) and 
        (smallBody[1] and white_body[1] and open[1]>low[4] and close[1]<high[4]) and 
        (longBody[0] and black_body[0] and close<close[4])):
	    return True
	
    return False


# checks if the candlestick matches evening star pattern
def evening_star(i, data, body_avg):

    prev2_body_hi = max(data.iloc[i-2, 1], data.iloc[i-2, 4])
    prev2_body_lo = min(data.iloc[i-2, 1], data.iloc[i-2, 4])
    prev2_body = prev2_body_hi - prev2_body_lo
    prev2_long_body = prev2_body > body_sma(i-2, data, PREV_DEPTH_BODY_AVG)
    prev_body_hi = max(data.iloc[i-1, 1], data.iloc[i-1, 4])
    prev_body_lo = min(data.iloc[i-1, 1], data.iloc[i-1, 4])
    prev_body = prev_body_hi - prev_body_lo
    prev_small_body = prev_body < body_sma(i-1, data, PREV_DEPTH_BODY_AVG)
    body_hi = max(data.iloc[i, 1], data.iloc[i, 4])
    body_lo = min(data.iloc[i, 1], data.iloc[i, 4])
    body = body_hi - body_lo
    long_body = body > body_avg
    prev2_white_body = data.iloc[i-2, 1] < data.iloc[i-2, 4]
    black_body = data.iloc[i, 1] > data.iloc[i, 4]

    if (prev2_long_body and prev_small_body and long_body and prev2_white_body and
            prev_body_lo > prev2_body_hi and black_body and body_lo <= ((prev2_body/2) + prev2_body_lo) and 
            body_lo > prev2_body_lo and prev_body_lo > body_hi):
        return True

    return False 


def three_black_crows(i, data):

    long_bodies = [None] * 3
    black_bodies = [None] * 3
    ranges = [None] * 3
    dn_shadows = [None] * 3
    bcrw_no_dn_sh = [None] * 3
    dn_shadow_percent = 5.0
    open = [None] * 3
    close = [None] * 3

    for n in range(3):

        body_hi = max(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body_lo = min(data.iloc[i-n, 1], data.iloc[i-n, 4])
        body = body_hi - body_lo
        body_avg = body_sma(i-n, data, PREV_DEPTH_BODY_AVG)
        long_bodies[n] = body > body_avg
        black_bodies[n] = data.iloc[i-n, 1] > data.iloc[i-n, 4]
        ranges[n] = data.iloc[i-n, 2] - data.iloc[i-n, 3]
        dn_shadows[n] = body_lo - data.iloc[i-n, 3]
        bcrw_no_dn_sh[n] = (ranges[n] * (dn_shadow_percent / 100)) > dn_shadows[n]
        open[n] = data.iloc[i-n, 1]
        close[n] = data.iloc[i-n, 4]

    if (long_bodies[0] and long_bodies[1] and long_bodies[2] and black_bodies[0] and black_bodies[1] and black_bodies[2] and
            close[0] < close[1] and close[1] < close[2] and open[0] > close[1] and open[0] < open[1] and open[1] > close[2] and
            open[1] < open[2] and bcrw_no_dn_sh[0] and bcrw_no_dn_sh[1] and bcrw_no_dn_sh[2]):
        return True

    return False


# bearish shooting star

def shooting_star(i, data, body_avg):

    body_hi = max(data['Close'], data['Open'])
    body_lo = min(data['Close'], data['Open'])
    body = body_hi - body_lo
    small_body = bool(body < body_avg)
    down_shadow = body_lo - data['Low']
    up_shadow = data['High'] - body_hi
    factor = 2.0
    shadow_percent = 5.0
    has_down_shadow = down_shadow > shadow_percent / 100 * body

    if (small_body and body and body_hi < (data['High'] + data['Low']) / 2
            and up_shadow >= factor * body and not has_down_shadow):
        return True

    return False


# bearish engulfing

def bearish_engulfing(i, data, body_avg):

    black_body = data.iloc[i, 1] > data.iloc[i, 4]
    body_hi = max(data.iloc[i, 1], data.iloc[i, 4])
    body_lo = min(data.iloc[i, 1], data.iloc[i, 4])
    body = body_hi - body_lo
    long_body = body > body_avg

    prev_white_body = data.iloc[i - 1, 1] < data.iloc[i - 1, 4]
    prev_hi = max(data.iloc[i - 1, 1], data.iloc[i - 1, 4])
    prev_lo = min(data.iloc[i - 1, 1], data.iloc[i - 1, 4])
    prev_body = prev_hi - prev_lo
    prev_body_avg = body_sma(i - 1, data, PREV_DEPTH_BODY_AVG)
    prev_small_body = prev_body < prev_body_avg

    if (black_body and long_body and prev_white_body and prev_small_body
            and data.iloc[i, 4] <= data.iloc[i - 1, 1] and
            data.iloc[i, 1] >= data.iloc[i - 1, 4] and
            (data.iloc[i, 4] < data.iloc[i - 1, 1] or
             data.iloc[i, 1] > data.iloc[i, 4])):
        return True

    return False

# checks if candlestick matches hanging man pattern
def hanging_man(i, data, body_avg):

    body_hi = max(data['Close'], data['Open'])
    body_lo = min(data['Close'], data['Open'])
    body = body_hi - body_lo
    shadow_percent = 5
    factor = 2.0
    small_body = body < body_avg
    hl2 = (data['High'] + data['Low']) / 2
    down_shadow = body_lo - data['Low']
    up_shadow = data['High'] - body_hi
    has_up_shadow = up_shadow > ((shadow_percent / 100) * body)

    if (small_body and body > 0 and body_lo > hl2 and down_shadow >= (factor * body) and not has_up_shadow):
        return True

    return False

# checks if candlestick matches doji pattern
def doji(i, data):

    body_hi = max(data['Close'], data['Open'])
    body_lo = min(data['Close'], data['Open'])
    body = body_hi - body_lo
    up_shadow = data['High'] - body_hi
    down_shadow = body_lo - data['Low']
    range = data['High'] - data['Low']
    doji_body_percent = 5.0
    shadow_equals_percent = 100.0
    shadow_equals = (up_shadow == down_shadow) or (abs(up_shadow - down_shadow) / (down_shadow * 100)) < shadow_equals_percent and (abs(down_shadow - up_shadow) / (up_shadow * 100)) < shadow_equals_percent
    is_doji_body = range > 0 and body <= (range * (doji_body_percent / 100))
    dragonfly_doji = is_doji_body and up_shadow <= body
    gravestone_doji_one = is_doji_body and down_shadow <= body
    doji = is_doji_body and shadow_equals

    if doji and not dragonfly_doji and not gravestone_doji_one:
        return True

    return False


# Helper functions
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
