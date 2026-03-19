# Regime Switching + Multi-Asset Hedge Engine
import numpy as np

class RegimeEngine:

    def detect_regime(self, returns, volatility):

        trend = np.mean(returns[-20:])

        if volatility > 0.05:
            return "CRISIS"

        if trend > 0.001:
            return "BULL"

        if trend < -0.001:
            return "BEAR"

        return "SIDEWAYS"


class HedgeEngine:

    def hedge_allocation(self, regime):

        if regime == "BULL":
            return {
                "risk_assets": 0.7,
                "hedge_assets": 0.2,
                "cash": 0.1
            }

        if regime == "BEAR":
            return {
                "risk_assets": 0.2,
                "hedge_assets": 0.6,
                "cash": 0.2
            }

        if regime == "CRISIS":
            return {
                "risk_assets": 0.1,
                "hedge_assets": 0.5,
                "cash": 0.4
            }

        # sideways
        return {
            "risk_assets": 0.4,
            "hedge_assets": 0.3,
            "cash": 0.3
        }


class RegimeHedgeSystem:

    def __init__(self):
        self.regime_engine = RegimeEngine()
        self.hedge_engine = HedgeEngine()

    def run(self, returns, volatility, capital):

        regime = self.regime_engine.detect_regime(returns, volatility)

        allocation = self.hedge_engine.hedge_allocation(regime)

        capital_dist = {
            k: capital * v for k, v in allocation.items()
        }

        return {
            "regime": regime,
            "allocation_pct": allocation,
            "allocation_value": capital_dist
        }
