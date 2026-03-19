import websocket
import json

class BinanceWS:
    def __init__(self, symbol="btcusdt"):
        self.url = f"wss://stream.binance.com:9443/ws/{symbol}@depth"
        self.data = {}

    def on_message(self, ws, message):
        self.data = json.loads(message)

    def start(self):
        ws = websocket.WebSocketApp(self.url, on_message=self.on_message)
        ws.run_forever()
