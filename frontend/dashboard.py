import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Quant Trading Dashboard")

try:
    df = pd.read_parquet("data/final_dataset.parquet")
except:
    st.error("Dataset não encontrado. Rode o pipeline primeiro.")
    st.stop()

# KPIs
st.subheader("📈 KPIs")
col1, col2, col3 = st.columns(3)

returns = df["ret"].dropna()

col1.metric("Retorno médio", f"{returns.mean():.4f}")
col2.metric("Volatilidade", f"{returns.std():.4f}")
col3.metric("Sharpe", f"{(returns.mean()/(returns.std()+1e-9)):.2f}")

# Equity Curve
st.subheader("💰 Equity Curve")
if "equity" in df.columns:
    st.line_chart(df.set_index("Datetime")["equity"])

# Preço
st.subheader("📉 Preço")
ticker = st.selectbox("Ativo", df["ticker"].unique())
data = df[df["ticker"] == ticker]
st.line_chart(data.set_index("Datetime")["Close"])

# Indicadores
st.subheader("📊 Indicadores")
st.line_chart(data.set_index("Datetime")[["rsi","vol_spike"]])

# Sinais
st.subheader("🚨 Sinais recentes")
cols = [c for c in ["Datetime","buy","sell"] if c in data.columns]
st.dataframe(data[cols].tail(20))
