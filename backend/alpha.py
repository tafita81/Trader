import pandas as pd

def compute_alpha(df):
    df["score"] = (-df["rsi"]/100 + df["vol_spike"]/10 - df["zscore"]/5)
    return df

def rank_assets(df):
    latest = df.sort_values("Datetime").groupby("ticker").tail(1)
    ranking = latest.sort_values("score", ascending=False)
    return ranking[["ticker","score","Close"]]