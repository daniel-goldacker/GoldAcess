import streamlit as st

def logout():
    st.markdown("<h2 style='text-align:center; color:#d9534f;'>🔒 Logout</h2>", unsafe_allow_html=True)
    st.warning("⚠️ **Você realmente deseja sair da sua conta?**")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        sair = st.button("✅ Sim, quero sair", use_container_width=True, key="btn_logout")
        if sair:
            st.session_state.logged_in = False
            st.session_state.username_logged = ""
            st.session_state.menu = "Home"
            st.rerun()
    with col2:
        cancelar = st.button("↩️ Cancelar", use_container_width=True, key="btn_cancel_logout")
        if cancelar:
            st.session_state.menu = "Home"
            st.rerun()
