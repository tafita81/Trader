def generate_signals(df):
    df["buy"] = (
        (df["vol_spike"] > 2) &
        (df["rsi"] < 30) &
        (df["regime"] == "capitulation")
    )
    df["sell"] = (
        (df["rsi"] > 70) |
        (df["regime"] == "euphoria")
    )
    return df