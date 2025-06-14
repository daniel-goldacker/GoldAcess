import streamlit as st
from auth import create_user

def create_new_user():
    defaults = {
        "username": "", 
        "password": "",
        "exp_minutes": 60,
        "profile": "APIs",
        "clear_fields": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.get("clear_fields", True):
        st.session_state.username = ""
        st.session_state.password = ""
        st.session_state.exp_minutes = 60
        st.session_state.profile = "APIs"
        st.session_state.clear_fields = False
    
    st.subheader("👤 Criar novo usuário")

    username = st.text_input("Usuário", key="username")
    password = st.text_input("Senha", type="password", key="password")

    exp_minutes = st.number_input(
        "Minutos até expiração do token",
        min_value=1,
        key="exp_minutes"
    )

    profile = st.selectbox(
        "Perfil do usuário",
        options=["Administrador", "APIs"],
        key="profile"
    )

    if st.button("Criar"):
        if not username or not password:
            st.warning("Usuário e senha são obrigatórios.")
        else:
            try:
                create_user(username, password, exp_minutes, profile)  # passe profile aqui
                st.session_state.clear_fields = True
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao criar usuário: {e}")