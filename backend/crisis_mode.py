# Crisis Mode Engine + Dynamic Risk Reduction

class CrisisEngine:

    def __init__(self):
        self.vol_threshold = 0.05
        self.drawdown_threshold = -0.08
        self.sharpe_threshold = 0.5

    def detect_crisis(self, volatility, drawdown, sharpe):

        signals = 0

        if volatility > self.vol_threshold:
            signals += 1

        if drawdown < self.drawdown_threshold:
            signals += 1

        if sharpe < self.sharpe_threshold:
            signals += 1

        if signals >= 2:
            return "CRISIS"

        if signals == 1:
            return "WARNING"

        return "NORMAL"

    def adjust_risk(self, state, base_risk):

        if state == "CRISIS":
            return base_risk * 0.3

        if state == "WARNING":
            return base_risk * 0.6

        return base_risk

    def adjust_allocation(self, allocation, state):

        if state == "CRISIS":
            # reduz exposição geral
            return {k: v * 0.5 for k, v in allocation.items()}

        if state == "WARNING":
            return {k: v * 0.8 for k, v in allocation.items()}

        return allocation

    def run(self, volatility, drawdown, sharpe, base_risk, allocation):

        state = self.detect_crisis(volatility, drawdown, sharpe)

        risk = self.adjust_risk(state, base_risk)

        allocation_adj = self.adjust_allocation(allocation, state)

        return {
            "state": state,
            "risk": risk,
            "allocation": allocation_adj
        }
