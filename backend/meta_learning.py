import numpy as np

class MetaLearner:
    def __init__(self):
        self.strategies = {}

    def register_strategy(self, name, performance):
        self.strategies[name] = performance

    def choose_best(self):
        if not self.strategies:
            return None
        return max(self.strategies, key=self.strategies.get)

    def update_performance(self, name, reward):
        if name not in self.strategies:
            self.strategies[name] = 0
        self.strategies[name] += reward

    def normalize(self):
        total = sum(abs(v) for v in self.strategies.values())
        if total == 0:
            return
        self.strategies = {k: v/total for k,v in self.strategies.items()}