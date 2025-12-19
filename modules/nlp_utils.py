# modules/nlp_utils.py
from textblob import TextBlob
import nltk

# Auto-downloading necessary data
try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown', quiet=True)
    nltk.download('punkt', quiet=True)

def analyze_text_sentiment(text):
    """Return sentiment as Positive / Neutral / Negative"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def extract_keywords(text, top_n=5):
    """Return top N keywords based on frequency"""
    words = text.lower().split()
    stop_words = {"the", "is", "a", "and", "of", "in", "to", "for"}
    keywords = [w for w in words if w not in stop_words]
    freq = {}
    for w in keywords:
        freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w[0] for w in sorted_words[:top_n]]
