# modules/visualization.py
import matplotlib.pyplot as plt

def plot_water_level(df):
    plt.figure(figsize=(10, 4))
    plt.plot(df['time'], df['water_level_percent'], marker='o')
    plt.title("Water Level Over Time")
    plt.xlabel("Time")
    plt.ylabel("Water Level (%)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_feeding_amount(df):
    plt.figure(figsize=(10, 4))
    plt.bar(df['time'], df['food_amount_g'])
    plt.title("Feeding Amount Over Time")
    plt.xlabel("Time")
    plt.ylabel("Food Amount (g)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
