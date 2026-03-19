import numpy as np

def optimize_portfolio(ranking, capital=10000):
    scores = ranking["score"].values
    scores = np.maximum(scores, 0)

    if scores.sum() == 0:
        weights = np.ones(len(scores)) / len(scores)
    else:
        weights = scores / scores.sum()

    allocation = {}

    for i, row in ranking.iterrows():
        allocation[row["ticker"]] = capital * weights[i]

    return allocation