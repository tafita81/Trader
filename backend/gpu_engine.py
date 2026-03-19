# GPU Strategy Engine (escala massiva de estratégias)
import torch
import torch.nn as nn
import numpy as np

FEATURES = ["rsi","zscore","vol_spike","ret"]

class GPUStrategyEngine(nn.Module):
    def __init__(self, n_strategies=1000):
        super().__init__()
        self.n = n_strategies
        self.weights = nn.Parameter(torch.randn(n_strategies, len(FEATURES)))

    def forward(self, x):
        # x shape: (features)
        return torch.matmul(self.weights, x)

    def generate_signal(self, row):
        x = torch.tensor([row.get(f,0) for f in FEATURES], dtype=torch.float32)
        signals = self.forward(x)
        return signals.detach().numpy()

    def combine(self, signals):
        return float(np.mean(signals))

    def update(self, signals, reward, lr=0.001):
        grad = torch.tensor(signals, dtype=torch.float32) * reward
        self.weights.data += lr * grad.unsqueeze(1)

    def prune(self):
        norms = torch.norm(self.weights, dim=1)
        threshold = torch.quantile(norms, 0.1)
        mask = norms > threshold
        self.weights.data = self.weights.data[mask]

    def expand(self, n_new=100):
        new_weights = torch.randn(n_new, self.weights.shape[1])
        self.weights.data = torch.cat([self.weights.data, new_weights], dim=0)
