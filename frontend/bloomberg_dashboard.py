import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("📊 Bloomberg-Level Quant Dashboard")

# Load data
try:
    df = pd.read_parquet("data/final_dataset.parquet")
except:
    st.error("Dataset não encontrado. Rode o pipeline.")
    st.stop()

# KPIs
returns = df["ret"].dropna()
sharpe = returns.mean() / (returns.std() + 1e-9)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Sharpe", f"{sharpe:.2f}")
col2.metric("Retorno Médio", f"{returns.mean():.4f}")
col3.metric("Volatilidade", f"{returns.std():.4f}")
col4.metric("Trades", len(df))

# Equity
st.subheader("💰 Equity Curve")
if "equity" in df.columns:
    st.line_chart(df.set_index("Datetime")["equity"])

# Drawdown
st.subheader("⚠️ Drawdown")
peak = np.maximum.accumulate(df["equity"])
dd = (df["equity"] - peak) / peak
st.line_chart(dd)

# Heatmap correlação
st.subheader("🔥 Correlação entre ativos")
pivot = df.pivot(index="Datetime", columns="ticker", values="ret")
st.dataframe(pivot.corr())

# Ranking
st.subheader("🏆 Ranking de ativos")
latest = df.sort_values("Datetime").groupby("ticker").tail(1)
ranking = latest.sort_values("ret", ascending=False)
st.dataframe(ranking[["ticker","ret","Close"]])

# Intraday preview
st.subheader("⚡ Últimos dados")
st.dataframe(df.tail(50))
