import numpy as np

def create_features(df):
    df = df.sort_values(["ticker","Datetime"])
    df["ret"] = df.groupby("ticker")["Close"].pct_change()
    df["vol"] = df.groupby("ticker")["ret"].rolling(24).std().reset_index(0,drop=True)
    df["vol_mean"] = df.groupby("ticker")["Volume"].rolling(24).mean().reset_index(0,drop=True)
    df["vol_spike"] = df["Volume"] / df["vol_mean"]
    delta = df.groupby("ticker")["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df["rsi"] = 100 - (100/(1+rs))
    return df