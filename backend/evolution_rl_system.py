import random
import copy

# ==============================
# AGENTE BASE
# ==============================
class Agent:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.param = random.random()

    def act(self, state):
        if self.param > 0.5:
            return "BUY"
        return "SELL"

    def update(self, reward):
        self.score += reward


# ==============================
# ARENA (COMPETIÇÃO)
# ==============================
class Arena:

    def run(self, agents, market):

        for agent in agents:

            action = agent.act(market)

            reward = market.get("pnl", 0)

            if action == "SELL":
                reward *= -1

            agent.update(reward)


# ==============================
# SELEÇÃO
# ==============================
class Selection:

    def select(self, agents):

        agents = sorted(agents, key=lambda a: a.score, reverse=True)

        return agents[:len(agents)//2]


# ==============================
# EVOLUÇÃO (MUTAÇÃO)
# ==============================
class Evolution:

    def reproduce(self, agents):

        new_agents = []

        for agent in agents:

            clone = copy.deepcopy(agent)

            clone.param += random.uniform(-0.1, 0.1)

            clone.name = agent.name + "_child"

            new_agents.append(clone)

        return agents + new_agents


# ==============================
# SISTEMA COMPLETO
# ==============================
class EvolutionRLSystem:

    def __init__(self, population_size=10):

        self.agents = [Agent(f"A{i}") for i in range(population_size)]

        self.arena = Arena()
        self.selector = Selection()
        self.evolution = Evolution()

    def step(self, market):

        # competição
        self.arena.run(self.agents, market)

        # seleção
        survivors = self.selector.select(self.agents)

        # evolução
        self.agents = self.evolution.reproduce(survivors)

        best = max(self.agents, key=lambda a: a.score)

        return {
            "population": len(self.agents),
            "best_agent": best.name,
            "best_score": best.score
        }
