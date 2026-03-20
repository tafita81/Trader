from market.flow import Flow

class OrderFlowAI:
    def __init__(self):
        self.flow = Flow()

    def decide(self, trades):
        delta = self.flow.compute_delta(trades)
        if delta > 5:
            return "BUY"
        elif delta < -5:
            return "SELL"
        return "HOLD"
