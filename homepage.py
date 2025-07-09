
import streamlit as st
from homepage import app as homepage_app
from dashboard import app as dashboard_app
from storage_analytics import app as storage_app

PAGES = {
    "🏠 Homepage": homepage_app,
    "📊 Real-Time Dashboard": dashboard_app,
    "🗄️ Storage Analytics": storage_app
}

st.sidebar.title("WasteHawk Navigation")
page = st.sidebar.radio("Go to", list(PAGES.keys()))
PAGES[page]()
