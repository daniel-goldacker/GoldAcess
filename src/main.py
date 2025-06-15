import streamlit as st
from streamlit_option_menu import option_menu
from frontend.create_new_user import create_new_user
from frontend.list_users import list_users
from frontend.login import login

st.set_page_config(page_title="Gerenciador de Identidade", layout="centered")

# --- Sessão de login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False

if not st.session_state.logged_in:
   login()

# --- Título ---
st.title("🔐 Gerenciador de Identidade")

# --- Menu lateral ---
with st.sidebar:
    st.markdown(f"👤 Usuário logado: **{st.session_state.username_logged}**")
    
    menu = option_menu(
        "Menu",
        ["Criar usuário", "Listar usuários", "Logout"],
        icons=["person-plus", "people", "box-arrow-right"],
        menu_icon="cast",
        default_index=0
    )

if menu == "Criar usuário":
  create_new_user()
elif menu == "Listar usuários":
   list_users(st.session_state.username_logged)
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username_logged = ""
    st.rerun()