# streamlit_app/Behavior_Analysis.py
import streamlit as st
from modules.nlp_utils import analyze_text_sentiment, extract_keywords

def behavior_analysis_page():
    """Behavior & NLP Analysis Page"""
    st.title("🐾 Behavior Analysis")

    st.subheader("Analyze Cat Behavior Notes")
    note = st.text_area("Enter cat behavior notes or sounds")
    if st.button("Analyze"):
        if note.strip() == "":
            st.warning("Please enter some notes!")
        else:
            result = analyze_text_sentiment()
            st.success(f"Analysis Result: {result}")

if __name__ == "__main__":
    behavior_analysis_page()