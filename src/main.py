import streamlit as st
from streamlit_option_menu import option_menu
from frontend.login import login
from frontend.user import users
from frontend.profile import profile
from frontend.home import home
from frontend.apidocs import api_docs

# --- Inicializa sessão ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False
if "username_logged" not in st.session_state:
    st.session_state.username_logged = ""

# --- MENU LATERAL ---
with st.sidebar:
    if st.session_state.logged_in:
        st.markdown(f"👤 Bem-vindo, **{st.session_state.username_logged}** !")
        menu_items_logged = ["Home", "Usuário", "Perfil", "API Docs", "Logout"]
        icons_logged = ["house", "person-plus", "people", "book", "box-arrow-right"]

        menu = option_menu(
            "Menu",
            menu_items_logged,
            icons=icons_logged,
            menu_icon="cast",
            default_index=0
        )
    else:
        menu_items_unlogged = ["Home", "API Docs", "Login"]
        icons_unlogged = ["house", "book", "box-arrow-in-right"]

        menu = option_menu(
            "Menu",
            menu_items_unlogged,
            icons=icons_unlogged,
            menu_icon="cast",
            default_index=0
        )

# --- ROTAS ---
if menu == "Home":
    home()
elif menu == "Usuário" and st.session_state.logged_in:
    users()
elif menu == "Perfil" and st.session_state.logged_in:
    profile()
elif menu == "API Docs":
    api_docs()
elif menu == "Login":
    login()
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username_logged = ""
    st.success("Logout realizado com sucesso.")
    st.rerun()
