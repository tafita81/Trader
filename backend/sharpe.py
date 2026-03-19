import numpy as np

def sharpe_ratio(returns, risk_free_rate=0.0):
    excess = returns - risk_free_rate
    return np.mean(excess) / (np.std(excess) + 1e-9)


def optimize_sharpe(df):
    assets = df['ticker'].unique()
    best = None
    best_score = -999

    for w in np.linspace(0.1,1.0,10):
        weights = {a: w/len(assets) for a in assets}

        portfolio_returns = []

        for a in assets:
            r = df[df['ticker']==a]['ret'].dropna()
            if len(r)>0:
                portfolio_returns.append(r * weights[a])

        if len(portfolio_returns)==0:
            continue

        total = np.sum(portfolio_returns, axis=0)
        s = sharpe_ratio(total)

        if s > best_score:
            best_score = s
            best = weights

    return best, best_score