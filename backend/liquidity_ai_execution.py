# Liquidity Forecasting + Adaptive Execution AI
import numpy as np
import time

class LiquidityForecaster:
    """Prevê liquidez futura simples (rolling + tendência)"""

    def predict(self, past_liquidity):
        if len(past_liquidity) < 5:
            return np.mean(past_liquidity) if past_liquidity else 0

        trend = np.mean(np.diff(past_liquidity[-5:]))
        forecast = past_liquidity[-1] + trend
        return max(forecast, 1e-6)


class ImpactModelAI:
    """Modelo simples de impacto (pode evoluir para ML/RL)"""

    def estimate(self, qty, forecast_liquidity):
        impact = qty / forecast_liquidity
        return min(impact, 0.03)


class AdaptiveExecutionAI:

    def __init__(self, client):
        self.client = client
        self.forecaster = LiquidityForecaster()
        self.impact_model = ImpactModelAI()

    def decide_slices(self, qty, forecast_liq, impact):
        base = int(qty / (forecast_liq * 0.1 + 1e-6))
        if impact > 0.02:
            base *= 2
        return max(2, min(base, 20))

    def execute(self, symbol, side, qty, orderbook, liquidity_history):

        bids = orderbook['bids']
        asks = orderbook['asks']

        current_liq = sum([a[1] for a in asks[:10]]) if side == 'BUY' else sum([b[1] for b in bids[:10]])

        forecast_liq = self.forecaster.predict(liquidity_history + [current_liq])

        impact = self.impact_model.estimate(qty, forecast_liq)

        slices = self.decide_slices(qty, forecast_liq, impact)
        slice_qty = qty / slices

        executions = []

        for i in range(slices):

            # ajuste dinâmico (simples)
            adj = 1 + (impact * (i / slices))

            result = self.client.place_order(symbol, side, slice_qty * adj)

            executions.append({
                'slice': i,
                'qty': slice_qty,
                'adj_factor': adj,
                'impact_est': impact,
                'forecast_liq': forecast_liq,
                'result': result
            })

            time.sleep(0.3)

        return {
            'forecast_liquidity': forecast_liq,
            'impact_estimate': impact,
            'slices': slices,
            'executions': executions
        }
