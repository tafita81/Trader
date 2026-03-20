import random

class Agent:
    def __init__(self, name):
        self.name = name
        self.memory = []

    def act(self, state):
        return random.choice(["BUY","SELL","HOLD"])

    def learn(self, reward):
        self.memory.append(reward)

class FlowAgent(Agent):
    def act(self, state):
        if state.get("flow") == "BUY_PRESSURE":
            return "BUY"
        if state.get("flow") == "SELL_PRESSURE":
            return "SELL"
        return "HOLD"

class BookAgent(Agent):
    def act(self, state):
        if state.get("book") == "STRONG_SUPPORT":
            return "BUY"
        if state.get("book") == "STRONG_RESISTANCE":
            return "SELL"
        return "HOLD"

class MetaAgent:
    def __init__(self):
        self.agents = [FlowAgent("flow"), BookAgent("book")]

    def decide(self, state):
        votes = {"BUY":0, "SELL":0, "HOLD":0}
        for agent in self.agents:
            votes[agent.act(state)] += 1
        return max(votes, key=votes.get)

    def learn(self, reward):
        for agent in self.agents:
            agent.learn(reward)

class System:
    def __init__(self):
        self.meta = MetaAgent()

    def run(self, market):
        state = {
            "flow": market.get("flow"),
            "book": market.get("book")
        }
        action = self.meta.decide(state)
        reward = market.get("pnl", 0)
        self.meta.learn(reward)
        return {"action": action, "reward": reward}
