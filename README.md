# 🐱 Cat-Care Project

## 📌 Project Overview
The **Cat-Care Project** is a smart cat-care system designed to help first-time cat owners monitor and manage their pets’ feeding, hydration, and activity. The system simulates a virtual cat environment, providing data tracking, visualization, and alerts to support daily care routines.

### Main Features
- 🥣 **Food Tracker**:
	-	Record feeding time & amount
	-	Analyze daily/weekly feeding patterns
	-	Visualize trends  
- 💧 **Water Monitor**:
	-	Track water level & drinking events
	-	Low-water alert logic
	-	Generate daily intake summary  
- 🐾 **Behavior & Text Analysis**:
	-	Simple NLP processing (keywords, sentiment, tags)
	-	For notes like “My cat ate very slowly today”
- 📊 **Data Visualization**:
	-	Line charts, bar charts, daily summaries
	-	Clean and responsive Streamlit UI 
- ⚙️ **Modular Python Design**:
- Separated into reusable modules (data I/O, API utils, visualization, NLP, etc.).  

---

## 🗂 Project Structure

The project is modular, separating core logic, data, and UI components:
---
```text
cat_care_project/
│
├── modules/                     # Core functional modules
│   ├── data_loader.py           # Load CSV/JSON data
│   ├── preprocess.py            # Data cleaning & processing
│   ├── api_utils.py             # External API calls (cat camera, health info)
│   ├── visualization.py         # Plotting (Matplotlib/Plotly)
│   ├── nlp_utils.py             # NLP analysis
│   └── utils.py                 # Helper functions (formatting, error handling)
│
├── streamlit_app/               # UI layer (interactive pages)
│   ├── Home.py                  # Home page
│   ├── Health_Monitor.py        # Health monitoring
│   ├── Food_Tracker.py          # Feeding tracking
│   ├── Behavior_Analysis.py     # Behavior & NLP analysis
│   └── Config.toml              # Streamlit settings
│
├── data/                        # Sample CSV/JSON data
│   └── sample_data.csv
│
├── notebooks/                   # Colab/Jupyter test notebooks
│   └── feature_test.ipynb
│
├── main.py                      # Optional main entry
├── requirements.txt             # Dependencies
└── README.md                    # Project description
```
---
### Module Descriptions
| Module | Function |
|--------|---------|
| `data_loader.py` | Load/save CSV/JSON data, simulated user inputs |
| `preprocess.py` | Data cleaning & transformation |
| `api_utils.py` | Interfaces for external APIs (cat camera, health info) |
| `visualization.py` | Generate line/bar/pie charts |
| `nlp_utils.py` | NLP analysis on cat sounds or text notes |
| `utils.py` | Helper functions, error handling |

---

### Streamlit Pages
| Page | Function |
|------|---------|
| `Home.py` | Overview & instructions |
| `Health_Monitor.py` | Monitor cat weight, hydration & alerts |
| `Food_Tracker.py` | Feeding events, water intake, daily summary |
| `Behavior_Analysis.py` | Cat behavior & user notes NLP analysis |
| `Config.toml` | Page layout, theme color, fonts |

---

---

## 📁 Dataset / Simulation

This project simulates **7 days of cat care data**, including:  

- Water level readings (hourly)  
- Feeding events (scheduled times)  
- Cat presence detection  
- System alerts for low water  

**Simulation rules**:  

- Water level decreases gradually as the cat drinks  
- Refilled to 100% at 8 AM daily  
- Feeding times: 8 AM, 3 PM, 9 PM  
- Cat presence simulated with a 90% probability  

---

## 🧪 Example Visualizations

- **Water Level Over Time** – line chart  
- **Feeding Amounts** – bar chart  
- **Cat Presence** – pie chart  

---

## 🛠 Technologies Used

- Python: `pandas`, `numpy`, `matplotlib`, `streamlit`  
- NLP: basic text analysis for cat sounds or notes  
- Modular project structure for easy expansion  

---

## 📝 Notes

- Code is modular: `modules/` contains all logic, `streamlit_app/` handles UI  
- Data can be extended or connected to real sensors in the future  
- Visualization and logging are fully automated  

---
---

## 🚀 Usage Instructions
1. Install dependencies:
```bash
pip install -r requirements.txt

2. Launch the Streamlit app
streamlit run streamlit_app/Home.py

3. Navigate between pages
	•	Home: Overview & instructions
	•	Health Monitor: Check cat weight & hydration
	•	Food Tracker: Feed the cat, log water consumption
	•	Behavior Analysis: Analyze cat activity & user notes
4.	Data logs are stored in data/ and can be exported as CSV or JSON.

📈 Sample Visualization
	•	Line chart: Water levels over time
	•	Bar chart: Feeding amounts per day
	•	Pie chart: Cat presence during feeding
[Placeholder for charts or screenshots from Streamlit]

🔮 Future Work
	•	Integrate real-time IoT sensors for actual feeding and water monitoring
	•	Enhance NLP analysis for cat behavior recognition from audio recordings
	•	Add push notifications for alerts to mobile devices
	•	Extend to multi-pet management

⚖️ License
For educational purposes. Refer to LICENSE if using external assets or images.
