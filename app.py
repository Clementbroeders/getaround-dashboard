### LIBRAIRIES ###
import streamlit as st
import pandas as pd
import requests


### CONFIGURATION ###
st.set_page_config(
    page_title="Get-Around dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("📊 Get-Around Dashboard 📊")

### FOOTER ###
st.markdown("""
    <p style='text-align:center;'>
        Powered by <a href='https://streamlit.io/'>Streamlit</a>. © 2024 Clément Broeders.
    </p>
""", unsafe_allow_html=True)