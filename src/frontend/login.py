import streamlit as st 
from bussines.user import authenticate

def login():
    st.title("🔐 Login")

    login_user = st.text_input("Usuário")
    login_pass = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        user = authenticate(login_user, login_pass)
        if user:
            # Validação do nome do perfil relacionado
            st.session_state.logged_in = True
            st.session_state.user = user  # salva o objeto completo
            st.session_state.username_logged = user.username
            st.session_state.login_failed = False
            st.rerun() 
    else:
            st.session_state.login_failed = True

    if st.session_state.login_failed:
        st.error("❌ Usuário ou senha inválidos, ou seu perfil ainda não está autorizado a acessar o sistema.")

    st.stop()
