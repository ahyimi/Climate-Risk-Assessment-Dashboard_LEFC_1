# -*- coding: utf-8 -*-
"""
Created on Tue May 13 11:00:11 2025

@author: Imee
"""

# lyari_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Lyari Freight Corridor Climate Risk Dashboard")

st.sidebar.header("Simulation Settings")
rainfall_threshold = st.sidebar.slider("Flood Trigger (mm/year)", 100, 300, 200)
heatwave_threshold = st.sidebar.slider("Heatwave Threshold (°C)", 35, 50, 45)
ndvi_threshold = st.sidebar.slider("Drought NDVI Threshold", 0.0, 0.5, 0.2)
max_loss = st.sidebar.number_input("Max Annual Economic Loss (USD)", value=10_000_000)

uploaded_file = st.file_uploader("Upload climate risk data (CSV)", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Sample synthetic dataset
    df = pd.DataFrame({
        "Year": list(range(1925, 2025)),
        "Rainfall_mm": [150 + i % 70 for i in range(100)],
        "Max_Temp_C": [43 + i % 7 for i in range(100)],
        "NDVI": [0.25 - 0.01 * (i % 5) for i in range(100)]
    })

# Flag risks
df["Flood"] = df["Rainfall_mm"] > rainfall_threshold
df["Heatwave"] = df["Max_Temp_C"] > heatwave_threshold
df["Drought"] = df["NDVI"] < ndvi_threshold

# Calculate disruption probability
df["Disruption_Prob"] = (
    0.6 * df["Flood"].astype(int) +
    0.25 * df["Heatwave"].astype(int) +
    0.15 * df["Drought"].astype(int)
)
df["Econ_Loss_USD"] = df["Disruption_Prob"] * max_loss

st.subheader("Climate Risk Summary Table")
st.dataframe(df[["Year", "Rainfall_mm", "Max_Temp_C", "NDVI", "Flood", "Heatwave", "Drought", "Disruption_Prob", "Econ_Loss_USD"]])

st.subheader("Disruption Probability Over Time")
st.line_chart(df.set_index("Year")["Disruption_Prob"])

st.subheader("Economic Loss Over Time (USD)")
st.line_chart(df.set_index("Year")["Econ_Loss_USD"])

st.success("Done. Use the sidebar to change thresholds and re-simulate.")
