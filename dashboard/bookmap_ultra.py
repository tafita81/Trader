import streamlit as st
import requests
import pandas as pd
import numpy as np
import time

st.set_page_config(layout="wide")

st.title("🚀 Bookmap Ultra (Heatmap + Replay + Alerts)")

API = "http://localhost:8000/data"

if "history" not in st.session_state:
    st.session_state.history = []

if "replay_idx" not in st.session_state:
    st.session_state.replay_idx = 0

placeholder = st.empty()

mode = st.sidebar.selectbox("Modo", ["Tempo Real", "Replay"])

alert_threshold = st.sidebar.slider("Alerta Liquidez", 1000, 100000, 5000)

while True:
    try:
        data = requests.get(API).json()

        heat = pd.DataFrame(data["heatmap"])

        st.session_state.history.append(heat["size"].values)

        if len(st.session_state.history) > 200:
            st.session_state.history.pop(0)

        if mode == "Replay":
            idx = st.sidebar.slider("Frame", 0, len(st.session_state.history)-1, st.session_state.replay_idx)
            matrix = np.array(st.session_state.history[:idx+1])
        else:
            matrix = np.array(st.session_state.history)

        # normalização para cor
        norm = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix) + 1e-9)

        with placeholder.container():

            st.subheader("🔥 Heatmap Profissional")
            st.image(norm, clamp=True)

            # ALERTA
            if np.max(matrix) > alert_threshold:
                st.error("🚨 ALERTA: Liquidez institucional detectada!")

            col1, col2 = st.columns(2)

            with col1:
                fp = pd.DataFrame.from_dict(data["footprint"], orient="index")
                st.subheader("📊 Footprint")
                st.bar_chart(fp)

            with col2:
                st.metric("Delta", data["delta"])
                st.json(data["walls"])

    except Exception as e:
        st.write("Erro:", e)

    time.sleep(1)
