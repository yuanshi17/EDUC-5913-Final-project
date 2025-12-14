import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def plot_line_chart(df, x, y, title="Line Chart"):
    fig, ax = plt.subplots(figsize=(10,4))
    for col in y:
        ax.plot(df[x], df[col], marker="o", label=col)
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel("Amount")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    return fig

def plot_bar_chart(df, x, y, title="Bar Chart"):
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(df[x], df[y])
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.xticks(rotation=45)
    return fig


# ============ NEW: WATER LEVEL SIMULATION FUNCTIONS ============

def generate_water_level_data(start_date="2024-12-13", days=7):
    """
    Generate 7-day water level simulation data with hourly readings.
    
    Parameters:
    - start_date: Starting date for simulation (default: "2024-12-13")
    - days: Number of days to simulate (default: 7)
    
    Returns:
    - DataFrame with columns: timestamp, water_level_percent, refill_event, cat_drinking
    """
    
    # Generate hourly timestamps for 7 days (168 hours)
    start = pd.to_datetime(start_date)
    timestamps = [start + timedelta(hours=i) for i in range(days * 24)]
    
    # Initialize water level data
    water_levels = []
    current_level = 100.0  # Start with full water bowl
    
    for ts in timestamps:
        hour = ts.hour
        
        # Refill to 100% at 8:00 AM every day
        if hour == 8:
            current_level = 100.0
            refill_event = True
        else:
            refill_event = False
        
        # Simulate cat drinking behavior
        # Higher probability during active hours (6-10 AM, 5-9 PM)
        if (6 <= hour <= 10) or (17 <= hour <= 21):
            drinking_probability = 0.7
            base_consumption = np.random.uniform(2, 5)  # 2-5% per hour
        else:
            drinking_probability = 0.3
            base_consumption = np.random.uniform(0.5, 2)  # 0.5-2% per hour
        
        # Determine if cat drinks this hour
        cat_drinking = np.random.random() < drinking_probability
        
        if cat_drinking and current_level > 0:
            # Add random fluctuation for realism
            fluctuation = np.random.uniform(-0.5, 0.5)
            consumption = base_consumption + fluctuation
            current_level = max(0, current_level - consumption)
        
        # Natural evaporation (very small amount)
        evaporation = np.random.uniform(0.1, 0.3)
        current_level = max(0, current_level - evaporation)
        
        water_levels.append({
            'timestamp': ts,
            'water_level_percent': round(current_level, 2),
            'refill_event': refill_event,
            'cat_drinking': cat_drinking
        })
    
    return pd.DataFrame(water_levels)


def check_water_alerts(water_level_percent, threshold=20):
    """
    Check if water level is below threshold and return alert status.
    
    Parameters:
    - water_level_percent: Current water level percentage
    - threshold: Alert threshold (default: 20%)
    
    Returns:
    - Dictionary with alert status and message
    """
    
    if water_level_percent <= 0:
        return {
            'alert': True,
            'severity': 'CRITICAL',
            'message': '🚨 CRITICAL: Water bowl is empty! Refill immediately!'
        }
    elif water_level_percent <= threshold:
        return {
            'alert': True,
            'severity': 'WARNING',
            'message': f'⚠️ WARNING: Water level is low ({water_level_percent:.1f}%). Please refill soon.'
        }
    else:
        return {
            'alert': False,
            'severity': 'NORMAL',
            'message': f'✅ Water level is adequate ({water_level_percent:.1f}%).'
        }


def calculate_daily_water_consumption(df):
    """
    Calculate daily water consumption statistics from simulation data.
    
    Parameters:
    - df: DataFrame with water level data (must have 'timestamp' and 'water_level_percent')
    
    Returns:
    - DataFrame with daily statistics
    """
    
    df = df.copy()
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    
    daily_stats = []
    
    for date in df['date'].unique():
        day_data = df[df['date'] == date]
        
        # Calculate consumption
        refill_rows = day_data[day_data['refill_event'] == True]
        num_refills = len(refill_rows)
        
        start_level = day_data.iloc[0]['water_level_percent']
        end_level = day_data.iloc[-1]['water_level_percent']
        total_consumed = (100 * num_refills) + (start_level - end_level)
        
        daily_stats.append({
            'date': date,
            'total_consumed_percent': round(total_consumed, 2),
            'avg_level_percent': round(day_data['water_level_percent'].mean(), 2),
            'min_level_percent': round(day_data['water_level_percent'].min(), 2),
            'num_refills': num_refills,
            'drinking_events': int(day_data['cat_drinking'].sum())
        })
    
    return pd.DataFrame(daily_stats)


def plot_water_level_chart(df, alert_threshold=20):
    """
    Plot water level over time with refill markers and alert threshold.
    
    Parameters:
    - df: DataFrame with water level data
    - alert_threshold: Alert threshold percentage
    
    Returns:
    - matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plot water level
    ax.plot(df['timestamp'], df['water_level_percent'], 
            linewidth=2, color='#1f77b4', label='Water Level')
    
    # Mark refill events
    refill_points = df[df['refill_event'] == True]
    if not refill_points.empty:
        ax.scatter(refill_points['timestamp'], refill_points['water_level_percent'],
                  color='green', s=100, marker='^', label='Refill', zorder=5)
    
    # Add alert threshold line
    ax.axhline(y=alert_threshold, color='red', linestyle='--', 
               linewidth=1.5, label=f'Alert Threshold ({alert_threshold}%)')
    
    # Styling
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Water Level (%)', fontsize=12)
    ax.set_title('Water Level Monitoring (7 Days)', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 105)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


# ============ NEW: FEEDING RECORDS SIMULATION FUNCTIONS ============

def generate_feeding_records(start_date="2024-12-13", days=7):
    """
    Generate 7-day feeding records with 3 meals per day.
    
    Parameters:
    - start_date: Starting date for simulation (default: "2024-12-13")
    - days: Number of days to simulate (default: 7)
    
    Returns:
    - DataFrame with columns: timestamp, food_amount, cat_present, event_type
    """
    
    feeding_times = [8, 15, 21]  # 8 AM, 3 PM, 9 PM
    start = pd.to_datetime(start_date)
    
    feeding_records = []
    
    for day in range(days):
        current_date = start + timedelta(days=day)
        
        for hour in feeding_times:
            timestamp = current_date.replace(hour=hour, minute=0, second=0)
            
            # Food amount: approximately 50g ± 5g
            food_amount = round(50 + np.random.uniform(-5, 5), 1)
            
            # Cat present: 90% probability
            cat_present = np.random.random() < 0.9
            
            feeding_records.append({
                'timestamp': timestamp,
                'food_amount': food_amount,
                'cat_present': cat_present,
                'event_type': 'Feeding'
            })
    
    return pd.DataFrame(feeding_records)


def calculate_daily_feeding_stats(df):
    """
    Calculate daily feeding statistics.
    
    Parameters:
    - df: DataFrame with feeding records
    
    Returns:
    - DataFrame with daily statistics
    """
    
    df = df.copy()
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    
    daily_stats = []
    
    for date in df['date'].unique():
        day_data = df[df['date'] == date]
        
        total_food = day_data['food_amount'].sum()
        total_feedings = len(day_data)
        cat_present_count = day_data['cat_present'].sum()
        presence_rate = (cat_present_count / total_feedings * 100) if total_feedings > 0 else 0
        
        daily_stats.append({
            'date': date,
            'total_food_g': round(total_food, 1),
            'num_feedings': total_feedings,
            'cat_present_count': int(cat_present_count),
            'presence_rate_percent': round(presence_rate, 1),
            'avg_food_per_meal_g': round(total_food / total_feedings, 1) if total_feedings > 0 else 0
        })
    
    return pd.DataFrame(daily_stats)


def plot_feeding_chart(df):
    """
    Plot feeding amounts over time with cat presence indicators.
    
    Parameters:
    - df: DataFrame with feeding records
    
    Returns:
    - matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Separate data by cat presence
    present = df[df['cat_present'] == True]
    absent = df[df['cat_present'] == False]
    
    # Plot feeding amounts
    if not present.empty:
        ax.scatter(present['timestamp'], present['food_amount'], 
                  color='green', s=100, marker='o', label='Cat Present', alpha=0.7)
    
    if not absent.empty:
        ax.scatter(absent['timestamp'], absent['food_amount'], 
                  color='red', s=100, marker='x', label='Cat Absent', alpha=0.7)
    
    # Add average line
    avg_food = df['food_amount'].mean()
    ax.axhline(y=avg_food, color='blue', linestyle='--', 
               linewidth=1.5, label=f'Average ({avg_food:.1f}g)', alpha=0.5)
    
    # Styling
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Food Amount (g)', fontsize=12)
    ax.set_title('Feeding Records (7 Days - 3 Meals/Day)', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(40, 60)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig