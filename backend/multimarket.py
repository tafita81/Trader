# Multi-mercado: ações (Yahoo) + cripto (Binance via requests)
import pandas as pd
import yfinance as yf
import requests

STOCKS = ["LIT","ALB","SQM"]
CRYPTO = ["BTCUSDT","ETHUSDT"]


def get_stocks():
    df = yf.download(STOCKS, period="13mo", interval="1h", group_by="ticker", auto_adjust=True, progress=False)
    frames = []
    for t in STOCKS:
        tmp = df[t].copy()
        tmp["ticker"] = t
        tmp.reset_index(inplace=True)
        frames.append(tmp)
    return pd.concat(frames)


def get_crypto():
    frames = []
    for sym in CRYPTO:
        url = f"https://api.binance.com/api/v3/klines?symbol={sym}&interval=1h&limit=1000"
        data = requests.get(url, timeout=10).json()
        df = pd.DataFrame(data, columns=["open_time","Open","High","Low","Close","Volume","close_time","qav","trades","tbbav","tbqav","ignore"])
        df["Datetime"] = pd.to_datetime(df["open_time"], unit="ms")
        for c in ["Open","High","Low","Close","Volume"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df["ticker"] = sym
        frames.append(df[["Datetime","Open","High","Low","Close","Volume","ticker"]])
    return pd.concat(frames)


def get_all_markets():
    s = get_stocks()
    c = get_crypto()
    return pd.concat([s, c], ignore_index=True)