import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Domain Expert", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("⛔ You must be logged in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("🤖 Multi-Domain AI Assistant")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("🚨 API Key missing!")
    st.stop()

system_prompts = {
    "Cybersecurity Expert": """You are a cybersecurity expert assistant. 
    Analyze incidents, threats, and provide technical guidance.
    Focus on mitigation strategies, risk assessment, and MITRE ATT&CK frameworks.""",
    
    "Data Science Expert": """You are a data science expert assistant. 
    Help with analysis, visualization, and statistical insights.
    Provide Python code snippets (pandas, plotly) for analyzing the dashboard data.""",
    
    "IT Operations Expert": """You are an IT operations expert assistant. 
    Help troubleshoot issues, optimize systems, and manage tickets.
    Focus on practical solutions for system downtime and maintenance."""
}


st.markdown("### 🧠 Select Your Intelligence Assistant")

col1, col2 = st.columns([3, 1])

with col1:
    selected_domain = st.selectbox("Choose Expert Role:", list(system_prompts.keys()))

with col2:
    st.write("")
    st.write("")
    if st.button("🗑️ Clear Chat", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.divider()

if "current_domain" not in st.session_state:
    st.session_state.current_domain = selected_domain

if st.session_state.current_domain != selected_domain:
    st.session_state.messages = []
    st.session_state.current_domain = selected_domain

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages or st.session_state.messages[0]["role"] != "system":
    st.session_state.messages.insert(0, {"role": "system", "content": system_prompts[selected_domain]})
elif st.session_state.messages[0]["content"] != system_prompts[selected_domain]:
    st.session_state.messages[0] = {"role": "system", "content": system_prompts[selected_domain]}

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input(f"Ask the {selected_domain}..."):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = "" 

        try:
            stream = client.chat.completions.create(
                model = "gpt-4o",
                messages = st.session_state.messages,
                stream = True 
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        except Exception as e:
            st.error(f"An error occurred: {e}")