import numpy as np

def detect_regime(df):
    df["zscore"] = (df["ret"] - df["ret"].rolling(50).mean()) / df["ret"].rolling(50).std()
    df["regime"] = np.where(df["zscore"] < -2, "capitulation", np.where(df["zscore"] > 2, "euphoria", "normal"))
    return df