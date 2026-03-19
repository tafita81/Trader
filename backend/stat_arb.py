# Statistical Arbitrage (pairs trading simplificado)
import pandas as pd
import numpy as np


def compute_spread(df, t1, t2):
    a = df[df['ticker']==t1].set_index('Datetime')['Close']
    b = df[df['ticker']==t2].set_index('Datetime')['Close']

    aligned = pd.concat([a, b], axis=1).dropna()
    aligned.columns = ['A','B']

    spread = aligned['A'] - aligned['B']
    z = (spread - spread.mean()) / (spread.std() + 1e-9)

    return aligned, z


def pairs_signal(df, t1, t2):
    aligned, z = compute_spread(df, t1, t2)

    signal = pd.Series(0, index=aligned.index)

    signal[z > 2] = -1
    signal[z < -2] = 1

    return signal


def pairs_trade_decision(df):
    tickers = df['ticker'].unique()

    if len(tickers) < 2:
        return None

    t1, t2 = tickers[:2]

    signal = pairs_signal(df, t1, t2)

    last = signal.iloc[-1]

    if last == 1:
        return f"LONG {t1} / SHORT {t2}"
    elif last == -1:
        return f"SHORT {t1} / LONG {t2}"

    return None