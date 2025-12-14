# streamlit_app/Food_Tracker.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 然后是原来的导入
import streamlit as st
import pandas as pd
from modules.data_loader import load_csv, save_csv

def food_tracker_page():
    """Food Tracker Page"""
    st.title("🍽️ Cat Food Tracker")

    data_file = "data/feeding_log.csv"
    df = load_csv(data_file)

    if df.empty:
        st.info("No feeding data yet!")
    else:
        st.subheader("Feeding Log")
        st.dataframe(df)

    st.subheader("Add Feeding Record")
    new_food = st.number_input("Food amount (g)", min_value=0)
    new_water = st.number_input("Water amount (ml)", min_value=0)
    new_weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f")
    new_date = st.date_input("Date")

    if st.button("Add Record"):
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
        st.success("Record added!")

if __name__ == "__main__":
    food_tracker_page()