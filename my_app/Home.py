import streamlit as st
from auth import login_user, register_user

st.set_page_config(page_title = "Intelligence Platform", layout = "wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None

st.title("Intelligence Platform Login")

col1, col2 = st.columns([1, 2])

with col1:
    st.info("Authorized Personnel Only")
    st.markdown("Please sign in to access the secure dashboard.")

with col2:
    tab1, tab2 = st.tabs(["🔓 Log In", "📝 Sign Up"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In", type="primary")

            if submit:
                user = login_user(username, password)

                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user[1]
                    st.session_state.role = user[3]

                    st.success("Login successful!")
                    st.switch_page("pages/1_Dashboard.py")
                else:
                    st.error("Invalid credentials")

    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("Choose Username")
            new_pass = st.text_input("Choose Password (min 8 chars)", type = "password")
            confirm_pass = st.text_input("Confirm Password", type = "password")
            submit_reg = st.form_submit_button("Create Account")

            if submit_reg:
                if new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                elif len(new_pass) < 8:
                    st.error("Password must have atleast 8 characters.")
                else:
                    if register_user(new_user, new_pass):
                        st.success("✅ Account created! Please switch to the 'Log In' tab.")
                    else:
                        st.error("Username already taken.")
                        