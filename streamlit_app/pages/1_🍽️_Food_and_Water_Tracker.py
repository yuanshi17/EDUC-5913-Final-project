# streamlit_app/pages/1_🍽️_Food_and_Water_Tracker.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import pandas as pd
from modules.data_loader import load_csv, save_csv

def food_tracker_page():
    """Food and Water Tracker Page"""
    st.title("🍽️ Food and Water Tracker")
    
    st.markdown("""
    Track your cat's daily food and water intake.
    """)
    
    data_file = "data/feeding_log.csv"
    
    try:
        df = load_csv(data_file)
        if not df.empty:
            st.subheader("📊 Feeding Log")
            st.dataframe(df, use_container_width=True)
    except:
        st.info("No feeding data yet. Start by adding your first record below!")
        df = pd.DataFrame()

    st.subheader("➕ Add Feeding Record")
    
    col1, col2 = st.columns(2)
    with col1:
        new_food = st.number_input("Food amount (g)", min_value=0)
        new_water = st.number_input("Water amount (ml)", min_value=0)
    with col2:
        new_weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f")
        new_date = st.date_input("Date")

    if st.button("💾 Add Record", type="primary"):
        new_row = {
            "date": str(new_date),
            "food_amount_g": new_food,
            "water_amount_ml": new_water,
            "weight_kg": new_weight
        }
        if df.empty:
            df = pd.DataFrame([new_row])
        else:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_csv(df, data_file)
        st.success("✅ Record added successfully!")
        st.balloons()
        st.rerun()

if __name__ == "__main__":
    food_tracker_page()