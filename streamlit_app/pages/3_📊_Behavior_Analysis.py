# streamlit_app/pages/3_📊_Behavior_Analysis.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Then import the original modules
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
            # Pass the note parameter to the function
            result = analyze_text_sentiment(note)
            st.success(f"Analysis Result: {result}")
            
            # Optionally, also extract keywords if available
            try:
                keywords = extract_keywords(note)
                if keywords:
                    st.info(f"Key themes: {', '.join(keywords)}")
            except Exception as e:
                # Skip keyword extraction if it fails
                pass

if __name__ == "__main__":
    behavior_analysis_page()