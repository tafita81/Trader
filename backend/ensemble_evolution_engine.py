# Ensemble Evolutivo + Feature Engineering Automático
import random
import numpy as np

class FeatureGenerator:

    def generate(self, prices):
        features = {}

        if len(prices) < 5:
            return features

        returns = np.diff(prices)

        features["momentum"] = prices[-1] - prices[-3]
        features["volatility"] = np.std(returns)
        features["trend"] = np.mean(returns)
        features["acceleration"] = (prices[-1] - prices[-2]) - (prices[-2] - prices[-3])

        return features


class Model:

    def __init__(self, name):
        self.name = name
        self.weight = random.uniform(0.1, 1.0)
        self.score = 0

    def predict(self, features):
        return sum(features.values()) * self.weight

    def update(self, reward):
        self.score += reward


class EnsembleEvolution:

    def __init__(self, n_models=5):
        self.models = [Model(f"model_{i}") for i in range(n_models)]
        self.feature_gen = FeatureGenerator()

    def predict(self, prices):
        features = self.feature_gen.generate(prices)

        preds = []
        for m in self.models:
            preds.append(m.predict(features))

        return np.mean(preds), features

    def update(self, rewards):
        for m in self.models:
            r = rewards.get(m.name, 0)
            m.update(r)

    def evolve(self):
        # seleciona melhores
        self.models = sorted(self.models, key=lambda x: x.score, reverse=True)[:3]

        # cria novos
        while len(self.models) < 5:
            parent = random.choice(self.models)
            child = Model(parent.name + "_mut")
            child.weight = parent.weight * random.uniform(0.8, 1.2)
            self.models.append(child)

    def step(self, prices, rewards):
        pred, features = self.predict(prices)
        self.update(rewards)
        self.evolve()

        return {
            "prediction": pred,
            "features": features,
            "models": [(m.name, m.score) for m in self.models]
        }
