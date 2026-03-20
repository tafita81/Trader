import hmac
import hashlib
import time
import requests

class BinanceClient:

    def __init__(self, api_key, secret_key, base_url="https://api.binance.com"):
        self.api_key = api_key
        self.secret_key = secret_key.encode()
        self.base_url = base_url

    def _sign(self, params):
        query = '&'.join([f"{k}={v}" for k,v in params.items()])
        signature = hmac.new(self.secret_key, query.encode(), hashlib.sha256).hexdigest()
        return query + "&signature=" + signature

    def _headers(self):
        return {"X-MBX-APIKEY": self.api_key}

    def order(self, symbol, side, quantity):

        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }

        query = self._sign(params)

        url = f"{self.base_url}/api/v3/order?{query}"

        return requests.post(url, headers=self._headers()).json()


class MultiAccountManager:

    def __init__(self, accounts):
        self.accounts = accounts

    def execute_all(self, symbol, signal, quantity):

        results = []

        for acc in self.accounts:

            res = acc.order(symbol, signal, quantity)
            results.append(res)

        return results


class SafeExecution:

    def __init__(self, max_allocation=0.1):
        self.max_allocation = max_allocation

    def validate(self, balance, quantity, price):

        if quantity * price > balance * self.max_allocation:
            return False

        return True
