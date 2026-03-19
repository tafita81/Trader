# IA de Regime de Mercado + Geração de Estratégias
import numpy as np

class MarketRegimeDetector:

    def detect(self, df):

        vol = df['ret'].rolling(20).std().iloc[-1]
        trend = df['Close'].pct_change(20).iloc[-1]

        if vol > 0.03:
            return "HIGH_VOL"

        if trend > 0.05:
            return "BULL"

        if trend < -0.05:
            return "BEAR"

        return "SIDEWAYS"


class StrategyGeneratorAI:

    def generate(self, regime):

        if regime == "BULL":
            return {
                "type": "momentum",
                "params": {"lookback": 20}
            }

        if regime == "BEAR":
            return {
                "type": "short_bias",
                "params": {"risk": 0.01}
            }

        if regime == "HIGH_VOL":
            return {
                "type": "mean_reversion",
                "params": {"zscore": 2}
            }

        return {
            "type": "market_making",
            "params": {"spread": 0.002}
        }


class RegimeStrategyEngine:

    def __init__(self):
        self.detector = MarketRegimeDetector()
        self.generator = StrategyGeneratorAI()

    def run(self, df):

        regime = self.detector.detect(df)

        strategy = self.generator.generate(regime)

        return {
            "regime": regime,
            "strategy": strategy
        }
