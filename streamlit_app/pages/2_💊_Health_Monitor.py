# streamlit_app/Health_Monitor.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modules.data_loader import load_csv, save_csv

def health_monitor_page():
    """Cat Health Monitor Page"""

    # 页面标题
    st.title("🐱 Cat Health Monitor")

    # 数据文件
    data_file = "data/feeding_log.csv"

    # 加载数据
    df = load_csv(data_file)

    # 显示最新状态
    st.subheader("📊 Current Status")
    if df.empty:
        st.info("No data available yet. Add feeding/water records first!")
    else:
        latest = df.iloc[-1]
        st.metric("Food Remaining (g)", latest.get("food_amount_g", 0))
        st.metric("Water Remaining (ml)", latest.get("water_amount_ml", 0))
        st.metric("Weight (kg)", latest.get("weight_kg", "N/A"))

    # 绘制历史趋势图
    if not df.empty:
        st.subheader("📈 Historical Trends")
        fig, ax = plt.subplots(figsize=(10, 5))

        if "food_amount_g" in df.columns:
            ax.plot(df["date"], df["food_amount_g"], label="Food (g)", marker="o")
        if "water_amount_ml" in df.columns:
            ax.plot(df["date"], df["water_amount_ml"], label="Water (ml)", marker="^")
        if "weight_kg" in df.columns:
            ax.plot(df["date"], df["weight_kg"], label="Weight (kg)", marker="s")

        ax.set_xlabel("Date")
        ax.set_ylabel("Amount / Unit")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # 下载数据按钮
    st.subheader("💾 Download Data")
    if st.button("Download CSV"):
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="cat_health_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    health_monitor_page()