# Production Runner (24h automático)
import time

from backend.capital_router import CapitalRouter
from backend.risk_engine import RiskEngine
from backend.crisis_mode import CrisisEngine
from backend.decision_engine import DecisionEngine

router = CapitalRouter()
risk = RiskEngine()
crisis = CrisisEngine()
decision_engine = DecisionEngine()

capital = 100

while True:

    # ===== MOCK INPUTS (substituir por dados reais) =====
    performance = {
        "sniper": 0.05,
        "arbitrage": 0.02,
        "ensemble": 0.08
    }

    allocation_data = router.dynamic_update(capital, performance)

    allocation = allocation_data["allocation"]

    # ===== CRISIS MODE =====
    crisis_data = crisis.run(
        volatility=0.02,
        drawdown=-0.03,
        sharpe=1.2,
        base_risk=0.02,
        allocation=allocation
    )

    # ===== DECISÃO =====
    signals = {
        "sniper": 0.7,
        "orderflow": 0.6,
        "tape": 0.5,
        "delta": 0.6,
        "volume": 0.4,
        "momentum": 0.5,
        "risk": 0.2
    }

    decision = decision_engine.decision(signals)

    # ===== EXECUÇÃO MOCK =====
    pnl = 1  # simulação lucro
    capital += pnl

    # ===== RISCO =====
    metrics = risk.update(capital, pnl)
    status = risk.check_kill_switch(metrics)

    print({
        "capital": capital,
        "decision": decision,
        "risk_status": status,
        "crisis": crisis_data["state"]
    })

    if status == "STOP_ALL":
        break

    time.sleep(5)
