# Monitoramento 24h + Alertas (produção)
import time

class Monitor:

    def __init__(self):
        self.last_status = None

    def check_health(self, metrics):
        if metrics['drawdown'] < -0.1:
            return "CRITICAL"
        if metrics['sharpe'] < 0:
            return "WARNING"
        return "OK"

    def alert(self, status, metrics):
        print(f"ALERTA: {status} | {metrics}")

    def run(self, get_metrics_func, interval=60):

        while True:

            metrics = get_metrics_func()

            status = self.check_health(metrics)

            if status != self.last_status:
                self.alert(status, metrics)
                self.last_status = status

            time.sleep(interval)
