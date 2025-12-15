# streamlit_app/Home.py
import sys
import os
# Add project root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from modules.data_loader import load_csv, save_csv

def home_page():
    """Home Page"""
    st.markdown("<h1 style='font-size: 3.5rem;'>🏠 Smart Cat</h1>", unsafe_allow_html=True)
    st.markdown("""
    Welcome to the Cat Care App!  
    Track your cat's food, water, and activities in one place.
    """)

    # Load cat data
    data_file = "data/sample_data.csv"
    
    try:
        df = load_csv(data_file)
        if df.empty:
            st.info("No data available. Start tracking your cat's activities!")
        else:
            st.subheader("🐾 Cat Activity Data")
            st.dataframe(df)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.info("No data available yet. Start by uploading your first CSV file below!")
        df = pd.DataFrame()  # Create empty DataFrame

    # Upload new data
    st.subheader("Upload New Activity Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        st.success(f"Uploaded {len(new_df)} rows!")
        st.dataframe(new_df)
        save_csv(new_df, data_file)
        st.success("Data saved locally!")
        st.rerun()  # Reload page to display new data

home_page()