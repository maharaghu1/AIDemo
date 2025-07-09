# storage analytics logic here


import streamlit as st
import random

def app():
    st.markdown("<h1 style='text-align:center; color:#3B7A57;'>🗄️ WasteHawk Storage Analytics</h1>", unsafe_allow_html=True)

    st.markdown("This dashboard provides insights into data usage, storage trends, and analytics from detections stored by the system.")

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Storage Used", f"{random.uniform(0.5, 2.3):.2f} GB")
    col2.metric("📁 Logs Archived", f"{random.randint(50, 200)} files")
    col3.metric("🧠 AI Model Versions", random.randint(3, 8))

    st.markdown("### 🧮 Storage Breakdown by Category")
    st.bar_chart({
        "Trash Logs": [random.randint(100, 400)],
        "Drone Images": [random.randint(200, 800)],
        "AI Results": [random.randint(150, 500)]
    })

    st.markdown("### 🕓 Weekly Growth Rate (GB)")
    st.line_chart({
        "Week": [1, 2, 3, 4],
        "Growth": [0.3, 0.6, 1.0, random.uniform(1.2, 1.8)]
    })
