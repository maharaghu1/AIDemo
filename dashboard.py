# dashboard logic here


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime
import altair as alt
import time

PRIMARY_NAVY = "#0A1C3D"
PRIMARY_CYAN = "#00A9E0"
LIGHTER_NAVY = "#ADD8E6"
ACCENT_YELLOW = "#FFC72C"
NEUTRAL_WHITE = "#FFFFFF"

def app():
    st.markdown(f"""
        <style>
            section[data-testid="stSidebar"] {{
                background-color: {LIGHTER_NAVY} !important;
            }}
            h1 {{
                color: {LIGHTER_NAVY};
                text-align: center;
            }}
            .stButton>button {{
                background-color: {PRIMARY_CYAN};
                color: white;
                font-weight: bold;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.image("https://8e41335d61f2.ngrok-free.app/assets/logo.png", width=160)
    st.markdown("<h1>📊 WasteHawk Real-Time Dashboard</h1>", unsafe_allow_html=True)

    st.sidebar.header("🔧 Analytics Controls")
    run = st.sidebar.checkbox("▶️ Enable Real-Time Analytics", value=False)
    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 60, 15)

    if "detections" not in st.session_state:
        st.session_state.detections = pd.DataFrame()
        st.session_state.history = pd.DataFrame(columns=["time", "count"])
        st.session_state.last_refresh = datetime.now()

    if run:
        placeholder = st.empty()
        while run:
            now = datetime.now()
            if (now - st.session_state.last_refresh).total_seconds() >= refresh_interval:
                detections = pd.DataFrame([
                    {
                        "type": random.choice(["Trash Bag", "Couch", "Mattress", "Appliance", "Debris"]),
                        "lat": 34.0136 + random.uniform(-0.001, 0.001),
                        "lon": -118.2479 + random.uniform(-0.001, 0.001),
                        "time": now.strftime("%H:%M:%S")
                    }
                    for _ in range(random.randint(3, 6))
                ])
                st.session_state.detections = detections
                st.session_state.last_refresh = now
                st.session_state.history = pd.concat([
                    st.session_state.history,
                    pd.DataFrame([{"time": now, "count": len(detections)}])
                ], ignore_index=True)

            with placeholder.container():
                detections = st.session_state.detections

                col1, col2, col3 = st.columns(3)
                col1.metric("Total Detections", len(detections))
                col2.metric("Detection Accuracy", f"{random.uniform(92.5, 98.8):.1f}%")
                col3.metric("Drone Status", "🟢 Online")

                st.markdown(f"<h3 style='color:{PRIMARY_CYAN};'>📷 Simulated Drone Camera Feed</h3>", unsafe_allow_html=True)
                st.image("https://cdn.pixabay.com/photo/2020/07/31/19/25/dump-5457190_1280.jpg",
                        caption="Live Drone Feed", use_column_width=True)

                st.markdown(f"<h3 style='color:{PRIMARY_CYAN};'>🗺️ Live Detection Map</h3>", unsafe_allow_html=True)
                map_obj = folium.Map(location=[34.0136, -118.2479], zoom_start=16)
                for _, row in detections.iterrows():
                    folium.Marker(
                        location=[row["lat"], row["lon"]],
                        popup=f"{row['type']} at {row['time']}",
                        icon=folium.Icon(color="red", icon="trash", prefix="fa")
                    ).add_to(map_obj)
                st_folium(map_obj, width=700, height=450)

                st.markdown(f"<h3 style='color:{PRIMARY_CYAN};'>📋 Detection Log</h3>", unsafe_allow_html=True)
                st.dataframe(detections, use_container_width=True)

                st.markdown(f"<h3 style='color:{PRIMARY_CYAN};'>📈 Detection History</h3>", unsafe_allow_html=True)
                history = st.session_state.history
                if not history.empty:
                    chart = alt.Chart(history).mark_line(point=True).encode(
                        x="time:T",
                        y="count:Q"
                    ).properties(width=700, height=300).interactive()
                    st.altair_chart(chart)

                st.markdown(f"<small style='color:{LIGHTER_NAVY};'>⏳ Last updated: {st.session_state.last_refresh.strftime('%H:%M:%S')}</small>", unsafe_allow_html=True)
                time.sleep(refresh_interval)
                st.rerun()
    else:
        st.warning("Analytics are paused. Use the sidebar to enable real-time simulation.")
