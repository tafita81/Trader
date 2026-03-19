# Auto-Tuning Engine (aprendizado contínuo dos pesos)
import numpy as np

class AutoTuningEngine:

    def __init__(self):
        self.weights = {
            "sniper": 0.2,
            "orderflow": 0.2,
            "tape": 0.15,
            "delta": 0.15,
            "volume": 0.1,
            "momentum": 0.1,
            "risk": 0.1
        }

        self.history = []
        self.lr = 0.05  # learning rate

    def log_trade(self, signals, result):
        """
        result: lucro (>0) ou prejuízo (<0)
        """
        self.history.append((signals, result))

        if len(self.history) > 500:
            self.history.pop(0)

    def update_weights(self):

        for signals, result in self.history[-50:]:

            for k in self.weights:
                v = signals.get(k, 0)

                # reforço positivo ou negativo
                if result > 0:
                    self.weights[k] += self.lr * v
                else:
                    self.weights[k] -= self.lr * v

        # normaliza pesos
        total = sum(abs(w) for w in self.weights.values())
        if total > 0:
            for k in self.weights:
                self.weights[k] /= total

    def get_weights(self):
        return self.weights

    def step(self, signals, result):
        self.log_trade(signals, result)
        self.update_weights()
        return self.weights
