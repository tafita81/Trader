import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(layout="wide")

st.title("📊 Quantum Fund PRO Dashboard")

# ===== SIMULAÇÃO REALTIME =====
def get_data():
    return {
        "capital": np.random.randint(900, 1500),
        "sharpe": round(np.random.uniform(0.5, 2.0), 2),
        "drawdown": round(np.random.uniform(-0.12, -0.01), 3),
        "pnl": np.random.randint(-50, 300)
    }

# ===== LOOP REALTIME =====
placeholder = st.empty()

while True:

    data = get_data()

    with placeholder.container():

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("💰 Capital", f"${data['capital']}")
        col2.metric("📈 Sharpe", data['sharpe'])
        col3.metric("⚠️ Drawdown", f"{data['drawdown']*100:.2f}%")
        col4.metric("📊 PnL", f"${data['pnl']}")

        # ===== ALERTAS VISUAIS =====
        if data["drawdown"] < -0.1:
            st.error("🚨 RISCO CRÍTICO - DRAWDOWN ALTO")
        elif data["sharpe"] < 0.5:
            st.warning("⚠️ PERFORMANCE BAIXA")
        else:
            st.success("✅ SISTEMA SAUDÁVEL")

        # ===== EQUITY =====
        st.subheader("📈 Equity vs Benchmark")

        equity = np.cumsum(np.random.randn(100)) + 100
        benchmark = np.cumsum(np.random.randn(100)) + 100

        df = pd.DataFrame({
            "Fund": equity,
            "Benchmark": benchmark
        })

        st.line_chart(df)

        # ===== HEATMAP =====
        st.subheader("🌍 Alocação Global")

        alloc = pd.DataFrame({
            "Asset": ["BTC","ALB","SQM","LIT"],
            "Weight": np.random.rand(4)
        })

        st.bar_chart(alloc.set_index("Asset"))

        # ===== LOG =====
        st.subheader("🧠 Decisões")
        st.text("BUY BTC | SELL SQM | HOLD LIT")

    time.sleep(2)
