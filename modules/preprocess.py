# modules/preprocess.py
import pandas as pd

def clean_water_data(df):
    """Example: Fill missing water levels or remove invalid entries"""
    df = df.copy()
    df['water_level_percent'] = df['water_level_percent'].fillna(0)
    return df

def clean_feeding_data(df):
    """Example: Ensure food amount is non-negative"""
    df = df.copy()
    df['food_amount_g'] = df['food_amount_g'].apply(lambda x: max(0, x))
    return df
