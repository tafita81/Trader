# Engine de 100 estratégias simultâneas
import numpy as np
import random

FEATURES = ["rsi","zscore","vol_spike","ret"]

class StrategyEngine:
    def __init__(self, n_strategies=100):
        self.n = n_strategies
        self.strategies = [self._create_strategy() for _ in range(n_strategies)]
        self.weights = np.ones(n_strategies) / n_strategies

    def _create_strategy(self):
        weights = {f: random.uniform(-1,1) for f in FEATURES}

        def strat(row):
            return sum(row.get(f,0)*w for f,w in weights.items())

        return strat

    def generate_signals(self, df):
        last = df.iloc[-1]
        signals = np.array([s(last) for s in self.strategies])
        return signals

    def combine(self, signals):
        return float(np.dot(signals, self.weights))

    def update(self, signals, reward):
        # reinforcement simples
        self.weights += 0.01 * reward * signals
        
        # normalizar
        total = np.sum(np.abs(self.weights)) + 1e-9
        self.weights = self.weights / total

    def prune_and_expand(self):
        # remove piores e cria novas
        idx = np.argsort(self.weights)
        worst = idx[:10]
        for i in worst:
            self.strategies[i] = self._create_strategy()
            self.weights[i] = 1.0 / self.n
