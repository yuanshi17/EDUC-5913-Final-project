# streamlit_app/pages/1_🍽️_Food_Tracker.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from modules.data_loader import load_csv, save_csv

# ============ WATER SIMULATION FUNCTIONS ============

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


# ============ MAIN PAGE FUNCTION ============

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
    """Calculate daily feeding statistics."""
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
    """Plot feeding amounts over time with cat presence indicators."""
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


def food_tracker_page():
    """Food Tracker Page with Water Level Simulation and Feeding Records"""
    st.title("🍽️ Cat Food & Water Tracker")
    
    # Create tabs for Food tracking, Feeding Simulation, and Water tracking
    tab1, tab2, tab3 = st.tabs(["🍽️ Manual Food Log", "🍖 Feeding Simulation", "💧 Water Level Simulation"])
    
    # ============ TAB 1: MANUAL FOOD LOG ============
    with tab1:
        st.subheader("📝 Manual Food Tracking")
        
        data_file = "data/feeding_log.csv"
        df = load_csv(data_file)

        if df.empty:
            st.info("No feeding data yet!")
        else:
            st.subheader("Feeding Log")
            st.dataframe(df, use_container_width=True)

        st.subheader("Add Feeding Record")
        col1, col2 = st.columns(2)
        with col1:
            new_food = st.number_input("Food amount (g)", min_value=0)
            new_water = st.number_input("Water amount (ml)", min_value=0)
        with col2:
            new_weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f")
            new_date = st.date_input("Date")

        if st.button("Add Record", type="primary"):
            new_row = {
                "date": str(new_date),
                "food_amount_g": new_food,
                "water_amount_ml": new_water,
                "weight_kg": new_weight
            }
            if df.empty:
                df = pd.DataFrame([new_row])
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_csv(df, data_file)
            st.success("✅ Record added successfully!")
            st.rerun()
    
    # ============ TAB 2: FEEDING SIMULATION ============
    with tab2:
        st.subheader("🍖 Feeding Records Simulation (7 Days)")
        st.markdown("""
        This simulation generates feeding records for 7 days with:
        - **3 meals per day** at **8 AM, 3 PM, and 9 PM**
        - Food amount: **~50g ± 5g** per meal
        - Cat presence: **90% probability**
        - Total: **21 feeding events** over 7 days
        """)
        
        # Food bowl management section
        st.subheader("🥣 Food Bowl Management")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Initialize food bowl if not exists
            if 'food_bowl_total' not in st.session_state:
                st.session_state['food_bowl_total'] = 0.0
            
            add_food_amount = st.number_input(
                "Add Food to Bowl (g)", 
                min_value=0.0, 
                step=10.0,
                help="Add food to the bowl before feeding"
            )
            
            if st.button("➕ Add Food to Bowl"):
                st.session_state['food_bowl_total'] += add_food_amount
                st.success(f"✅ Added {add_food_amount}g to bowl!")
                st.rerun()
        
        with col2:
            st.metric(
                "Current Food in Bowl", 
                f"{st.session_state['food_bowl_total']:.1f}g",
                help="Remaining food in the bowl"
            )
        
        with col3:
            if st.button("🔄 Reset Bowl", help="Clear all food from bowl"):
                st.session_state['food_bowl_total'] = 0.0
                st.success("Bowl reset to 0g")
                st.rerun()
        
        # Simulation settings
        st.subheader("⚙️ Simulation Settings")
        col1, col2 = st.columns(2)
        with col1:
            feed_start_date = st.date_input("Simulation Start Date", 
                                           value=pd.to_datetime("2024-12-13"),
                                           key="feed_start_date")
        with col2:
            st.info("📅 **Feeding Schedule**\n- 🌅 8:00 AM\n- 🌤️ 3:00 PM\n- 🌙 9:00 PM")
        
        # Generate feeding simulation button
        if st.button("🔄 Generate Feeding Simulation", type="primary"):
            with st.spinner("Generating 7-day feeding records..."):
                feeding_data = generate_feeding_records(start_date=str(feed_start_date), days=7)
                save_csv(feeding_data, "data/feeding_simulation.csv")
                st.session_state['feeding_data'] = feeding_data
                
                # Calculate total food consumed
                total_consumed = feeding_data['food_amount'].sum()
                
                # Deduct from bowl
                if st.session_state['food_bowl_total'] >= total_consumed:
                    st.session_state['food_bowl_total'] -= total_consumed
                    st.success(f"✅ Simulation complete! 21 feeding events generated (3 meals/day × 7 days).")
                    st.info(f"🍽️ Total food consumed: {total_consumed:.1f}g | Remaining in bowl: {st.session_state['food_bowl_total']:.1f}g")
                else:
                    st.warning(f"⚠️ Simulation generated but insufficient food in bowl!")
                    st.error(f"Required: {total_consumed:.1f}g | Available: {st.session_state['food_bowl_total']:.1f}g | Shortage: {total_consumed - st.session_state['food_bowl_total']:.1f}g")
                    st.session_state['food_bowl_total'] = max(0, st.session_state['food_bowl_total'] - total_consumed)
                
                st.rerun()
        
        # Load existing or generate new data
        feeding_file = "data/feeding_simulation.csv"
        if 'feeding_data' not in st.session_state:
            if os.path.exists(feeding_file):
                st.session_state['feeding_data'] = load_csv(feeding_file)
            else:
                st.session_state['feeding_data'] = generate_feeding_records(
                    start_date=str(feed_start_date), days=7)
                save_csv(st.session_state['feeding_data'], feeding_file)
        
        feeding_df = st.session_state['feeding_data']
        
        if not feeding_df.empty:
            # Convert timestamp
            feeding_df['timestamp'] = pd.to_datetime(feeding_df['timestamp'])
            
            # Current status
            st.subheader("📊 Feeding Summary")
            
            # Calculate consumption statistics
            total_consumed = feeding_df['food_amount'].sum()
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                total_meals = len(feeding_df)
                st.metric("Total Meals", total_meals)
            with col2:
                st.metric("Food Consumed", f"{total_consumed:.1f}g")
            with col3:
                st.metric("Food Remaining", f"{st.session_state['food_bowl_total']:.1f}g")
            with col4:
                present_count = feeding_df['cat_present'].sum()
                st.metric("Cat Present", f"{int(present_count)}/{total_meals}")
            with col5:
                presence_rate = (present_count / total_meals * 100) if total_meals > 0 else 0
                st.metric("Presence Rate", f"{presence_rate:.1f}%")
            
            # Food balance alert
            if st.session_state['food_bowl_total'] < 100:
                st.warning(f"⚠️ Low food alert! Only {st.session_state['food_bowl_total']:.1f}g remaining. Consider refilling.")
            elif st.session_state['food_bowl_total'] < 0:
                st.error(f"🚨 Food shortage! Bowl is {abs(st.session_state['food_bowl_total']):.1f}g in deficit.")
            
            # Feeding chart
            st.subheader("📈 Feeding Records Over Time")
            fig = plot_feeding_chart(feeding_df)
            st.pyplot(fig)
            
            # Daily statistics
            st.subheader("📅 Daily Feeding Statistics")
            daily_feeding_stats = calculate_daily_feeding_stats(feeding_df)
            st.dataframe(daily_feeding_stats, use_container_width=True)
            
            # Daily food bar chart
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.bar(daily_feeding_stats['date'].astype(str), 
                   daily_feeding_stats['total_food_g'], 
                   color='#ff7f0e', alpha=0.8)
            ax2.set_xlabel('Date', fontsize=11)
            ax2.set_ylabel('Total Food (g)', fontsize=11)
            ax2.set_title('Daily Food Consumption', fontsize=13, fontweight='bold')
            ax2.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig2)
            
            # Feeding time analysis
            st.subheader("🕐 Feeding Time Analysis")
            feeding_df['hour'] = feeding_df['timestamp'].dt.hour
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Presence by time
                time_presence = feeding_df.groupby('hour')['cat_present'].sum().reset_index()
                time_presence.columns = ['hour', 'cat_present_count']
                
                fig3, ax3 = plt.subplots(figsize=(8, 4))
                colors = ['#2ecc71' if h in [8, 15, 21] else '#95a5a6' 
                         for h in time_presence['hour']]
                ax3.bar(time_presence['hour'], time_presence['cat_present_count'], 
                       color=colors, alpha=0.8)
                ax3.set_xlabel('Hour of Day', fontsize=11)
                ax3.set_ylabel('Cat Present Count', fontsize=11)
                ax3.set_title('Cat Presence by Feeding Time', fontsize=12, fontweight='bold')
                ax3.set_xticks([8, 15, 21])
                ax3.grid(axis='y', alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig3)
            
            with col2:
                # Average food by time
                time_food = feeding_df.groupby('hour')['food_amount'].mean().reset_index()
                
                fig4, ax4 = plt.subplots(figsize=(8, 4))
                colors = ['#e74c3c' if h in [8, 15, 21] else '#95a5a6' 
                         for h in time_food['hour']]
                ax4.bar(time_food['hour'], time_food['food_amount'], 
                       color=colors, alpha=0.8)
                ax4.set_xlabel('Hour of Day', fontsize=11)
                ax4.set_ylabel('Average Food (g)', fontsize=11)
                ax4.set_title('Average Food Amount by Time', fontsize=12, fontweight='bold')
                ax4.set_xticks([8, 15, 21])
                ax4.grid(axis='y', alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig4)
            
            # Detailed feeding log
            with st.expander("📋 View All Feeding Records"):
                st.dataframe(feeding_df, use_container_width=True)
            
            # Download data
            st.subheader("💾 Export Feeding Data")
            col1, col2 = st.columns(2)
            with col1:
                csv = feeding_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Feeding Records (CSV)",
                    data=csv,
                    file_name=f"feeding_simulation_{feed_start_date}.csv",
                    mime="text/csv"
                )
            with col2:
                daily_csv = daily_feeding_stats.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Daily Stats (CSV)",
                    data=daily_csv,
                    file_name=f"daily_feeding_stats_{feed_start_date}.csv",
                    mime="text/csv"
                )
    
    # ============ TAB 3: WATER LEVEL SIMULATION ============
    with tab3:
        st.subheader("💧 Water Level Simulation (7 Days)")
        st.markdown("""
        This simulation tracks water levels over a 7-day period with:
        - **168 hourly readings** (24 hours × 7 days)
        - Water **refilled to 100%** every day at **8:00 AM**
        - Gradual decrease as the cat drinks
        - Random fluctuations for realistic behavior
        """)
        
        # Simulation settings
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Simulation Start Date", value=pd.to_datetime("2024-12-13"))
        with col2:
            alert_threshold = st.slider("Low Water Alert Threshold (%)", 10, 50, 20)
        
        # Generate simulation button
        if st.button("🔄 Generate New Water Simulation", type="primary"):
            with st.spinner("Generating 7-day water level simulation..."):
                water_data = generate_water_level_data(start_date=str(start_date), days=7)
                save_csv(water_data, "data/water_simulation.csv")
                st.session_state['water_data'] = water_data
                st.success("✅ Simulation complete! 168 hourly readings generated.")
        
        # Load existing or generate new data
        water_file = "data/water_simulation.csv"
        if 'water_data' not in st.session_state:
            if os.path.exists(water_file):
                st.session_state['water_data'] = load_csv(water_file)
            else:
                st.session_state['water_data'] = generate_water_level_data(start_date=str(start_date), days=7)
                save_csv(st.session_state['water_data'], water_file)
        
        water_df = st.session_state['water_data']
        
        if not water_df.empty:
            # Convert timestamp
            water_df['timestamp'] = pd.to_datetime(water_df['timestamp'])
            
            # Current status
            st.subheader("📊 Current Water Status")
            current_level = water_df.iloc[-1]['water_level_percent']
            alert_info = check_water_alerts(current_level, threshold=alert_threshold)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Water Level", f"{current_level:.1f}%")
            with col2:
                total_refills = water_df['refill_event'].sum()
                st.metric("Total Refills (7 days)", int(total_refills))
            with col3:
                total_drinking = water_df['cat_drinking'].sum()
                st.metric("Drinking Events", int(total_drinking))
            
            # Alert display
            if alert_info['severity'] == 'CRITICAL':
                st.error(alert_info['message'])
            elif alert_info['severity'] == 'WARNING':
                st.warning(alert_info['message'])
            else:
                st.success(alert_info['message'])
            
            # Water level chart
            st.subheader("📈 Water Level Over Time (168 Hours)")
            fig = plot_water_level_chart(water_df, alert_threshold)
            st.pyplot(fig)
            
            # Daily statistics
            st.subheader("📅 Daily Water Consumption")
            daily_stats = calculate_daily_water_consumption(water_df)
            st.dataframe(daily_stats, use_container_width=True)
            
            # Daily consumption bar chart
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.bar(daily_stats['date'].astype(str), daily_stats['total_consumed_percent'], 
                    color='#17becf', alpha=0.8)
            ax2.set_xlabel('Date', fontsize=11)
            ax2.set_ylabel('Water Consumed (%)', fontsize=11)
            ax2.set_title('Daily Water Consumption', fontsize=13, fontweight='bold')
            ax2.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig2)
            
            # Hourly drinking pattern
            st.subheader("🕐 Hourly Drinking Pattern")
            water_df['hour'] = water_df['timestamp'].dt.hour
            hourly_drinking = water_df.groupby('hour')['cat_drinking'].sum().reset_index()
            
            fig3, ax3 = plt.subplots(figsize=(10, 4))
            ax3.bar(hourly_drinking['hour'], hourly_drinking['cat_drinking'], 
                    color='#9467bd', alpha=0.7)
            ax3.set_xlabel('Hour of Day', fontsize=11)
            ax3.set_ylabel('Drinking Events', fontsize=11)
            ax3.set_title('When Does Your Cat Drink? (24-Hour Pattern)', fontsize=13, fontweight='bold')
            ax3.set_xticks(range(0, 24, 2))
            ax3.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig3)
            
            # Summary statistics
            with st.expander("📊 View Detailed Statistics"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Average Daily Consumption", 
                             f"{daily_stats['total_consumed_percent'].mean():.1f}%")
                    st.metric("Peak Consumption Day", 
                             f"{daily_stats['total_consumed_percent'].max():.1f}%")
                with col2:
                    st.metric("Minimum Water Level", 
                             f"{water_df['water_level_percent'].min():.1f}%")
                    st.metric("Average Water Level", 
                             f"{water_df['water_level_percent'].mean():.1f}%")
            
            # Download data
            st.subheader("💾 Export Data")
            col1, col2 = st.columns(2)
            with col1:
                csv = water_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Hourly Data (CSV)",
                    data=csv,
                    file_name=f"water_simulation_{start_date}.csv",
                    mime="text/csv"
                )
            with col2:
                daily_csv = daily_stats.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Daily Stats (CSV)",
                    data=daily_csv,
                    file_name=f"daily_water_stats_{start_date}.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    food_tracker_page()