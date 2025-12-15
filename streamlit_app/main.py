# main.py
import streamlit as st
from streamlit_app.Home import home_page
from streamlit_app.Health_Monitor import health_monitor_page
from streamlit_app.Food_and_Water_Tracker import food_and_water_tracker_page
from streamlit_app.Behavior_Analysis import behavior_analysis_page

st.set_page_config(page_title="🐱 Virtual Cat Monitor", layout="centered")

# Sidebar Nevigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Health Monitor", "Food Tracker", "Behavior Analysis"])

if page == "Home":
    home_page()
elif page == "Health Monitor":
    health_monitor_page()
elif page == "Food and Water Tracker":
    food_and_water_tracker_page()
elif page == "Behavior Analysis":
    behavior_analysis_page()