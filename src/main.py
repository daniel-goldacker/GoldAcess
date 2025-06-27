import streamlit as st
from streamlit_option_menu import option_menu
from frontend.login import login
from frontend.user import users
from frontend.profile import profile
from frontend.home import home
from frontend.apidocs import api_docs
from frontend.logout import logout

# --- Inicializa sessão ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username_logged" not in st.session_state:
    st.session_state.username_logged = ""
if "menu" not in st.session_state:
    st.session_state.menu = "Home"

# --- MENU LATERAL ---
with st.sidebar:
    if st.session_state.logged_in:
        menu_items = ["Home", "Usuário", "Perfil", "API Docs", "Logout"]
        icons = ["house", "person-plus", "people", "book", "box-arrow-right"]
    else:
        menu_items = ["Home", "API Docs", "Login"]
        icons = ["house", "book", "box-arrow-in-right"]

    selected = option_menu(
        "Menu",
        menu_items,
        icons=icons,
        menu_icon="cast",
        default_index=menu_items.index(st.session_state.menu)
        if st.session_state.menu in menu_items else 0
    )

if selected != st.session_state.menu:
    st.session_state.menu = selected
    st.rerun()

# --- ROTAS ---
if st.session_state.menu == "Home":
    home()
elif st.session_state.menu == "Usuário" and st.session_state.logged_in:
    users()
elif st.session_state.menu == "Perfil" and st.session_state.logged_in:
    profile()
elif st.session_state.menu == "API Docs":
    api_docs()
elif st.session_state.menu == "Login":
    login()
elif st.session_state.menu == "Logout":
    logout()
