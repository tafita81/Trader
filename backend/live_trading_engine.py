import time

class LiveTradingEngine:

    def __init__(self):
        self.balance = 100.0
        self.reserve = 0.0
        self.risk_per_trade = 0.02
        self.weekly_withdraw_rate = 0.1
        self.last_withdraw = time.time()

    def position_size(self):
        return self.balance * self.risk_per_trade

    def execute_trade(self, signal, price):

        size = self.position_size()

        pnl = 0

        if signal == "BUY":
            pnl = size * 0.002

        elif signal == "SELL":
            pnl = size * 0.002

        self.balance += pnl

        return pnl

    def protect_capital(self):

        if self.balance < 50:
            return "STOP"

        return "OK"

    def auto_withdraw(self):

        now = time.time()

        if now - self.last_withdraw > 604800:  # 7 dias

            amount = self.balance * self.weekly_withdraw_rate

            self.balance -= amount
            self.reserve += amount

            self.last_withdraw = now

            return amount

        return 0
