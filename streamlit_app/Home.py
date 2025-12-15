# streamlit_app/Home.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
import pandas as pd
from modules.data_loader import load_csv, save_csv


# Page configuration - must be before other Streamlit commands
st.set_page_config(
   page_title="Cat Care Tracker",
   page_icon="🐱",
   layout="wide",  # Use wide screen layout
   initial_sidebar_state="expanded",  # Expand sidebar by default
   menu_items={
       'Get Help': 'https://github.com/yuanshi17/EDUC-5913-Final-project',
       'Report a bug': "https://github.com/yuanshi17/EDUC-5913-Final-project/issues",
       'About': "# Cat Care Tracker\nTrack your cat's daily activities, health, and behavior!"
   }
)


def home_page():
   """Home Page"""
  
   # Custom CSS styles
   st.markdown("""
   <style>
   .big-title {
       font-size: 6rem;
       font-weight: 800;
       color: #FF6B6B;
       text-align: center;
       margin-bottom: 1rem;
   }
   .subtitle {
       font-size: 1.2rem;
       text-align: center;
       color: #666;
       margin-bottom: 2rem;
   }
   .metric-card {
       background-color: #F0F2F6;
       padding: 1rem;
       border-radius: 10px;
       border-left: 4px solid #FF6B6B;
   }
   .info-box {
       background-color: #E8F4F8;
       padding: 1.5rem;
       border-radius: 10px;
       border-left: 4px solid #4A90E2;
       margin: 1rem 0;
   }
   </style>
   """, unsafe_allow_html=True)
  
   # Title section
   st.markdown('<p class="big-title">🏠 Smart Cat</p>', unsafe_allow_html=True)
   st.markdown('<p class="subtitle">Track your cat\'s food, water, and activities in one place</p>',
               unsafe_allow_html=True)
  
   # Welcome guide
   with st.expander("📖 How to Use This App", expanded=False):
       col1, col2 = st.columns(2)
      
       with col1:
           st.markdown("""
           ### 🚀 Getting Started
           1. **Upload Data**: Start by uploading your cat's activity CSV file below
           2. **View Dashboard**: See your cat's activity summary and statistics
           3. **Explore Pages**: Use the sidebar to navigate to different features
           """)
      
       with col2:
           st.markdown("""
           ### 📊 Features
           - 🍽️ **Food Tracker**: Monitor daily food intake
           - 💊 **Health Monitor**: Track weight and medications
           - 📊 **Behavior Analysis**: Analyze mood patterns
           """)
      
       st.info("💡 **Tip**: Your CSV file should include columns: date, time, activity, cat_name, amount, notes")


   # Load cat data
   data_file = "data/sample_data.csv"
  
   try:
       df = load_csv(data_file)
      
       if df.empty:
           st.markdown('<div class="info-box">ℹ️ No data available yet. Start by uploading your first CSV file below!</div>',
                      unsafe_allow_html=True)
       else:
           # Data overview dashboard
           st.markdown("---")
           st.subheader("📊 Activity Dashboard")
          
           # Key metric cards
           col1, col2, col3, col4 = st.columns(4)
          
           with col1:
               total_activities = len(df)
               st.markdown('<div class="metric-card">', unsafe_allow_html=True)
               st.metric("Total Activities", total_activities,
                        help="Total number of logged activities")
               st.markdown('</div>', unsafe_allow_html=True)
          
           with col2:
               days_tracked = df['date'].nunique() if 'date' in df.columns else 0
               st.markdown('<div class="metric-card">', unsafe_allow_html=True)
               st.metric("Days Tracked", days_tracked,
                        help="Number of unique days with data")
               st.markdown('</div>', unsafe_allow_html=True)
          
           with col3:
               active_cats = df['cat_name'].nunique() if 'cat_name' in df.columns else 0
               st.markdown('<div class="metric-card">', unsafe_allow_html=True)
               st.metric("Cats Tracked", active_cats,
                        help="Number of different cats")
               st.markdown('</div>', unsafe_allow_html=True)
          
           with col4:
               latest_activity = df['activity'].iloc[-1] if 'activity' in df.columns and len(df) > 0 else "N/A"
               st.markdown('<div class="metric-card">', unsafe_allow_html=True)
               st.metric("Latest Activity", latest_activity.capitalize(),
                        help="Most recent logged activity")
               st.markdown('</div>', unsafe_allow_html=True)
          
           st.markdown("---")
          
           # Activity type distribution
           if 'activity' in df.columns:
               st.subheader("📈 Activity Distribution")
               col1, col2 = st.columns([2, 1])
              
               with col1:
                   # Activity count
                   activity_counts = df['activity'].value_counts()
                   st.bar_chart(activity_counts)
              
               with col2:
                   st.markdown("### Activity Summary")
                   for activity, count in activity_counts.items():
                       percentage = (count / len(df)) * 100
                       st.write(f"**{activity.capitalize()}**: {count} ({percentage:.1f}%)")
          
           st.markdown("---")
          
           # Display data table
           st.subheader("🐾 Recent Activity Data")
          
           # Display options
           col1, col2 = st.columns([1, 3])
           with col1:
               show_rows = st.selectbox("Rows to display", [10, 25, 50, 100], index=0)
          
           # Show recent data
           st.dataframe(
               df.tail(show_rows),
               use_container_width=True,
               hide_index=True
           )
          
           # Download button
           csv = df.to_csv(index=False)
           st.download_button(
               label="📥 Download Full Data as CSV",
               data=csv,
               file_name=f"cat_care_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
               mime="text/csv",
               help="Download all your cat's activity data"
           )
  
   except (FileNotFoundError, pd.errors.EmptyDataError):
       st.markdown('<div class="info-box">ℹ️ No data available yet. Start by uploading your first CSV file below!</div>',
                  unsafe_allow_html=True)
       df = pd.DataFrame()


   # Upload new data
   st.markdown("---")
   st.subheader("📤 Upload New Activity Data")
  
   col1, col2 = st.columns([2, 1])
  
   with col1:
       uploaded_file = st.file_uploader(
           "Choose a CSV file",
           type="csv",
           help="Upload a CSV file with columns: date, time, activity, cat_name, amount, notes"
       )
  
   with col2:
       st.markdown("### CSV Format Example")
       st.code("""date,time,activity,cat_name,amount,notes
2024-12-13,09:00,food,Whiskers,50g,Morning meal
2024-12-13,09:15,water,Whiskers,100ml,Fresh""")
  
   if uploaded_file:
       try:
           new_df = pd.read_csv(uploaded_file)
          
           # Validate required columns
           required_columns = ['date', 'time', 'activity', 'cat_name', 'amount', 'notes']
           missing_columns = [col for col in required_columns if col not in new_df.columns]
          
           if missing_columns:
               st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
           else:
               st.success(f"✅ Successfully uploaded {len(new_df)} rows!")
              
               # Display preview
               with st.expander("👀 Preview uploaded data", expanded=True):
                   st.dataframe(new_df.head(10), use_container_width=True)
              
               # Save options
               if st.button("💾 Save Data", type="primary"):
                   save_csv(new_df, data_file)
                   st.success("✅ Data saved successfully!")
                   st.balloons()
                   st.rerun()
      
       except Exception as e:
           st.error(f"❌ Error reading file: {str(e)}")
           st.info("Please make sure your CSV file is properly formatted.")


if __name__ == "__main__":
   home_page()