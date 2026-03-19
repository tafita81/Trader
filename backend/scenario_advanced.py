# Cenário Multi-Step + Stress Test Engine
# - Simulação de múltiplos passos
# - Cenários extremos (crash / pump)
# - Decisão baseada em distribuição (não só média)

import numpy as np

class AdvancedScenarioEngine:

    def __init__(self, n_scenarios=200, steps=10):
        self.n_scenarios = n_scenarios
        self.steps = steps

    def simulate_paths(self, price, mean, std):
        paths = []

        for _ in range(self.n_scenarios):
            p = price
            path = []

            for _ in range(self.steps):
                r = np.random.normal(mean, std)
                p = p * (1 + r)
                path.append(p)

            paths.append(path)

        return np.array(paths)

    def stress_scenarios(self, price):
        crash = price * 0.7
        pump = price * 1.3
        return [crash, pump]

    def evaluate(self, paths):

        final_prices = paths[:, -1]

        buy = final_prices - np.mean(final_prices)
        sell = np.mean(final_prices) - final_prices
        hold = np.zeros_like(final_prices)

        return {
            "BUY": buy,
            "SELL": sell,
            "HOLD": hold
        }

    def risk_metrics(self, values):
        return {
            "mean": np.mean(values),
            "worst": np.min(values),
            "var_95": np.percentile(values, 5)
        }

    def choose_action(self, results):

        scores = {}

        for action, values in results.items():
            metrics = self.risk_metrics(values)

            # penaliza risco
            score = metrics["mean"] + 0.5 * metrics["var_95"]

            scores[action] = score

        return max(scores, key=scores.get), scores

    def run(self, df):

        returns = df['ret'].dropna()

        mean = returns.mean()
        std = returns.std()

        price = df['Close'].iloc[-1]

        paths = self.simulate_paths(price, mean, std)

        results = self.evaluate(paths)

        best, scores = self.choose_action(results)

        stress = self.stress_scenarios(price)

        return {
            "best_action": best,
            "scores": scores,
            "stress_test": {
                "crash_price": stress[0],
                "pump_price": stress[1]
            }
        }
