# Profit Optimizer (reduz perdas + aumenta Sharpe)
import numpy as np

class ProfitOptimizer:

    def __init__(self):
        self.min_confidence = 0.6
        self.max_risk = 0.03
        self.loss_cut = -0.02
        self.take_profit = 0.04

    def filter_trade(self, signal_strength, volatility):
        """
        Evita trades ruins
        """
        if signal_strength < self.min_confidence:
            return False

        if volatility > 0.05:
            return False

        return True

    def dynamic_risk(self, sharpe, drawdown):
        """
        Ajusta risco dinamicamente
        """
        if sharpe > 1.5:
            return min(self.max_risk, 0.03)

        if sharpe < 0.5 or drawdown < -0.1:
            return 0.01

        return 0.02

    def stop_loss(self, entry_price, current_price):
        change = (current_price - entry_price) / entry_price
        return change < self.loss_cut

    def take_profit_rule(self, entry_price, current_price):
        change = (current_price - entry_price) / entry_price
        return change > self.take_profit

    def position_sizing(self, capital, risk):
        return capital * risk

    def optimize(self, signal_strength, volatility, sharpe, drawdown, capital):

        # 1. filtrar trade
        if not self.filter_trade(signal_strength, volatility):
            return {"action": "SKIP"}

        # 2. ajustar risco
        risk = self.dynamic_risk(sharpe, drawdown)

        # 3. tamanho da posição
        size = self.position_sizing(capital, risk)

        return {
            "action": "EXECUTE",
            "risk": risk,
            "size": size
        }
