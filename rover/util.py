def scale(value, fromLow, fromHigh, toLow, toHigh):
    fromDelta = fromHigh - fromLow
    toDelta = toHigh - toLow
    pct = (value - fromLow) / fromDelta
    return pct * toDelta + toLow
