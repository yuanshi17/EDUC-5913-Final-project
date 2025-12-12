# modules/utils.py
from datetime import datetime

def current_timestamp():
    """Return current timestamp as string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_weight(kg):
    """Format weight with 2 decimal places"""
    return f"{kg:.2f} kg"
