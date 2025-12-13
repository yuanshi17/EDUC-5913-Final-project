# modules/nlp_utils.py
import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_text(text):
    """Return basic token analysis"""
    doc = nlp(text)
    return [(token.text, token.lemma_, token.pos_, token.is_stop) for token in doc]

def get_nouns(text):
    """Return nouns in the text"""
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ == "NOUN"]
