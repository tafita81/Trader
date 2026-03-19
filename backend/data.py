import yfinance as yf
import pandas as pd

TICKERS = ["LIT","URNM","URA","COPX","REMX","SMH","SOXX"]

def get_data():
    df = yf.download(
        TICKERS,
        period="13mo",
        interval="1h",
        group_by="ticker",
        auto_adjust=True,
        progress=False
    )

    frames = []

    for t in TICKERS:
        temp = df[t].copy()
        temp["ticker"] = t
        temp.reset_index(inplace=True)
        frames.append(temp)

    return pd.concat(frames)