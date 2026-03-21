import random

class EvolutionEngine:

    def __init__(self):
        self.generation = 0

    def mutate(self, agent):
        agent.mutation_rate = random.uniform(0.9, 1.1)
        return agent

    def crossover(self, a1, a2):
        child = a1
        child.name = a1.name + "_child"
        return child

    def evolve(self, agents):

        # ordenar por performance
        ranked = sorted(agents, key=lambda x: x.score(), reverse=True)

        survivors = ranked[:3]

        new_agents = []

        for i in range(len(survivors)-1):
            child = self.crossover(survivors[i], survivors[i+1])
            child = self.mutate(child)
            new_agents.append(child)

        self.generation += 1

        return survivors + new_agents
