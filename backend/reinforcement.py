import numpy as np

class ReinforcementLearner:
    def __init__(self):
        self.weights = {
            "rsi": 0.3,
            "vol_spike": 0.3,
            "zscore": 0.4
        }
        self.learning_rate = 0.01

    def predict_score(self, row):
        return (
            row["rsi"] * self.weights["rsi"] +
            row["vol_spike"] * self.weights["vol_spike"] +
            row["zscore"] * self.weights["zscore"]
        )

    def update_weights(self, row, reward):
        # ajuste simples baseado no resultado do trade
        self.weights["rsi"] += self.learning_rate * reward * row["rsi"]
        self.weights["vol_spike"] += self.learning_rate * reward * row["vol_spike"]
        self.weights["zscore"] += self.learning_rate * reward * row["zscore"]

        # normalização
        total = sum(abs(v) for v in self.weights.values())
        self.weights = {k: v/total for k,v in self.weights.items()}

    def train_on_history(self, df):
        for i in range(len(df)-1):
            row = df.iloc[i]
            next_ret = df.iloc[i+1]["ret"]

            reward = next_ret
            self.update_weights(row, reward)

        return self.weights