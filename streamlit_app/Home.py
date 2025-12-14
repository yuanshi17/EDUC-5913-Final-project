# streamlit_app/Home.py
import streamlit as st
import pandas as pd
from modules.data_loader import load_csv, save_csv

def home_page():
    """Home Page"""
    st.title("🏠 Cat Care Home")
    st.markdown("""
    Welcome to the Cat Care App!  
    Track your cat's food, water, and activities in one place.
    """)

    # 加载猫咪数据
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
        df = pd.DataFrame()  # 创建空的 DataFrame

    # 上传新数据
    st.subheader("Upload New Activity Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        st.success(f"Uploaded {len(new_df)} rows!")
        st.dataframe(new_df)
        save_csv(new_df, data_file)
        st.success("Data saved locally!")
        st.rerun()  # 重新加载页面以显示新数据

home_page()