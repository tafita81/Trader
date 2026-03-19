# Multi-Agent RL para Market Making (competição + seleção)
# - Vários agentes (políticas independentes)
# - Ambiente compartilhado (order book simplificado)
# - Seleção de capital por performance (bandit)

import numpy as np
import random
from collections import deque

ACTIONS = ["BUY","SELL","BOTH","NONE"]

class ReplayBuffer:
    def __init__(self, maxlen=20000):
        self.buf = deque(maxlen=maxlen)
    def add(self, s,a,r,s2):
        self.buf.append((s,a,r,s2))
    def sample(self, n=64):
        batch = random.sample(self.buf, min(len(self.buf), n))
        s,a,r,s2 = zip(*batch)
        return np.array(s), np.array(a), np.array(r), np.array(s2)

class Agent:
    def __init__(self, state_dim=2, n_actions=4):
        self.W = np.random.randn(state_dim, n_actions)*0.01
        self.lr = 0.01
        self.gamma = 0.95
        self.eps = 0.1
        self.buf = ReplayBuffer()
        self.inventory = 0
        self.spread = 0.002
        self.pnl = 0.0

    def state(self, imbalance):
        return np.array([imbalance, self.inventory/100.0])

    def q(self, s):
        return s @ self.W

    def act(self, s):
        if np.random.rand() < self.eps:
            return random.randrange(len(ACTIONS))
        return int(np.argmax(self.q(s)))

    def train(self, bs=64):
        if len(self.buf.buf) < 50: return
        S,A,R,S2 = self.buf.sample(bs)
        Q = S @ self.W
        Q2 = S2 @ self.W
        T = Q.copy()
        for i in range(len(S)):
            T[i, A[i]] = R[i] + self.gamma * np.max(Q2[i])
        grad = S.T @ (T - Q) / len(S)
        self.W += self.lr * grad

    def adapt_spread(self, imbalance):
        if abs(imbalance)>0.3: self.spread=0.004
        elif abs(imbalance)>0.1: self.spread=0.003
        else: self.spread=0.002

class MultiAgentMM:
    def __init__(self, n_agents=5):
        self.agents = [Agent() for _ in range(n_agents)]
        # pesos de alocação por agente (bandit)
        self.weights = np.ones(n_agents)/n_agents
        self.decay = 0.99

    # ===== features do book =====
    def imbalance(self, bids, asks):
        bv = sum([b[1] for b in bids[:5]])
        av = sum([a[1] for a in asks[:5]])
        return 0 if (bv+av)==0 else (bv-av)/(bv+av)

    # ===== seleção de agente (bandit suave) =====
    def sample_agent(self):
        idx = np.random.choice(len(self.agents), p=self.weights)
        return idx, self.agents[idx]

    def update_weights(self, rewards):
        # rewards por agente no step
        r = np.array(rewards)
        # normaliza e atualiza (Exp3 simplificado)
        probs = self.weights * np.exp(r - np.max(r))
        probs = probs / (probs.sum()+1e-9)
        self.weights = self.decay*self.weights + (1-self.decay)*probs
        self.weights = self.weights / self.weights.sum()

    # ===== passo do ambiente =====
    def step(self, bids, asks, pnl_changes):
        mid = (bids[0][0] + asks[0][0]) / 2
        imb = self.imbalance(bids, asks)

        orders_all = []
        rewards = []

        for i, ag in enumerate(self.agents):
            ag.adapt_spread(imb)
            s = ag.state(imb)
            a = ag.act(s)

            bid = mid*(1-ag.spread)
            ask = mid*(1+ag.spread)

            orders = []
            if ACTIONS[a] in ["BUY","BOTH"]:
                orders.append((i, "BUY", bid))
            if ACTIONS[a] in ["SELL","BOTH"]:
                orders.append((i, "SELL", ask))

            # reward: pnl_change do agente - penalidade inventário
            pnl = pnl_changes[i] if i < len(pnl_changes) else 0.0
            reward = pnl - 0.001*abs(ag.inventory)

            s2 = ag.state(imb)
            ag.buf.add(s, a, reward, s2)
            ag.train()

            rewards.append(reward)
            orders_all.extend(orders)

        # atualiza pesos (quem performa melhor recebe mais capital)
        self.update_weights(rewards)

        # filtro de risco global
        for ag in self.agents:
            if abs(ag.inventory) > 200:
                ag.inventory = np.sign(ag.inventory)*200

        return orders_all, self.weights
