# streamlit_app/pages/3_📊_Behavior_Analysis.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st

def analyze_sentiment_textblob(text):
    """Analyze sentiment using TextBlob"""
    try:
        from textblob import TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Polarity ranges from -1 (negative) to 1 (positive)
        if polarity > 0.1:
            sentiment = "Positive 😊"
            color = "green"
        elif polarity < -0.1:
            sentiment = "Negative 😟"
            color = "red"
        else:
            sentiment = "Neutral 😐"
            color = "gray"
            
        return {
            "sentiment": sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity,
            "color": color
        }
    except ImportError:
        st.error("TextBlob not installed. Install with: pip install textblob")
        return None

def analyze_sentiment_vader(text):
    """Analyze sentiment using VADER (better for social media/short texts)"""
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        
        # Get compound score (ranges from -1 to 1)
        compound = scores['compound']
        
        # VADER classification thresholds
        if compound >= 0.05:
            sentiment = "Positive 😊"
            color = "green"
        elif compound <= -0.05:
            sentiment = "Negative 😟"
            color = "red"
        else:
            sentiment = "Neutral 😐"
            color = "gray"
            
        return {
            "sentiment": sentiment,
            "compound": compound,
            "positive": scores['pos'],
            "neutral": scores['neu'],
            "negative": scores['neg'],
            "color": color
        }
    except ImportError:
        st.error("VADER not installed. Install with: pip install vaderSentiment")
        return None

def behavior_analysis_page():
    """Behavior & NLP Analysis Page"""
    st.title("🐾 Behavior Analysis")
    
    st.markdown("""
    Analyze your cat's behavior notes to understand sentiment and emotional patterns.
    This tool helps identify concerning behaviors or positive changes.
    """)

    # Method selection
    method = st.radio(
        "Choose Analysis Method:",
        ["VADER (Recommended for short texts)", "TextBlob (Better for longer descriptions)"],
        help="VADER is great for social media-style text, TextBlob works well for formal text"
    )

    st.subheader("📝 Enter Cat Behavior Notes")
    
    # Example notes
    with st.expander("💡 See Example Notes"):
        st.markdown("""
        **Concerning behaviors:**
        - "Cat eats too much and vomits frequently"
        - "Very lethargic, not playing, seems depressed"
        - "Aggressive, hissing at everyone"
        
        **Positive behaviors:**
        - "Playful and energetic today, ate well"
        - "Purring a lot, very affectionate and happy"
        - "Great appetite and sleeping peacefully"
        
        **Neutral observations:**
        - "Cat slept most of the day"
        - "Ate normal amount of food"
        """)
    
    note = st.text_area(
        "Behavior notes:",
        placeholder="e.g., Cat seems very tired today, not eating much...",
        height=100
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        analyze_button = st.button("🔍 Analyze", type="primary")
    
    if analyze_button:
        if note.strip() == "":
            st.warning("⚠️ Please enter some notes to analyze!")
        else:
            with st.spinner("Analyzing sentiment..."):
                if "VADER" in method:
                    result = analyze_sentiment_vader(note)
                else:
                    result = analyze_sentiment_textblob(note)
                
                if result:
                    st.markdown("---")
                    st.subheader("📊 Analysis Results")
                    
                    # Display sentiment with color
                    st.markdown(f"### Overall Sentiment: :{result['color']}[{result['sentiment']}]")
                    
                    # Display detailed scores
                    st.markdown("#### Detailed Scores:")
                    
                    if "VADER" in method:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Compound", f"{result['compound']:.3f}")
                        with col2:
                            st.metric("Positive", f"{result['positive']:.1%}")
                        with col3:
                            st.metric("Neutral", f"{result['neutral']:.1%}")
                        with col4:
                            st.metric("Negative", f"{result['negative']:.1%}")
                        
                        st.info("""
                        **How to interpret:**
                        - **Compound score**: Overall sentiment (-1 to +1)
                        - **Positive/Neutral/Negative**: Percentage of each emotion type
                        - Values closer to -1 indicate negative sentiment
                        - Values closer to +1 indicate positive sentiment
                        """)
                    else:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Polarity", f"{result['polarity']:.3f}")
                        with col2:
                            st.metric("Subjectivity", f"{result['subjectivity']:.3f}")
                        
                        st.info("""
                        **How to interpret:**
                        - **Polarity**: Sentiment direction (-1 = negative, +1 = positive)
                        - **Subjectivity**: Opinion vs fact (0 = objective, 1 = subjective)
                        """)
                    
                    # Health recommendations based on sentiment
                    if result['color'] == 'red':
                        st.error("""
                        🚨 **Concerning Behavior Detected**
                        
                        The sentiment analysis suggests negative behavioral patterns. Consider:
                        - Monitoring your cat closely for the next 24-48 hours
                        - Checking for changes in eating, drinking, or litter box habits
                        - Consulting your veterinarian if symptoms persist
                        """)
                    elif result['color'] == 'green':
                        st.success("""
                        ✅ **Positive Behavior Noted**
                        
                        Your cat seems to be doing well! Continue:
                        - Maintaining their current routine
                        - Providing engaging activities
                        - Regular health check-ups
                        """)
                    else:
                        st.info("""
                        ℹ️ **Neutral Observation**
                        
                        Normal daily activity. Keep monitoring for any changes.
                        """)

    # Installation instructions
    with st.expander("⚙️ Setup Instructions"):
        st.markdown("""
        ### Required Libraries
        
        To use this feature, you need to install sentiment analysis libraries:
        
        **For VADER (Recommended):**
        ```bash
        pip install vaderSentiment
        ```
        
        **For TextBlob:**
        ```bash
        pip install textblob
        python -m textblob.download_corpora
        ```
        
        Both libraries are free, open-source, and work offline (no API key needed)!
        """)

if __name__ == "__main__":
    behavior_analysis_page()