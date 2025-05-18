export function scale(value: number, fromLow: number, fromHigh: number, toLow: number, toHigh: number): number {
    const fromDelta = fromHigh - fromLow;
    const toDelta = toHigh - toLow;
    const pct = (value - fromLow) / fromDelta;
    return pct * toDelta + toLow;
}
