# Liquidity-Aware Execution + Market Impact Prediction
import numpy as np
import time

class OrderBookAnalyzer:

    def __init__(self):
        pass

    def estimate_liquidity(self, bids, asks):
        bid_liq = sum([b[1] for b in bids[:10]])
        ask_liq = sum([a[1] for a in asks[:10]])
        return bid_liq, ask_liq

    def estimate_slippage(self, side, quantity, bids, asks):
        book = asks if side == "BUY" else bids

        filled = 0
        cost = 0

        for price, size in book:
            take = min(size, quantity - filled)
            cost += take * price
            filled += take

            if filled >= quantity:
                break

        if filled == 0:
            return None

        avg_price = cost / filled
        return avg_price


class MarketImpactModel:

    def predict_impact(self, quantity, liquidity):
        if liquidity == 0:
            return 0.01

        impact = quantity / liquidity
        return min(impact, 0.02)


class LiquidityExecutionEngine:

    def __init__(self, client):
        self.client = client
        self.analyzer = OrderBookAnalyzer()
        self.impact_model = MarketImpactModel()

    def execute(self, symbol, side, quantity, orderbook):

        bids = orderbook["bids"]
        asks = orderbook["asks"]

        bid_liq, ask_liq = self.analyzer.estimate_liquidity(bids, asks)

        liquidity = ask_liq if side == "BUY" else bid_liq

        impact = self.impact_model.predict_impact(quantity, liquidity)

        # fragmentação baseada na liquidez
        slices = max(2, int(quantity / (liquidity * 0.1 + 1e-6)))
        slice_qty = quantity / slices

        executions = []

        for i in range(slices):

            price = self.analyzer.estimate_slippage(side, slice_qty, bids, asks)

            result = self.client.place_order(symbol, side, slice_qty)

            executions.append({
                "slice": i,
                "qty": slice_qty,
                "price_est": price,
                "impact": impact,
                "result": result
            })

            time.sleep(0.5)

        return {
            "impact_estimate": impact,
            "executions": executions
        }
