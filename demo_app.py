import streamlit as st
from cryptography.fernet import Fernet

# إعداد مفتاح التشفير
if 'key' not in st.session_state:
    st.session_state.key = Fernet.generate_key()
cipher = Fernet(st.session_state.key)

st.title("🛡️ Sovereign Manager (Demo)")
st.write("إثبات حماية البيانات للشركات السويدية")

user_input = st.text_input("أدخل بيانات حساسة (مثلاً: Hani - 0700000000):")

if st.button("تفعيل التشفير السيادي"):
    encrypted = cipher.encrypt(user_input.encode()).decode()
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**داخل السويد:**\n\n{user_input}")
    with col2:
        st.error(f"**خارج السويد (OpenAI):**\n\n{encrypted[:40]}...")
