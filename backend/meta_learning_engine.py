# Meta-Learning + Model Competition Engine
import numpy as np
import random

class Model:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.weight = 1.0

    def update(self, reward):
        self.score += reward

class MetaLearningEngine:

    def __init__(self):
        self.models = [
            Model("sniper"),
            Model("orderflow"),
            Model("rl"),
            Model("genetic"),
            Model("scenario")
        ]

        self.temperature = 0.5  # exploração vs exploração

    def softmax(self, scores):
        exp = np.exp(scores - np.max(scores))
        return exp / exp.sum()

    def select_model(self):
        scores = np.array([m.score for m in self.models])
        probs = self.softmax(scores / self.temperature)
        idx = np.random.choice(len(self.models), p=probs)
        return self.models[idx]

    def update_models(self, rewards_dict):
        for m in self.models:
            reward = rewards_dict.get(m.name, 0)
            m.update(reward)

    def get_weights(self):
        scores = np.array([m.score for m in self.models])
        probs = self.softmax(scores)

        return {
            m.name: float(p)
            for m, p in zip(self.models, probs)
        }

    def step(self, rewards_dict):
        self.update_models(rewards_dict)
        return self.get_weights()
