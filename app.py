import os
import streamlit as st
import pandas as pd
import random
import joblib

# ปิด usage stats
os.environ["STREAMLIT_BROWSER_GATHERUSAGESTATS"] = "false"

MODEL_PATH = "chatbot_model.pkl"
DATASET_PATH = "qa_dataset.xlsx"

# โหลดโมเดล/ชุดคำตอบ
try:
    model = joblib.load(MODEL_PATH)
    df = pd.read_excel(DATASET_PATH)
    intent_to_response = df.groupby("intent")["response"].apply(list).to_dict()
    is_ready = True
except FileNotFoundError:
    st.error("ไม่พบไฟล์ 'chatbot_model.pkl' หรือ 'qa_dataset.xlsx' โปรดตรวจสอบว่าคุณได้รันโค้ดส่วนก่อนหน้าแล้ว")
    is_ready = False

st.set_page_config(page_title="WRC Toyota Gazoo Racing 2025 Chatbot", page_icon="🏁")
st.title("WRC Toyota Gazoo Racing 2025 Chatbot")
st.caption("สอบถามข้อมูลเกี่ยวกับทีม WRC Toyota Gazoo Racing ฤดูกาล 2025 ได้ที่นี่")

# session state
if "history" not in st.session_state:
    st.session_state.history = []

# input
user_input = st.text_input("คุณ: ", "", placeholder="ถามเกี่ยวกับทีม WRC Toyota Gazoo Racing 2025...")

col1, col2 = st.columns([1,1])
with col1:
    send = st.button("ส่ง", type="primary", disabled=not is_ready)
with col2:
    clear = st.button("ล้างประวัติ")

if clear:
    st.session_state.history = []

if send and user_input.strip() and is_ready:
    predicted_intent = model.predict([user_input])[0]
    fallback = "ขอโทษครับ/ค่ะ บอทนี้ตอบเฉพาะเรื่องที่เกี่ยวข้องกับทีม WRC Toyota Gazoo Racing 2025 เท่านั้น"
    bot_reply = random.choice(
        intent_to_response.get(predicted_intent, [fallback])
    )
    st.session_state.history.append({"user": user_input, "bot": bot_reply})

# history
for chat in st.session_state.history:
    st.markdown(f"**คุณ:** {chat['user']}")
    st.markdown(f"**🤖 บอท:** {chat['bot']}")
