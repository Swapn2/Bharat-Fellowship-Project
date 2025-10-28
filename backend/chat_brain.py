# backend/chat_brain.py
import pandas as pd
from backend.data_analyzer import analyze_data

def chat_brain(user_input, cleaned_path):
    """
    Handles user queries and maps them to analysis intents.
    """
    text = user_input.lower().strip()

    # Basic NLP-style intent mapping
    if "district" in text:
        intent = "distinct_districts"
    elif "market" in text:
        intent = "distinct_markets"
    elif "commodity" in text and "top" in text:
        intent = "top_commodities"
    elif "mean" in text or "average" in text:
        intent = "mean_modal"
    elif "price" in text and ("min" in text or "max" in text):
        intent = "price_stats"
    elif "correlation" in text:
        intent = "correlation"
    else:
        return "⚠️ Sorry, I couldn’t understand that request."

    # Analyze based on identified intent
    result = analyze_data(intent, cleaned_path)
    return result
