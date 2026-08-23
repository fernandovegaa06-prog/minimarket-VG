import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

st.set_page_config(page_title="Minimarket Vega", page_icon="🛒", layout="centered")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(-45deg, #0f766e, #115e59, #0d9488, #134e4a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        color: #0f766e;
        margin-bottom: 20px;
    }
    h1, h2, h3, p, label { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🛒 Minimarket Vega</h1><p>Sistema funcionando correctamente.</p></div>', unsafe_allow_html=True)
st.success("¡El sistema ya arrancó sin errores! Ahora puedes empezar a añadir tus funciones.")
