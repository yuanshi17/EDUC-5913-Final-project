# modules/data_loader.py
import pandas as pd
import json
import os

def load_csv(file_path):
    """Load CSV data into a DataFrame"""
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"File {file_path} not found.")
        return pd.DataFrame()

def save_csv(df, file_path):
    """Save DataFrame to CSV"""
    df.to_csv(file_path, index=False)

def load_json(file_path):
    """Load JSON data"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(data, file_path):
    """Save data to JSON"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
