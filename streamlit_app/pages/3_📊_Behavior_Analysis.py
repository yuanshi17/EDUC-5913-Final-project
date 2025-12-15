# streamlit_app/pages/3_📊_Behavior_Analysis.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st

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
        st.error("❌ Transformers not installed. Please install with: `pip install transformers torch`")
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
        'refusing', 'losing weight', 'not drinking', 'weak', 'sick',
        'coughing', 'sneezing', 'discharge', 'bleeding', 'pain'
    ]
    
    # Positive indicators for cats
    positive_keywords = [
        'playful', 'energetic', 'purring', 'affectionate', 'happy',
        'eating well', 'healthy', 'active', 'grooming', 'curious',
        'sleeping peacefully', 'good appetite', 'alert', 'friendly'
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
    Analyze your cat's behavior notes using advanced AI to understand their emotional and physical state.
    This tool detects concerning behaviors or positive changes.
    """)

    # Method selection
    st.subheader("🔧 Choose Analysis Method")
    method = st.radio(
        "Select your preferred analysis method:",
        [
            "🤗 Hugging Face AI (Most Accurate - Recommended)",
            "🐱 Cat-Specific Keywords (Rule-based)"
        ],
        help="Hugging Face uses state-of-the-art AI for best accuracy"
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
            - "Coughing and sneezing a lot"
            """)
        
        with col2:
            st.markdown("""
            **😊 Positive behaviors:**
            - "Playful and energetic today, ate well"
            - "Purring a lot, very affectionate and happy"
            - "Great appetite and sleeping peacefully"
            - "Curious and exploring, seems healthy"
            - "Grooming regularly and active"
            - "Alert and responsive to playtime"
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
            with st.spinner("Analyzing sentiment with AI..."):
                result = None
                
                # Choose analysis method
                if "Hugging Face" in method:
                    result = analyze_sentiment_huggingface(note)
                    if result is None:
                        st.info("Falling back to Cat-Specific Keywords analysis...")
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
                        st.markdown("#### 🎯 AI Confidence Score")
                        st.progress(result['confidence'])
                        st.caption(f"The AI model is {result['confidence']:.1%} confident in this prediction")
                        
                        # Show the raw label
                        st.metric("AI Classification", result['label'])
                    
                    elif "keywords" in result:
                        st.markdown("#### 🔑 Keywords Analysis")
                        st.metric("Relevant Keywords Found", result['keywords'])
                    
                    # Health recommendations
                    st.markdown("---")
                    st.subheader("💡 Veterinary Recommendations")
                    
                    if result['color'] == 'red':
                        st.error("""
                        **🚨 Concerning Behavior Detected**
                        
                        **Immediate Actions:**
                        - 📝 Monitor your cat closely for the next 24-48 hours
                        - 🍽️ Check eating, drinking, and litter box habits
                        - 🔍 Look for other symptoms (lethargy, vomiting, diarrhea)
                        - 📊 Keep a detailed behavior log with timestamps
                        - 🌡️ Check temperature if possible (normal: 100.5-102.5°F)
                        
                        **Contact Your Vet If:**
                        - ⏰ Symptoms persist for more than 24 hours
                        - 🚫 Cat refuses food/water for 12+ hours
                        - 😣 Shows signs of pain or severe distress
                        - ⚡ Any sudden or dramatic behavioral changes
                        - 🆘 Difficulty breathing, bleeding, or seizures
                        """)
                        
                    elif result['color'] == 'green':
                        st.success("""
                        **✅ Positive Behavior Noted**
                        
                        **Keep Up The Good Work:**
                        - 🍽️ Continue current routine and balanced diet
                        - 🎾 Maintain regular play sessions (15-20 min daily)
                        - 💧 Ensure fresh water is always available
                        - 🏥 Schedule regular vet check-ups (annual or bi-annual)
                        - 📝 Keep tracking behaviors for long-term patterns
                        - 🧼 Maintain regular grooming and litter box cleaning
                        """)
                        
                    else:
                        st.info("""
                        **ℹ️ Neutral Observation**
                        
                        **Continue Monitoring:**
                        - 👀 Normal daily activity noted
                        - 📊 Keep observing for any changes
                        - ✅ Maintain regular care routine
                        - 📝 Log behaviors for future reference
                        - 🔔 Watch for any patterns over time
                        """)
                    
                    # Additional tips
                    with st.expander("📚 Additional Cat Care Tips"):
                        st.markdown("""
                        ### General Cat Health Indicators
                        
                        **Healthy Cat Signs:**
                        - Clear, bright eyes
                        - Clean ears with no odor
                        - Healthy coat (shiny, no bald patches)
                        - Pink gums
                        - Normal breathing (20-30 breaths/min at rest)
                        - Regular eating and drinking
                        
                        **Warning Signs to Watch:**
                        - Changes in appetite or thirst
                        - Weight loss or gain
                        - Changes in litter box habits
                        - Excessive vocalization
                        - Hiding or withdrawal
                        - Vomiting or diarrhea
                        - Difficulty breathing
                        - Lethargy or decreased activity
                        """)

    # Installation guide
    st.markdown("---")
    with st.expander("⚙️ Setup & Installation Guide"):
        st.markdown("""
        ### 📦 Required Libraries
        
        This feature requires Hugging Face Transformers:
        
        ```bash
        pip install transformers torch
        ```
        
        ### 📄 Add to requirements.txt
        ```
        transformers
        torch
        ```
        
        ### ✅ Why Hugging Face Transformers?
        - 🎯 **Most Accurate**: State-of-the-art AI models
        - 🆓 **100% Free & Open Source**
        - 🔑 **No API Keys Required**
        - 💻 **Works Offline** after initial model download
        - 🧠 **Context Understanding**: Correctly identifies "too much" as negative
        - 🌍 **Widely Used**: Millions of downloads, well-maintained
        
        ### 🚀 First Run Note
        On first use, the model will download (~250MB). This happens once and then runs locally.
        """)

if __name__ == "__main__":
    behavior_analysis_page()