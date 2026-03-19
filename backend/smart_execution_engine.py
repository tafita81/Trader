# Smart Order Routing + Fragmented Execution
import time
import random

class SmartOrderRouter:

    def __init__(self, exchanges):
        self.exchanges = exchanges  # {name: client}

    def get_best_price(self, symbol):
        prices = {}

        for name, client in self.exchanges.items():
            try:
                price = client.get_price(symbol)
                prices[name] = price
            except:
                continue

        if not prices:
            return None, None

        best_exchange = min(prices, key=prices.get)
        return best_exchange, prices[best_exchange]


class FragmentedExecutor:

    def __init__(self, router, max_slices=5):
        self.router = router
        self.max_slices = max_slices

    def execute(self, symbol, side, total_quantity):

        slices = random.randint(2, self.max_slices)
        qty_per_slice = total_quantity / slices

        executions = []

        for i in range(slices):

            exchange, price = self.router.get_best_price(symbol)

            if not exchange:
                continue

            result = exchange.execute_order(symbol, side, qty_per_slice)

            executions.append({
                "exchange": exchange,
                "qty": qty_per_slice,
                "result": result
            })

            time.sleep(random.uniform(0.5, 2))

        return executions


# ===== MOCK CLIENT EXAMPLE =====
class ExchangeClient:

    def __init__(self, name):
        self.name = name

    def get_price(self, symbol):
        return random.uniform(100, 101)

    def execute_order(self, symbol, side, qty):
        return {"status": "FILLED", "qty": qty}
