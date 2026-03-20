import requests
import time
from news_intelligence import NewsIntelligence
from supply_chain_engine import SupplyChainEngine
from scarcity_engine import ScarcityEngine
from opportunity_engine import OpportunityEngine

class NewsLiveTrading:

    def __init__(self):
        self.news = NewsIntelligence()
        self.supply = SupplyChainEngine()
        self.scarcity = ScarcityEngine()
        self.opportunity = OpportunityEngine()

    def fetch_news(self):
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "iran OR oil OR sanctions OR chips OR lithium",
            "language": "en",
            "apiKey": "YOUR_NEWS_API_KEY"
        }

        res = requests.get(url, params=params).json()
        articles = res.get("articles", [])
        return [a.get("title", "") for a in articles]

    def process_news(self, text):
        parsed = self.news.parse(text)
        scarcity = self.scarcity.predict(parsed, self.supply)
        trades = self.opportunity.detect(scarcity)

        return {
            "news": text,
            "parsed": parsed,
            "scarcity": scarcity,
            "trades": trades
        }

    def run(self):

        while True:
            try:
                news_list = self.fetch_news()

                for text in news_list[:5]:
                    result = self.process_news(text)
                    print(result)

                time.sleep(30)

            except Exception as e:
                print("ERROR:", e)
                time.sleep(10)


if __name__ == "__main__":
    bot = NewsLiveTrading()
    bot.run()
