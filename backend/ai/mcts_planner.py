import random

class MCTSPlanner:

    def __init__(self, simulations=50):
        self.simulations = simulations

    def simulate(self, agent, market):
        score = 0
        for _ in range(self.simulations):
            score += random.uniform(-1, 1)
        return score / self.simulations

    def plan(self, agents, market):
        results = []
        for a in agents:
            value = self.simulate(a, market)
            results.append({"agent": a.name, "value": value})
        return sorted(results, key=lambda x: x['value'], reverse=True)
