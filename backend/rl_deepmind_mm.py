# RL contínuo estilo DeepMind (simplificado e plug-and-play)
# - Replay Buffer
# - Treino online
# - Política epsilon-greedy

import numpy as np
from collections import deque
import random

class ReplayBuffer:
    def __init__(self, maxlen=10000):
        self.buffer = deque(maxlen=maxlen)

    def add(self, s, a, r, s2):
        self.buffer.append((s, a, r, s2))

    def sample(self, batch_size=64):
        batch = random.sample(self.buffer, min(len(self.buffer), batch_size))
        s, a, r, s2 = zip(*batch)
        return np.array(s), np.array(a), np.array(r), np.array(s2)

class DeepRLMarketMaker:
    def __init__(self, state_dim=2, n_actions=4):
        self.actions = ["BUY","SELL","BOTH","NONE"]
        self.n_actions = n_actions

        # "rede" linear simples (substitui NN pesada)
        self.W = np.random.randn(state_dim, n_actions) * 0.01

        self.lr = 0.01
        self.gamma = 0.95
        self.epsilon = 0.1

        self.buffer = ReplayBuffer()

        self.inventory = 0
        self.spread = 0.002

    # ===== FEATURES =====
    def state(self, imbalance):
        inv = self.inventory / 100.0
        return np.array([imbalance, inv])

    # ===== POLICY =====
    def q_values(self, s):
        return s @ self.W

    def act(self, s):
        if np.random.rand() < self.epsilon:
            return random.randrange(self.n_actions)
        return int(np.argmax(self.q_values(s)))

    # ===== LEARNING =====
    def train_step(self, batch_size=64):
        if len(self.buffer.buffer) < 10:
            return

        S, A, R, S2 = self.buffer.sample(batch_size)

        Q = S @ self.W
        Q_next = S2 @ self.W

        target = Q.copy()

        for i in range(len(S)):
            target[i, A[i]] = R[i] + self.gamma * np.max(Q_next[i])

        # gradient descent simples
        grad = S.T @ (target - Q) / len(S)
        self.W += self.lr * grad

    # ===== SPREAD =====
    def adapt_spread(self, imbalance):
        if abs(imbalance) > 0.3:
            self.spread = 0.004
        elif abs(imbalance) > 0.1:
            self.spread = 0.003
        else:
            self.spread = 0.002

    # ===== EXEC =====
    def step(self, bids, asks, pnl_change):

        bid_p, ask_p = bids[0][0], asks[0][0]
        mid = (bid_p + ask_p) / 2

        bid_vol = sum([b[1] for b in bids[:5]])
        ask_vol = sum([a[1] for a in asks[:5]])

        imbalance = 0 if (bid_vol+ask_vol)==0 else (bid_vol-ask_vol)/(bid_vol+ask_vol)

        self.adapt_spread(imbalance)

        s = self.state(imbalance)
        a = self.act(s)

        bid = mid * (1 - self.spread)
        ask = mid * (1 + self.spread)

        orders = []

        if self.actions[a] in ["BUY","BOTH"]:
            orders.append(("BUY", bid))
        if self.actions[a] in ["SELL","BOTH"]:
            orders.append(("SELL", ask))

        # reward
        reward = pnl_change - 0.001 * abs(self.inventory)

        s2 = self.state(imbalance)

        self.buffer.add(s, a, reward, s2)

        self.train_step()

        return orders
