# Risk Engine Institucional + Kill Switch
import time

class RiskEngine:

    def __init__(self):
        self.max_drawdown = -0.10
        self.max_daily_loss = -0.05
        self.max_consecutive_losses = 5

        self.peak_capital = None
        self.daily_start = None
        self.loss_streak = 0

    def update(self, capital, pnl):

        # inicialização
        if self.peak_capital is None:
            self.peak_capital = capital

        if self.daily_start is None:
            self.daily_start = capital

        # atualiza pico
        if capital > self.peak_capital:
            self.peak_capital = capital

        # calcula drawdown
        drawdown = (capital - self.peak_capital) / self.peak_capital

        # perda diária
        daily_loss = (capital - self.daily_start) / self.daily_start

        # streak de perdas
        if pnl < 0:
            self.loss_streak += 1
        else:
            self.loss_streak = 0

        return {
            "drawdown": drawdown,
            "daily_loss": daily_loss,
            "loss_streak": self.loss_streak
        }

    def check_kill_switch(self, metrics):

        if metrics["drawdown"] < self.max_drawdown:
            return "STOP_ALL"

        if metrics["daily_loss"] < self.max_daily_loss:
            return "STOP_DAY"

        if metrics["loss_streak"] >= self.max_consecutive_losses:
            return "PAUSE"

        return "OK"

    def reset_daily(self, capital):
        self.daily_start = capital
        self.loss_streak = 0


# ===== USO =====
# risk = RiskEngine()
# metrics = risk.update(capital, pnl)
# status = risk.check_kill_switch(metrics)
