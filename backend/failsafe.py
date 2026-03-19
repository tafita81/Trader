import numpy as np

def check_system_health(equity_curve):
    if len(equity_curve) == 0:
        return "OK"
    peak = np.maximum.accumulate(equity_curve)
    dd = (equity_curve - peak) / (peak + 1e-9)
    max_dd = float(dd.min())
    if max_dd < -0.10:
        return "STOP"
    return "OK"