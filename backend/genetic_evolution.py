# Evolução Genética de Estratégias (nível hedge fund)
# - População de estratégias
# - Seleção natural
# - Mutação
# - Crossover

import numpy as np
import random

class GeneticStrategy:

    def __init__(self, n_features=4):
        self.weights = np.random.uniform(-1, 1, n_features)
        self.fitness = 0

    def evaluate(self, features):
        return np.dot(self.weights, features)

    def mutate(self, rate=0.1):
        for i in range(len(self.weights)):
            if random.random() < rate:
                self.weights[i] += np.random.normal(0, 0.1)

    def crossover(self, other):
        child = GeneticStrategy(len(self.weights))
        for i in range(len(self.weights)):
            child.weights[i] = random.choice([self.weights[i], other.weights[i]])
        return child


class GeneticEngine:

    def __init__(self, population_size=20):
        self.population = [GeneticStrategy() for _ in range(population_size)]

    def evaluate_population(self, features, rewards):
        for i, strat in enumerate(self.population):
            strat.fitness = rewards[i] if i < len(rewards) else 0

    def select_top(self, k=5):
        return sorted(self.population, key=lambda x: x.fitness, reverse=True)[:k]

    def evolve(self):

        top = self.select_top()

        new_population = top.copy()

        while len(new_population) < len(self.population):

            parent1, parent2 = random.sample(top, 2)

            child = parent1.crossover(parent2)
            child.mutate()

            new_population.append(child)

        self.population = new_population

    def get_best(self):
        return max(self.population, key=lambda x: x.fitness)
