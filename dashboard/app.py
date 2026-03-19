import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Quantum Fund Dashboard")

# ===== MOCK DATA (substituir por dados reais) =====
data = {
    "Capital": 1240,
    "Sharpe": 1.42,
    "Drawdown": -0.06,
    "PnL": 240
}

# ===== KPIs =====
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Capital", f"${data['Capital']}")
col2.metric("📈 Sharpe", data['Sharpe'])
col3.metric("⚠️ Drawdown", f"{data['Drawdown']*100:.2f}%")
col4.metric("📊 PnL", f"${data['PnL']}")

# ===== EQUITY CURVE =====
st.subheader("📈 Equity Curve")

df = pd.DataFrame({
    "equity": [100,120,110,130,150,180,170,200]
})

st.line_chart(df)

# ===== ALLOCATION =====
st.subheader("🌍 Allocation")

alloc = pd.DataFrame({
    "Asset": ["BTC","ALB","SQM","LIT"],
    "Weight": [0.4,0.3,0.2,0.1]
})

st.bar_chart(alloc.set_index("Asset"))

# ===== LOGS =====
st.subheader("🧠 Last Decisions")

st.text("BUY BTC | SELL SQM | HOLD ALB")
