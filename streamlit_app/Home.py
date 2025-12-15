# streamlit_app/Home.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
import pandas as pd
from datetime import datetime
from modules.data_loader import load_csv, save_csv

<<<<<<< HEAD

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
=======
# Page configuration - must be before other Streamlit commands
st.set_page_config(
    page_title="Cat Care Tracker",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yuanshi17/EDUC-5913-Final-project',
        'Report a bug': "https://github.com/yuanshi17/EDUC-5913-Final-project/issues",
        'About': "# Cat Care Tracker\nTrack your cat's daily activities, health, and behavior!"
    }
>>>>>>> e8d824e (Improve UX: Add sample data, manual entry, better instructions)
)


def home_page():
<<<<<<< HEAD
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

=======
    """Home Page"""
    
    # Custom CSS styles
    st.markdown("""
    <style>
    .big-title {
        font-size: 5rem;
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
    with st.expander("❓ First time here? Click for quick start guide", expanded=False):
        st.markdown("""
        ## 🚀 Quick Start (3 Easy Steps)
        
        1. **👇 Scroll down** to "Get Started with Your Cat's Data"
        2. **🎯 Click "Load Sample Data"** to see how it works
        3. **🎉 Explore** the dashboard and other pages in the sidebar!
        
        ---
        
        ### 📱 What Can You Do?
        
        - **🍽️ Food & Water Tracker**: Log meals and water intake
        - **💊 Health Monitor**: Track weight, medications, vet visits
        - **📊 Behavior Analysis**: Understand your cat's mood patterns
        
        ### 💡 Pro Tips
        
        - Start with sample data to explore features
        - Use manual entry for quick daily logging
        - Upload a file if you have existing records
        - Check the dashboard daily to spot trends!
        """)

    # Load cat data
    data_file = "data/sample_data.csv"
    
    try:
        df = load_csv(data_file)
        
        if df.empty:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 3rem;
                border-radius: 15px;
                text-align: center;
                color: white;
                margin: 2rem 0;
            ">
                <h2 style="margin: 0; font-size: 2rem;">👋 Welcome to Cat Care Tracker!</h2>
                <p style="font-size: 1.2rem; margin: 1rem 0;">Let's start tracking your cat's activities</p>
                <p style="font-size: 1rem; opacity: 0.9;">
                    👇 Scroll down and click <strong>"Load Sample Data"</strong> to see how it works<br>
                    or add your own cat's first activity!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Activity dashboard
            st.markdown("---")
            st.subheader("📊 Activity Dashboard")
            
            # Key metrics
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
            
            # Activity distribution
            if 'activity' in df.columns:
                st.subheader("📈 Activity Distribution")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Activity counts
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
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin: 2rem 0;
        ">
            <h2 style="margin: 0; font-size: 2rem;">👋 Welcome to Cat Care Tracker!</h2>
            <p style="font-size: 1.2rem; margin: 1rem 0;">Let's start tracking your cat's activities</p>
            <p style="font-size: 1rem; opacity: 0.9;">
                👇 Scroll down and click <strong>"Load Sample Data"</strong> to see how it works<br>
                or add your own cat's first activity!
            </p>
        </div>
        """, unsafe_allow_html=True)
        df = pd.DataFrame()

    # Data input options
    st.markdown("---")
    st.subheader("📥 Get Started with Your Cat's Data")

    # Three tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Load Sample Data", "📤 Upload File", "✍️ Manual Entry"])

    # Tab 1: Sample data
    with tab1:
        st.markdown("""
        ### 👋 New here? Try our sample data!
        
        Click the button below to load example cat activity data and explore the app's features.
        """)
        
        if st.button("🎉 Load Sample Cat Data", type="primary", use_container_width=True):
            # Create sample data
            sample_data = pd.DataFrame({
                'date': ['2024-12-13', '2024-12-13', '2024-12-13', '2024-12-14', '2024-12-14'],
                'time': ['09:00', '09:15', '14:30', '08:30', '09:00'],
                'activity': ['food', 'water', 'play', 'food', 'water'],
                'cat_name': ['Whiskers', 'Whiskers', 'Whiskers', 'Whiskers', 'Whiskers'],
                'amount': ['50g', '100ml', '15min', '50g', '80ml'],
                'notes': ['Morning meal', 'Fresh water', 'Toy mouse', 'Morning meal', 'Fresh water']
            })
            save_csv(sample_data, data_file)
            st.success("✅ Sample data loaded! Scroll up to see the dashboard.")
            st.balloons()
            st.rerun()
        
        st.info("💡 **Tip**: Sample data helps you understand how the app works before adding your own cat's information.")

    # Tab 2: File upload
    with tab2:
        st.markdown("""
        ### 📄 Already have data? Upload it here
        
        If you've been tracking your cat's activities in a spreadsheet (like Excel), you can upload it here.
        """)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose your file", 
                type="csv",
                help="We support CSV files (spreadsheet format)"
            )
            
            st.markdown("""
            **Don't have a file yet?** Download our template:
            """)
            
            # Create template
            template_data = """date,time,activity,cat_name,amount,notes
2024-12-13,09:00,food,YourCatName,50g,Breakfast
2024-12-13,12:00,water,YourCatName,100ml,Midday drink
2024-12-13,18:00,play,YourCatName,20min,Evening playtime"""
            
            st.download_button(
                label="📥 Download Template",
                data=template_data,
                file_name="cat_activity_template.csv",
                mime="text/csv",
                help="Download this template, fill it with your cat's data, and upload it back!"
            )
        
        with col2:
            st.markdown("### 📋 File Format")
            st.code("""date,time,activity,cat_name,amount,notes
2024-12-13,09:00,food,Whiskers,50g,Morning
2024-12-13,09:15,water,Whiskers,100ml,Fresh""", language="csv")
            
            st.caption("Your file should have these columns: date, time, activity, cat_name, amount, notes")
        
        if uploaded_file:
            try:
                new_df = pd.read_csv(uploaded_file)
                
                # Validate required columns
                required_columns = ['date', 'time', 'activity', 'cat_name', 'amount', 'notes']
                missing_columns = [col for col in required_columns if col not in new_df.columns]
                
                if missing_columns:
                    st.error(f"❌ Oops! Your file is missing: {', '.join(missing_columns)}")
                    st.info("💡 Try downloading our template above and use it as a guide.")
                else:
                    st.success(f"✅ Great! Found {len(new_df)} activities for your cat!")
                    
                    # Show preview
                    with st.expander("👀 Preview your data", expanded=True):
                        st.dataframe(new_df.head(10), use_container_width=True)
                    
                    # Save option
                    if st.button("💾 Save This Data", type="primary"):
                        save_csv(new_df, data_file)
                        st.success("✅ Data saved! Check out the dashboard above!")
                        st.balloons()
                        st.rerun()
            
            except Exception as e:
                st.error(f"❌ Couldn't read your file: {str(e)}")
                st.info("💡 Make sure your file is a CSV (comma-separated values) format. You can save Excel files as CSV!")

    # Tab 3: Manual entry
    with tab3:
        st.markdown("""
        ### ✍️ Add activity one at a time
        
        Prefer to log activities as they happen? Use this quick entry form!
        """)
        
        with st.form("manual_entry", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                entry_date = st.date_input("📅 Date", help="When did this happen?")
                entry_time = st.time_input("🕐 Time", help="What time?")
            
            with col2:
                entry_cat = st.text_input("🐱 Cat Name", placeholder="e.g., Whiskers", help="Your cat's name")
                entry_activity = st.selectbox(
                    "🎯 Activity Type",
                    ["food", "water", "play", "sleep", "grooming", "litter", "medication", "other"],
                    help="What activity are you logging?"
                )
            
            with col3:
                entry_amount = st.text_input("📊 Amount", placeholder="e.g., 50g, 100ml, 15min", help="How much?")
                entry_notes = st.text_input("📝 Notes", placeholder="Any details to remember?", help="Optional notes")
            
            submitted = st.form_submit_button("➕ Add Activity", type="primary", use_container_width=True)
            
            if submitted:
                if not entry_cat:
                    st.error("❌ Please enter your cat's name!")
                else:
                    new_entry = pd.DataFrame([{
                        'date': str(entry_date),
                        'time': str(entry_time),
                        'activity': entry_activity,
                        'cat_name': entry_cat,
                        'amount': entry_amount,
                        'notes': entry_notes
                    }])
                    
                    try:
                        existing_df = load_csv(data_file)
                        if existing_df.empty:
                            combined_df = new_entry
                        else:
                            combined_df = pd.concat([existing_df, new_entry], ignore_index=True)
                        
                        save_csv(combined_df, data_file)
                        st.success(f"✅ Added {entry_activity} activity for {entry_cat}!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Couldn't save: {str(e)}")
        
        st.info("💡 **Tip**: You can add multiple activities one by one. The dashboard above updates automatically!")
>>>>>>> e8d824e (Improve UX: Add sample data, manual entry, better instructions)

if __name__ == "__main__":
   home_page()