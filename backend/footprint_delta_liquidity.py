# Footprint + Delta + Liquidity Engine
import numpy as np

# ===== FOOTPRINT (volume por preço) =====
def footprint(trades):
    # trades: (price, size, side)
    levels = {}
    for price, size, side in trades:
        if price not in levels:
            levels[price] = {"buy":0, "sell":0}
        if side == "BUY":
            levels[price]["buy"] += size
        else:
            levels[price]["sell"] += size
    return levels

# ===== DELTA (pressão líquida) =====
def delta(trades):
    buy = sum([t[1] for t in trades if t[2]=="BUY"])
    sell = sum([t[1] for t in trades if t[2]=="SELL"])
    return buy - sell

# ===== CVD (cumulative volume delta) =====
def update_cvd(prev_cvd, trades):
    return prev_cvd + delta(trades)

# ===== LIQUIDEZ (zonas prováveis de stop) =====
def detect_liquidity(highs, lows):
    # regiões onde preço testou várias vezes
    liquidity_zones = []

    for i in range(2, len(highs)):
        if highs[i] == highs[i-1] == highs[i-2]:
            liquidity_zones.append(("resistance", highs[i]))

    for i in range(2, len(lows)):
        if lows[i] == lows[i-1] == lows[i-2]:
            liquidity_zones.append(("support", lows[i]))

    return liquidity_zones

# ===== DECISÃO AVANÇADA =====
def institutional_decision(trades, highs, lows, prev_cvd):

    fp = footprint(trades)
    d = delta(trades)
    cvd = update_cvd(prev_cvd, trades)
    liquidity = detect_liquidity(highs, lows)

    # lógica simples
    if d > 0 and cvd > prev_cvd:
        return "BUY", cvd, liquidity

    if d < 0 and cvd < prev_cvd:
        return "SELL", cvd, liquidity

    return "SKIP", cvd, liquidity
