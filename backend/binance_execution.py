# Binance Execution Engine + Segurança + Alertas
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

    def place_order(self, symbol, side, quantity):
        endpoint = "/api/v3/order"

        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }

        query = self._sign(params)

        headers = {"X-MBX-APIKEY": self.api_key}

        url = self.base_url + endpoint + "?" + query

        r = requests.post(url, headers=headers)

        return r.json()


# ===== EXECUÇÃO SEGURA =====
class SafeExecutor:

    def __init__(self, client):
        self.client = client
        self.max_retries = 3

    def execute(self, symbol, side, quantity):

        for i in range(self.max_retries):
            try:
                result = self.client.place_order(symbol, side, quantity)

                if "orderId" in result:
                    return result

            except Exception as e:
                time.sleep(1)

        return {"error": "failed_execution"}


# ===== ALERTAS TELEGRAM =====
def send_telegram(token, chat_id, msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg})


# ===== EXEMPLO USO =====
# client = BinanceClient(API_KEY, SECRET)
# executor = SafeExecutor(client)
# executor.execute("BTCUSDT", "BUY", 0.001)
