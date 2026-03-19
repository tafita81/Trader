# IA Global Multi-Mercado com Auto-Alocação de Capital
# - Analisa múltiplos mercados
# - Detecta regimes
# - Distribui capital dinamicamente

import numpy as np

class GlobalAllocator:

    def __init__(self):
        self.weights = {}

    def compute_scores(self, data_dict):
        scores = {}

        for market, df in data_dict.items():

            ret = df['ret'].mean()
            vol = df['ret'].std()

            sharpe = ret / (vol + 1e-9)

            momentum = df['Close'].pct_change(20).iloc[-1]

            score = sharpe + momentum

            scores[market] = score

        return scores

    def softmax(self, scores):
        values = np.array(list(scores.values()))
        exp = np.exp(values - np.max(values))
        probs = exp / exp.sum()

        return dict(zip(scores.keys(), probs))

    def allocate(self, data_dict, capital):

        scores = self.compute_scores(data_dict)

        weights = self.softmax(scores)

        allocation = {}

        for market, w in weights.items():
            allocation[market] = capital * w

        self.weights = weights

        return allocation

    def rebalance(self, data_dict, capital):
        return self.allocate(data_dict, capital)
