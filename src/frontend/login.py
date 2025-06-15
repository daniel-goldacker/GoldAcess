
import streamlit as st 
from auth import authenticate

def login():
    st.title("🔐 Login")

    login_user = st.text_input("Usuário")
    login_pass = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if authenticate(login_user, login_pass):
            st.session_state.logged_in = True
            st.session_state.username_logged = login_user
            st.session_state.login_failed = False
            st.rerun()
        else:
            st.session_state.login_failed = True

    if st.session_state.login_failed:
        st.error("❌ Usuário ou senha inválidos.")

    st.stop()