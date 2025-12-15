# streamlit_app/pages/3_📊_Behavior_Analysis.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st

def analyze_sentiment_textblob(text):
    """Analyze sentiment using TextBlob - lightweight and accurate"""
    try:
        from textblob import TextBlob
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Enhanced thresholds for better accuracy
        if polarity > 0.15:
            sentiment = "Positive 😊"
            color = "green"
            description = "Your cat seems to be doing well!"
        elif polarity < -0.15:
            sentiment = "Negative 😟"
            color = "red"
            description = "This may indicate a concerning behavior."
        else:
            sentiment = "Neutral 😐"
            color = "gray"
            description = "Normal observation."
            
        return {
            "sentiment": sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity,
            "color": color,
            "description": description
        }
    except ImportError:
        return None

def analyze_sentiment_huggingface(text):
    """Analyze sentiment using Hugging Face Transformers - most accurate"""
    try:
        from transformers import pipeline
        
        # Load pre-trained sentiment analysis model
        # This model is specifically trained for nuanced sentiment detection
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        
        # Get prediction
        result = sentiment_pipeline(text)[0]
        label = result['label']
        score = result['score']
        
        # Map to user-friendly format
        if label == "POSITIVE":
            sentiment = "Positive 😊"
            color = "green"
            description = "Your cat seems to be doing well!"
        else:  # NEGATIVE
            sentiment = "Negative 😟"
            color = "red"
            description = "This may indicate a concerning behavior."
        
        return {
            "sentiment": sentiment,
            "label": label,
            "confidence": score,
            "color": color,
            "description": description
        }
    except ImportError:
        return None
    except Exception as e:
        st.error(f"Error with Hugging Face model: {str(e)}")
        return None

def get_cat_specific_interpretation(text):
    """Provide cat-specific behavioral interpretation"""
    text_lower = text.lower()
    
    # Negative indicators for cats
    negative_keywords = [
        'too much', 'vomit', 'lethargic', 'aggressive', 'hissing',
        'not eating', 'depressed', 'hiding', 'crying', 'limping',
        'blood', 'diarrhea', 'scratching excessively', 'biting',
        'refusing', 'losing weight', 'not drinking'
    ]
    
    # Positive indicators for cats
    positive_keywords = [
        'playful', 'energetic', 'purring', 'affectionate', 'happy',
        'eating well', 'healthy', 'active', 'grooming', 'curious',
        'sleeping peacefully', 'good appetite'
    ]
    
    negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
    positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
    
    if negative_count > positive_count:
        return "negative", negative_count
    elif positive_count > negative_count:
        return "positive", positive_count
    else:
        return "neutral", 0

def behavior_analysis_page():
    """Behavior & NLP Analysis Page"""
    
    st.title("🐾 Behavior Analysis")
    
    st.markdown("""
    Analyze your cat's behavior notes to understand their emotional and physical state.
    This tool uses AI to detect concerning behaviors or positive changes.
    """)

    # Method selection
    st.subheader("🔧 Choose Analysis Method")
    method = st.radio(
        "Select your preferred AI model:",
        [
            "🤗 Hugging Face (Most Accurate - Recommended)",
            "📝 TextBlob (Fast & Lightweight)",
            "🐱 Cat-Specific Keywords (Rule-based)"
        ],
        help="Hugging Face uses advanced AI models for best accuracy"
    )

    # Example notes
    with st.expander("💡 See Example Notes"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **😟 Concerning behaviors:**
            - "Cat eats too much and vomits frequently"
            - "Very lethargic, not playing, seems depressed"
            - "Aggressive, hissing at everyone"
            - "Not eating or drinking for 2 days"
            - "Hiding under bed, refuses to come out"
            """)
        
        with col2:
            st.markdown("""
            **😊 Positive behaviors:**
            - "Playful and energetic today, ate well"
            - "Purring a lot, very affectionate and happy"
            - "Great appetite and sleeping peacefully"
            - "Curious and exploring, seems healthy"
            - "Grooming regularly and active"
            """)
    
    st.markdown("---")
    
    # Text input
    st.subheader("📝 Enter Cat Behavior Notes")
    note = st.text_area(
        "Describe your cat's behavior:",
        placeholder="e.g., Cat seems very tired today, not eating much and hiding under the bed...",
        height=120
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    if analyze_button:
        if note.strip() == "":
            st.warning("⚠️ Please enter some notes to analyze!")
        else:
            with st.spinner("Analyzing sentiment..."):
                result = None
                
                # Choose analysis method
                if "Hugging Face" in method:
                    result = analyze_sentiment_huggingface(note)
                    if result is None:
                        st.error("❌ Hugging Face not available. Install with: `pip install transformers torch`")
                        st.info("Falling back to TextBlob analysis...")
                        result = analyze_sentiment_textblob(note)
                
                elif "TextBlob" in method:
                    result = analyze_sentiment_textblob(note)
                    if result is None:
                        st.error("❌ TextBlob not available. Install with: `pip install textblob`")
                
                else:  # Cat-Specific Keywords
                    cat_sentiment, keyword_count = get_cat_specific_interpretation(note)
                    if cat_sentiment == "negative":
                        result = {
                            "sentiment": "Negative 😟",
                            "color": "red",
                            "description": f"Found {keyword_count} concerning keyword(s)",
                            "keywords": keyword_count
                        }
                    elif cat_sentiment == "positive":
                        result = {
                            "sentiment": "Positive 😊",
                            "color": "green",
                            "description": f"Found {keyword_count} positive keyword(s)",
                            "keywords": keyword_count
                        }
                    else:
                        result = {
                            "sentiment": "Neutral 😐",
                            "color": "gray",
                            "description": "No strong indicators detected",
                            "keywords": 0
                        }
                
                # Display results
                if result:
                    st.markdown("---")
                    st.subheader("📊 Analysis Results")
                    
                    # Main sentiment display
                    st.markdown(f"### Overall Sentiment: :{result['color']}[{result['sentiment']}]")
                    st.info(result['description'])
                    
                    # Detailed metrics
                    if "confidence" in result:
                        st.markdown("#### 🎯 Confidence Score")
                        st.progress(result['confidence'])
                        st.caption(f"Model is {result['confidence']:.1%} confident in this prediction")
                    
                    elif "polarity" in result:
                        st.markdown("#### 📈 Sentiment Scores")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Polarity", f"{result['polarity']:.3f}", 
                                     help="Range: -1 (negative) to +1 (positive)")
                        with col2:
                            st.metric("Subjectivity", f"{result['subjectivity']:.3f}",
                                     help="Range: 0 (objective) to 1 (subjective)")
                    
                    elif "keywords" in result:
                        st.markdown("#### 🔑 Keywords Found")
                        st.metric("Relevant Keywords", result['keywords'])
                    
                    # Health recommendations
                    st.markdown("---")
                    st.subheader("💡 Recommendations")
                    
                    if result['color'] == 'red':
                        st.error("""
                        **🚨 Concerning Behavior Detected**
                        
                        **Immediate Actions:**
                        - Monitor your cat closely for the next 24-48 hours
                        - Check eating, drinking, and litter box habits
                        - Look for other symptoms (lethargy, vomiting, etc.)
                        - Keep a behavior log with timestamps
                        
                        **When to Contact Vet:**
                        - Symptoms persist for more than 24 hours
                        - Cat refuses food/water for 12+ hours
                        - Shows signs of pain or distress
                        - Any sudden behavioral changes
                        """)
                        
                    elif result['color'] == 'green':
                        st.success("""
                        **✅ Positive Behavior Noted**
                        
                        **Keep It Up:**
                        - Continue current routine and diet
                        - Maintain regular play sessions
                        - Ensure fresh water is always available
                        - Schedule regular vet check-ups
                        - Keep tracking behaviors for patterns
                        """)
                        
                    else:
                        st.info("""
                        **ℹ️ Neutral Observation**
                        
                        **Continue Monitoring:**
                        - Normal daily activity noted
                        - Keep observing for any changes
                        - Maintain regular care routine
                        - Log behaviors for future reference
                        """)

    # Installation guide
    st.markdown("---")
    with st.expander("⚙️ Setup & Installation Guide"):
        st.markdown("""
        ### 📦 Required Libraries
        
        Choose one or both methods:
        
        #### Option 1: Hugging Face (Recommended - Most Accurate)
        ```bash
        pip install transformers torch
        ```
        
        #### Option 2: TextBlob (Lightweight Alternative)
        ```bash
        pip install textblob
        python -m textblob.download_corpora
        ```
        
        #### Option 3: Both (Best of Both Worlds)
        ```bash
        pip install transformers torch textblob
        python -m textblob.download_corpora
        ```
        
        ### 📄 Add to requirements.txt
        ```
        transformers
        torch
        textblob
        ```
        
        ### ✅ Why These Libraries?
        - **100% Free & Open Source**
        - **No API Keys Required**
        - **Works Offline**
        - **State-of-the-art Accuracy**
        - **Widely Used & Well-Maintained**
        
        The Hugging Face model correctly understands context like "too much" as negative!
        """)

if __name__ == "__main__":
    behavior_analysis_page()