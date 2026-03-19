import streamlit as st
import requests
import pandas as pd
import numpy as np
import time

st.set_page_config(layout="wide")

st.title("🔥 Bookmap Pro (Heatmap Histórico)")

API = "http://localhost:8000/data"

history = []

placeholder = st.empty()

while True:
    try:
        data = requests.get(API).json()

        heat = pd.DataFrame(data["heatmap"])

        # salvar histórico
        history.append(heat["size"].values)

        if len(history) > 100:
            history.pop(0)

        heatmap_matrix = np.array(history)

        with placeholder.container():

            col1, col2 = st.columns(2)

            st.subheader("🔥 Heatmap Histórico (Tempo x Liquidez)")
            st.image(heatmap_matrix, clamp=True)

            # footprint
            fp = pd.DataFrame.from_dict(data["footprint"], orient="index")

            st.subheader("📊 Footprint")
            st.bar_chart(fp)

            # delta
            st.metric("Delta", data["delta"])

            st.subheader("🧱 Walls")
            st.json(data["walls"])

            st.subheader("🚨 Spoof")
            st.json(data["spoof"])

    except Exception as e:
        st.write("Erro:", e)

    time.sleep(1)
