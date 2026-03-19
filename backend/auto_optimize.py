# Auto-Optimization Engine (produção)
# - Monitora métricas
# - Ajusta parâmetros automaticamente
# - Dispara re-treino (RL/genetic)
# - Proteção por regime/risco

import numpy as np

class AutoOptimizer:
    def __init__(self):
        self.history = []
        self.params = {
            "risk": 0.03,
            "spread": 0.002,
            "epsilon": 0.1
        }

    def log_metrics(self, metrics: dict):
        self.history.append(metrics)
        if len(self.history) > 500:
            self.history.pop(0)

    def _rolling(self, key, n=50):
        vals = [m.get(key, 0) for m in self.history[-n:]]
        return np.mean(vals) if vals else 0.0

    def adjust_risk(self):
        sharpe = self._rolling("sharpe")
        dd = self._rolling("drawdown")

        if sharpe > 1.5 and dd > -0.05:
            self.params["risk"] = min(0.04, self.params["risk"] * 1.1)
        elif sharpe < 0.5 or dd < -0.1:
            self.params["risk"] = max(0.01, self.params["risk"] * 0.7)

    def adjust_exploration(self):
        # reduz exploração conforme melhora
        sharpe = self._rolling("sharpe")
        if sharpe > 1:
            self.params["epsilon"] = max(0.02, self.params["epsilon"] * 0.99)
        else:
            self.params["epsilon"] = min(0.2, self.params["epsilon"] * 1.01)

    def adjust_spread(self, vol):
        # adapta ao regime de volatilidade
        if vol > 0.03:
            self.params["spread"] = 0.004
        elif vol > 0.015:
            self.params["spread"] = 0.003
        else:
            self.params["spread"] = 0.002

    def should_retrain(self):
        sharpe = self._rolling("sharpe")
        return sharpe < 0.3

    def step(self, metrics, vol):
        # 1) log
        self.log_metrics(metrics)

        # 2) ajustar knobs
        self.adjust_risk()
        self.adjust_exploration()
        self.adjust_spread(vol)

        # 3) gatilho de re-treino
        retrain = self.should_retrain()

        return {
            "params": self.params.copy(),
            "retrain": retrain
        }
