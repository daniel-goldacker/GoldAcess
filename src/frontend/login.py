import streamlit as st
from bussines.user import authenticate
from bussines.profile import get_profiles
from frontend.register import register

def login():
    if "login_failed" not in st.session_state:
        st.session_state.login_failed = False

    st.markdown("<h2 style='text-align: center;'>🔐 Bem-vindo ao GoldCo</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Faça login para continuar</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_user = st.text_input("👤 Usuário", placeholder="Digite seu nome de usuário", key="login_user")
        login_pass = st.text_input("🔑 Senha", type="password", placeholder="Digite sua senha", key="login_pass")

        login_button_disabled = not login_user or not login_pass
        col_login, col_create = st.columns(2)

        if col_login.button("🚪 Entrar", disabled=login_button_disabled):
            user = authenticate(login_user, login_pass)
            if user:
                profile = get_profiles(user.profile_id)
                if profile.is_admin:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.username_logged = user.username
                    st.session_state.profile_logger = profile.name
                    st.session_state.login_failed = False
                    st.rerun()
                else:
                    st.session_state.login_failed = True
            else:
                st.session_state.login_failed = True

        if col_create.button("📝 Criar Conta"):
            register()

        if st.session_state.login_failed:
            st.error("❌ Usuário ou senha inválidos, ou seu perfil não está autorizado a acessar o sistema.")
