def scale(value, from_low, from_high, to_low, to_high):
    from_delta = from_high - from_low
    to_delta = to_high - to_low
    pct = (value - from_low) / from_delta
    return pct * to_delta + to_low
