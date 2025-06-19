import streamlit as st
from streamlit_option_menu import option_menu
from frontend.login import login
from frontend.user import users
from frontend.profile import profile
from frontend.home import home
from frontend.profile import profile

# --- Sessão de login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False

if not st.session_state.logged_in:
   login()

# --- Menu lateral ---
with st.sidebar:
    st.markdown(f"👤 Usuário logado: **{st.session_state.username_logged}**")
    
    menu = option_menu(
        "Menu",
        ["Home", "Criar usuário", "Perfil", "Logout"],
        icons=["house", "person-plus", "people", "box-arrow-right"],
        menu_icon="cast",
        default_index=0
    )

if menu == "Home":
    home()
elif menu == "Criar usuário":
  users()
elif menu == "Perfil":
   profile()
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username_logged = ""
    st.rerun()