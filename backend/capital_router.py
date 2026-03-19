# Intelligent Capital Router
# Distribui capital dinamicamente entre estratégias

import numpy as np

class CapitalRouter:

    def __init__(self):
        self.min_weight = 0.05

    def normalize(self, scores):
        values = np.array(list(scores.values()))

        # evita negativos extremos
        values = np.maximum(values, 0)

        if values.sum() == 0:
            values = np.ones_like(values)

        weights = values / values.sum()

        return dict(zip(scores.keys(), weights))

    def apply_floor(self, weights):
        adjusted = {}

        for k, v in weights.items():
            adjusted[k] = max(v, self.min_weight)

        # renormaliza
        total = sum(adjusted.values())
        for k in adjusted:
            adjusted[k] /= total

        return adjusted

    def allocate(self, capital, strategy_scores):

        # 1. normaliza scores → pesos
        weights = self.normalize(strategy_scores)

        # 2. aplica mínimo por estratégia
        weights = self.apply_floor(weights)

        # 3. distribui capital
        allocation = {}

        for strategy, w in weights.items():
            allocation[strategy] = capital * w

        return {
            "capital_total": capital,
            "weights": weights,
            "allocation": allocation
        }

    def dynamic_update(self, capital, performance):
        """
        performance: {strategy: retorno recente}
        """

        # transforma performance em score
        scores = {
            k: max(v, 0) for k, v in performance.items()
        }

        return self.allocate(capital, scores)
