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