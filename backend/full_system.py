# Sistema completo integrado (tudo conectado)

from backend.multimarket import get_all_markets
from backend.gpu_engine import GPUStrategyEngine
from backend.strategy_engine_100 import StrategyEngine
from backend.hedge import hedge_allocation, compute_correlation
from backend.kelly import kelly_allocation
from backend.antifragile import antifragile_adjustment, detect_stress
from backend.failsafe import check_system_health
from backend.performance import compute_metrics
from backend.monthly_report import generate_monthly_report
from backend.pdf_report_blackrock import generate_blackrock_report
from config.growth_mode import adjust_risk

import pandas as pd

engine_gpu = GPUStrategyEngine(1000)
engine_100 = StrategyEngine(100)


def run_full_autonomous_fund(capital=100):

    # ===== DATA =====
    df = get_all_markets()

    # ===== FEATURES =====
    df['ret'] = df['Close'].pct_change()
    df['zscore'] = (df['Close'] - df['Close'].rolling(20).mean()) / (df['Close'].rolling(20).std() + 1e-9)
    df['vol_spike'] = df['Volume'] / (df['Volume'].rolling(20).mean() + 1e-9)

    df = detect_stress(df)

    # ===== SIGNALS =====
    row = df.iloc[-1]

    signals_gpu = engine_gpu.generate_signal(row)
    signal_gpu = engine_gpu.combine(signals_gpu)

    signals_100 = engine_100.generate_signals(df)
    signal_100 = engine_100.combine(signals_100)

    final_signal = (signal_gpu + signal_100) / 2

    # ===== PORTFOLIO =====
    allocation = kelly_allocation(df, capital)

    corr = compute_correlation(df)
    allocation = hedge_allocation(allocation, corr)

    allocation = antifragile_adjustment(df, allocation)

    # ===== RISK =====
    risk = adjust_risk(capital)

    allocation = {k: v * risk for k, v in allocation.items()}

    # ===== LEARNING =====
    reward = df['ret'].iloc[-1]

    engine_gpu.update(signals_gpu, reward)
    engine_gpu.prune()
    engine_gpu.expand()

    engine_100.update(signals_100, reward)
    engine_100.prune_and_expand()

    # ===== PERFORMANCE =====
    metrics = compute_metrics(df)

    # ===== FAILSAFE =====
    if check_system_health(df.get('equity', pd.Series([1]))) == "STOP":
        print("Sistema parado por risco")
        return None

    # ===== REPORTS =====
    generate_monthly_report(df, capital)
    generate_blackrock_report(df, capital)

    return allocation