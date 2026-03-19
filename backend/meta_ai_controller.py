# Meta-AI Controller: orquestra todo o sistema em tempo real
# Integra: decision, risk, crisis, capital router, execution

import time

class MetaAIController:

    def __init__(self, decision_engine, risk_engine, crisis_engine, capital_router, exec_engine):
        self.decision_engine = decision_engine
        self.risk_engine = risk_engine
        self.crisis_engine = crisis_engine
        self.capital_router = capital_router
        self.exec_engine = exec_engine

        self.state = {
            "mode": "NORMAL",  # NORMAL | DEFENSIVE | AGGRESSIVE
            "confidence": 0.5
        }

    # ===== avaliação global =====
    def evaluate_system(self, metrics):
        score = 0

        if metrics.get("sharpe", 0) > 1:
            score += 1
        if metrics.get("drawdown", 0) > -0.05:
            score += 1
        if metrics.get("winrate", 0) > 0.55:
            score += 1

        self.state["confidence"] = score / 3

        if score >= 2:
            self.state["mode"] = "AGGRESSIVE"
        elif score == 1:
            self.state["mode"] = "NORMAL"
        else:
            self.state["mode"] = "DEFENSIVE"

        return self.state

    # ===== ajuste dinâmico =====
    def adjust_parameters(self):
        if self.state["mode"] == "AGGRESSIVE":
            return {"risk": 0.03, "capital_multiplier": 1.2}

        if self.state["mode"] == "DEFENSIVE":
            return {"risk": 0.01, "capital_multiplier": 0.7}

        return {"risk": 0.02, "capital_multiplier": 1.0}

    # ===== decisão central =====
    def run_cycle(self, market_data, portfolio):

        # 1. avaliar sistema
        state = self.evaluate_system(portfolio["metrics"])

        # 2. ajustar parâmetros
        params = self.adjust_parameters()

        # 3. decisão
        decision = self.decision_engine.decision(market_data["signals"])

        # 4. alocação
        allocation = self.capital_router.allocate(
            portfolio["capital"] * params["capital_multiplier"],
            market_data["strategy_scores"]
        )

        # 5. crise
        crisis = self.crisis_engine.run(
            volatility=market_data["vol"],
            drawdown=portfolio["metrics"]["drawdown"],
            sharpe=portfolio["metrics"]["sharpe"],
            base_risk=params["risk"],
            allocation=allocation["allocation"]
        )

        # 6. execução
        execution = None
        if decision["action"] in ["BUY", "STRONG_BUY", "SELL", "STRONG_SELL"]:
            execution = self.exec_engine.execute(
                symbol=market_data["symbol"],
                side="BUY" if "BUY" in decision["action"] else "SELL",
                qty=portfolio["capital"] * params["risk"],
                orderbook=market_data.get("orderbook", {}),
                liquidity_history=market_data.get("liq_history", [])
            )

        # 7. risco
        metrics = self.risk_engine.update(portfolio["capital"], portfolio.get("pnl", 0))
        status = self.risk_engine.check_kill_switch(metrics)

        return {
            "state": state,
            "params": params,
            "decision": decision,
            "allocation": allocation,
            "crisis": crisis,
            "execution": execution,
            "risk_status": status
        }


# ===== LOOP EXEMPLO =====
# controller = MetaAIController(...)
# while True:
#     result = controller.run_cycle(market_data, portfolio)
#     print(result)
#     time.sleep(5)
