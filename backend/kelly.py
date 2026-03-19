import numpy as np

def kelly_fraction(p, b):
    # p = prob. de ganho, b = payoff (ganho/perda)
    return max(0.0, (p*(b+1)-1)/b) if b>0 else 0.0


def estimate_edge(df):
    # estima p e b a partir do histórico 1h (13 meses)
    r = df['ret'].dropna()
    wins = r[r>0]
    losses = -r[r<0]

    p = len(wins) / max(1, len(r))
    avg_win = wins.mean() if len(wins)>0 else 0.0
    avg_loss = losses.mean() if len(losses)>0 else 1e-6
    b = avg_win / (avg_loss + 1e-9)

    return float(p), float(b)


def kelly_allocation(df, capital):
    alloc = {}
    for t in df['ticker'].unique():
        d = df[df['ticker']==t]
        p, b = estimate_edge(d)
        f = kelly_fraction(p, b)
        # fração conservadora (half-kelly)
        f = 0.5 * f
        alloc[t] = capital * f
    return alloc