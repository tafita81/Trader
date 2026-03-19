# Binance Professional Execution Engine
import requests
import time
import hmac
import hashlib

class BinanceClient:

    def __init__(self, api_key, secret):
        self.api_key = api_key
        self.secret = secret.encode()
        self.base_url = "https://api.binance.com"

    def _sign(self, params):
        query = "&".join([f"{k}={v}" for k,v in params.items()])
        signature = hmac.new(self.secret, query.encode(), hashlib.sha256).hexdigest()
        return query + "&signature=" + signature

    def place_limit_order(self, symbol, side, quantity, price):
        endpoint = "/api/v3/order"

        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": quantity,
            "price": price,
            "timestamp": int(time.time()*1000)
        }

        query = self._sign(params)
        headers = {"X-MBX-APIKEY": self.api_key}

        r = requests.post(self.base_url + endpoint + "?" + query, headers=headers)
        return r.json()

    def get_order(self, symbol, order_id):
        endpoint = "/api/v3/order"

        params = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": int(time.time()*1000)
        }

        query = self._sign(params)
        headers = {"X-MBX-APIKEY": self.api_key}

        r = requests.get(self.base_url + endpoint + "?" + query, headers=headers)
        return r.json()


class ExecutionEngine:

    def __init__(self, client):
        self.client = client
        self.max_wait = 10

    def execute_limit_safe(self, symbol, side, quantity, market_price, slippage=0.001):

        # ajusta preço com slippage
        if side == "BUY":
            price = market_price * (1 + slippage)
        else:
            price = market_price * (1 - slippage)

        order = self.client.place_limit_order(symbol, side, quantity, round(price, 2))

        if "orderId" not in order:
            return {"error": "order_failed"}

        order_id = order["orderId"]

        # tracking
        for _ in range(self.max_wait):
            status = self.client.get_order(symbol, order_id)

            if status.get("status") == "FILLED":
                return {"status": "FILLED", "order": status}

            time.sleep(1)

        return {"status": "TIMEOUT", "orderId": order_id}


# ===== ALERT =====
def send_telegram(token, chat_id, msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg})
