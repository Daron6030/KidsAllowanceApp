import streamlit as st
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Копилка Доченьки", page_icon="💖", layout="centered")

# Стили и фон
st.markdown("""
<style>
    .big-balance {
        font-size: 58px !important;
        font-weight: bold;
        color: #1a1a1a;
        text-align: center;
    }
    .stButton>button {
        height: 85px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 20px;
    }
    .plus-button {
        background: linear-gradient(135deg, #8A2BE2, #BA55D3);
        color: white;
        font-size: 42px !important;
        height: 110px !important;
        border-radius: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Данные
DATA_FILE = "balance_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"balance": 1000, "last_reset": datetime.now().strftime("%Y-%m-%d")}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# Проверка еженедельного начисления (каждую субботу)
today = datetime.now()
last_reset = datetime.strptime(data["last_reset"], "%Y-%m-%d")

if today.weekday() == 5 and (today - last_reset).days >= 6:  # Суббота
    data["balance"] += 1000
    data["last_reset"] = today.strftime("%Y-%m-%d")
    save_data(data)

# ==================== ИНТЕРФЕЙС ====================

st.title("💖 Копилка Доченьки 💖")

# Верхняя часть — +100
st.markdown("### Зачислить +100 ₽")
col1, col2 = st.columns(2)

with col1:
    mom = st.checkbox("Мама согласна ✅", key="mom")
with col2:
    dad = st.checkbox("Папа согласен ✅", key="dad")

if mom and dad:
    if st.button("➕ Зачислить +100 ₽", type="primary", use_container_width=True):
        data["balance"] += 100
        save_data(data)
        st.success("✅ +100 ₽ успешно зачислено!")
        st.rerun()
else:
    st.button("➕ Зачислить +100 ₽", type="primary", disabled=True, use_container_width=True)

# Центральный баланс
st.markdown("### Твой баланс")
st.markdown(f"<div class='big-balance'>{data['balance']} ₽</div>", unsafe_allow_html=True)

st.markdown("---")

# Нижние кнопки
col_green, col_red = st.columns(2)

with col_green:
    if st.button("🌟 -50 ₽\n\nЯ сама отдала", 
                key="green", 
                use_container_width=True):
        if data["balance"] >= 50:
            data["balance"] -= 50
            save_data(data)
            st.rerun()
        else:
            st.error("Недостаточно денег")

with col_red:
    if st.button("🚫 -100 ₽\n\nНаказание", 
                key="red", 
                use_container_width=True):
        if data["balance"] >= 100:
            data["balance"] -= 100
            save_data(data)
            st.rerun()
        else:
            st.error("Недостаточно денег")

# Декоративные элементы
st.markdown("""
    <div style="text-align:center; margin-top:30px;">
        <h3>Ты молодец! 🌈 Продолжай копить 💰</h3>
    </div>
""", unsafe_allow_html=True)

# Запуск: streamlit run app.py