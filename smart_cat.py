import streamlit as st
import pandas as pd
from datetime import datetime
import random
import os
import requests
import base64

# -----------------------------
# 配置页面
# -----------------------------
st.set_page_config(layout="centered")
st.markdown("<style>footer {visibility: hidden;} </style>", unsafe_allow_html=True)  # 隐藏页脚

API_KEY = "live_4J13auPSkd8drMRuqHDOW5VRsChrgxqRkk3Lo6jqVZ4a8SnwDyCLMdElLFtjsyim"

# -----------------------------
# 获取随机猫咪图片
# -----------------------------
def get_cat_image():
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        image_url = data[0]["url"]
        img_data = requests.get(image_url).content
        encoded = base64.b64encode(img_data).decode()
        return f"data:image/jpg;base64,{encoded}"
    except:
        # fallback
        fallback = "https://placekitten.com/800/600"
        img_data = requests.get(fallback).content
        encoded = base64.b64encode(img_data).decode()
        return f"data:image/jpg;base64,{encoded}"

bg_image = get_cat_image()

# -----------------------------
# 设置背景 + 半透明遮罩 + 问候语样式
# -----------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: relative;
    }}
    .overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.4);  /* 半透明遮罩 */
        z-index: 0;
    }}
    .greeting {{
        color: white;
        font-size: 48px;
        text-align: center;
        margin-top: 20%;
        font-weight: bold;
        text-shadow: 2px 2px 6px #000000;
        z-index: 1;
        position: relative;
        background-color: rgba(0,0,0,0.3);
        padding: 10px 20px;
        border-radius: 10px;
        display: inline-block;
    }}
    .buttons {{
        display: flex;
        justify-content: center;
        margin-top: 30px;
        z-index: 1;
        position: relative;
    }}
    </style>
    <div class="overlay"></div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 问候语
# -----------------------------
hour = datetime.now().hour
if hour < 12:
    greeting = "早上好 😺"
elif hour < 18:
    greeting = "中午好 😺"
else:
    greeting = "晚上好 😺"

st.markdown(f'<div class="greeting">{greeting}</div>', unsafe_allow_html=True)

# -----------------------------
# 互动按钮
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    if st.button("喂猫"):
        st.success("猫猫吃饱啦！😻")
with col2:
    if st.button("摸猫"):
        st.info("猫猫蹭蹭你！😽")

st.title("🐱 Smart Cat App with Widgets")
st.write("Monitor your cat's food and feeding history!")

# 输入控件（Input Widgets）
initial_food = st.number_input("Set initial cat food portions:", min_value=0, max_value=100, value=10)
feed_amount = st.number_input("Set portions per feeding:", min_value=1, max_value=10, value=1)

# 初始化 Session State
if 'food_level' not in st.session_state:
    st.session_state.food_level = initial_food
if 'feed_history' not in st.session_state:
    st.session_state.feed_history = []

# 显示猫粮剩余量
st.write(f"🍽 Cat food remaining: {st.session_state.food_level} portions")

# 喂食按钮
if st.button("Feed the Cat"):
    if st.session_state.food_level >= feed_amount:
        st.session_state.food_level -= feed_amount
        st.session_state.feed_history.append(datetime.now())
        st.success(f"The cat has been fed {feed_amount} portion(s)! 😺")
    else:
        st.warning("Not enough cat food left! 🛑")

# 显示喂食记录
if st.session_state.feed_history:
    st.subheader("Feeding History")
    df = pd.DataFrame({'Time': st.session_state.feed_history})
    st.line_chart(df.set_index('Time'))

# 可视化剩余猫粮
st.subheader("Food Stock Visualization")
st.bar_chart([st.session_state.food_level])


# -----------------------------
import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt

# --------------------- 宠物模拟类 ---------------------
class PetSimulator:
    def __init__(self, name, weight_kg, food_stock_g, water_stock_ml,
                 feed_efficiency=0.85, water_efficiency=0.0005, log_file="pet_log.csv"):
        self.name = name
        self.weight_kg = weight_kg
        self.food_stock_g = food_stock_g
        self.water_stock_ml = water_stock_ml
        self.feed_efficiency = feed_efficiency
        self.water_efficiency = water_efficiency
        self.log_file = log_file
        self._init_log()

    def _init_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "event", "amount", "unit",
                                 "weight_kg", "food_stock_g", "water_stock_ml"])
        self._log("init", 0, "-")

    def _log(self, event, amount, unit):
        with open(self.log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                event, amount, unit,
                round(self.weight_kg, 3),
                round(self.food_stock_g, 1),
                round(self.water_stock_ml, 1)
            ])

    def feed(self, amount_g):
        actual_feed = min(amount_g, self.food_stock_g)
        self.food_stock_g -= actual_feed
        gained_kg = (actual_feed / 1000.0) * self.feed_efficiency
        self.weight_kg += gained_kg
        self._log("feed", actual_feed, "g")
        return actual_feed, gained_kg

    def drink(self, amount_ml):
        actual_drink = min(amount_ml, self.water_stock_ml)
        self.water_stock_ml -= actual_drink
        gained_kg = actual_drink * self.water_efficiency
        self.weight_kg += gained_kg
        self._log("drink", actual_drink, "ml")
        return actual_drink, gained_kg

    def get_status(self):
        return {
            "体重 (kg)": round(self.weight_kg, 3),
            "食物剩余 (g)": round(self.food_stock_g, 1),
            "水剩余 (ml)": round(self.water_stock_ml, 1)
        }

    def get_log(self):
        if os.path.exists(self.log_file):
            return pd.read_csv(self.log_file)
        return pd.DataFrame(columns=["timestamp","event","amount","unit",
                                     "weight_kg","food_stock_g","water_stock_ml"])

# --------------------- Streamlit 界面部分 ---------------------
st.set_page_config(page_title="🐾 虚拟宠物监测模拟器", layout="centered")

st.title("🐶 虚拟宠物食水监测模拟器")
st.markdown("实时追踪宠物体重、食物与水的消耗情况")

# 初始化宠物对象（Session 保持）
if "pet" not in st.session_state:
    st.session_state.pet = PetSimulator("小毛球", 4.2, 1000, 1500)

pet = st.session_state.pet

# ---- 状态展示 ----
st.subheader("📊 当前状态")
status = pet.get_status()
st.dataframe(pd.DataFrame([status]))

# ---- 操作输入 ----
st.subheader("🍗 喂食 / 💧 饮水 控制")

col1, col2 = st.columns(2)

with col1:
    feed_amount = st.number_input("喂食量 (g)", min_value=0.0, step=10.0, value=100.0)
    if st.button("执行喂食"):
        actual, gained = pet.feed(feed_amount)
        st.success(f"✅ 实际喂食 {actual:.1f} g，体重增加 {gained:.4f} kg")

with col2:
    drink_amount = st.number_input("饮水量 (ml)", min_value=0.0, step=10.0, value=50.0)
    if st.button("执行饮水"):
        actual, gained = pet.drink(drink_amount)
        st.success(f"✅ 实际饮水 {actual:.1f} ml，体重增加 {gained:.5f} kg")

# ---- 日志展示 ----
st.subheader("🧾 操作记录日志")
df = pet.get_log()
if len(df) > 0:
    st.dataframe(df.tail(10))
else:
    st.info("暂无记录。")

# ---- 绘制趋势图 ----
st.subheader("📈 趋势图")
if len(df) > 1:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df["timestamp"], df["weight_kg"], label="体重 (kg)", marker="o")
    ax.plot(df["timestamp"], df["food_stock_g"], label="食物剩余 (g)", marker="s")
    ax.plot(df["timestamp"], df["water_stock_ml"], label="水剩余 (ml)", marker="^")
    ax.set_xlabel("时间")
    ax.set_ylabel("数值 / 单位")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("请先进行一次喂食或饮水操作后再查看趋势图。")

