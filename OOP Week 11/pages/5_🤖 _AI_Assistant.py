import streamlit as st
from services.ai_assistant import AIAssistant

st.set_page_config(page_title="AI Assistant", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

with st.sidebar:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.switch_page("Home.py")

st.title("🤖 Multi-Domain AI Assistant")

if "ai_assistant" not in st.session_state:
    st.session_state.ai_assistant = AIAssistant()

ai = st.session_state.ai_assistant

st.subheader("🧠 Select Your Intelligence Assistant")

col1, col2 = st.columns([3, 1])

with col1:
    domain = st.selectbox("Choose Expert Role:", 
                         ["Cybersecurity Expert", "Data Science Expert", "IT Operations Expert"])

with col2:
    if st.button("🗑️ Clear Chat", type="primary", use_container_width=True):
        ai.clear_history()
        st.rerun()

st.divider()

for msg in ai.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input(f"Ask the {domain}..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        response = ai.send_message(prompt)
        st.write(response)