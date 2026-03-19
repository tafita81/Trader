# Modo Agressivo Controlado (Growth Mode)

SETTINGS = {
    "initial_capital": 100,
    "risk_per_trade": 0.03,  # 3%
    "max_drawdown": 0.10,
    "scale_rules": {
        200: 0.02,
        500: 0.015,
        1000: 0.01
    }
}


def adjust_risk(capital):
    for threshold, risk in sorted(SETTINGS["scale_rules"].items()):
        if capital >= threshold:
            current_risk = risk
    return current_risk if 'current_risk' in locals() else SETTINGS["risk_per_trade"]
