# Global Arbitrage Engine (multi-mercado automático)
import numpy as np

class ArbitrageEngine:

    def __init__(self, threshold=0.002):
        self.threshold = threshold  # diferença mínima (0.2%)

    def find_opportunities(self, prices_dict):
        # prices_dict = {"binance": 100, "coinbase": 100.5}
        opps = []

        exchanges = list(prices_dict.keys())

        for i in range(len(exchanges)):
            for j in range(i+1, len(exchanges)):

                ex1, ex2 = exchanges[i], exchanges[j]
                p1, p2 = prices_dict[ex1], prices_dict[ex2]

                diff = (p2 - p1) / p1

                if abs(diff) > self.threshold:
                    if diff > 0:
                        opps.append({
                            "buy": ex1,
                            "sell": ex2,
                            "spread": diff
                        })
                    else:
                        opps.append({
                            "buy": ex2,
                            "sell": ex1,
                            "spread": -diff
                        })

        return sorted(opps, key=lambda x: x["spread"], reverse=True)

    def execute(self, opportunity, capital):
        size = capital * 0.1

        return {
            "action": "ARBITRAGE",
            "buy_exchange": opportunity["buy"],
            "sell_exchange": opportunity["sell"],
            "size": size,
            "expected_profit": size * opportunity["spread"]
        }

    def run(self, prices_dict, capital):

        opps = self.find_opportunities(prices_dict)

        if not opps:
            return {"action": "NONE"}

        best = opps[0]

        return self.execute(best, capital)
