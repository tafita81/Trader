# Decision Engine Unificado com Score de Probabilidade
import numpy as np

class DecisionEngine:

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

    def normalize(self, value, min_v=-1, max_v=1):
        return (value - min_v) / (max_v - min_v)

    def compute_score(self, signals):
        score = 0

        for k, w in self.weights.items():
            v = signals.get(k, 0)
            v_norm = self.normalize(v)
            score += v_norm * w

        return score

    def probability(self, score):
        return 1 / (1 + np.exp(-5 * (score - 0.5)))

    def decision(self, signals):

        score = self.compute_score(signals)
        prob = self.probability(score)

        if prob > 0.7:
            action = "STRONG_BUY"
        elif prob > 0.6:
            action = "BUY"
        elif prob < 0.3:
            action = "STRONG_SELL"
        elif prob < 0.4:
            action = "SELL"
        else:
            action = "SKIP"

        return {
            "score": round(score, 4),
            "probability": round(prob, 4),
            "action": action
        }
