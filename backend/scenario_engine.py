# Simulação de Cenários Futuros + Decisão Ótima
# - Monte Carlo
# - Cenários múltiplos
# - Escolha da melhor ação esperada

import numpy as np

class ScenarioEngine:

    def __init__(self, n_scenarios=100):
        self.n_scenarios = n_scenarios

    def simulate_returns(self, mean, std):
        return np.random.normal(mean, std, self.n_scenarios)

    def simulate_price_paths(self, last_price, returns):
        paths = []
        for r in returns:
            future_price = last_price * (1 + r)
            paths.append(future_price)
        return np.array(paths)

    def evaluate_actions(self, price_paths):

        results = {
            "BUY": [],
            "SELL": [],
            "HOLD": []
        }

        for price in price_paths:

            results["BUY"].append(price - price_paths.mean())
            results["SELL"].append(price_paths.mean() - price)
            results["HOLD"].append(0)

        expected = {
            k: np.mean(v) for k, v in results.items()
        }

        return expected

    def choose_best_action(self, expected_values):
        return max(expected_values, key=expected_values.get)

    def run(self, df):

        returns = df['ret'].dropna()

        mean = returns.mean()
        std = returns.std()

        last_price = df['Close'].iloc[-1]

        sim_returns = self.simulate_returns(mean, std)

        price_paths = self.simulate_price_paths(last_price, sim_returns)

        expected = self.evaluate_actions(price_paths)

        action = self.choose_best_action(expected)

        return {
            "expected": expected,
            "best_action": action
        }
