import streamlit as st
from sqlalchemy.orm import Session
from bussines.profile import add_profile, get_profiles, update_profile, delete_profile
from db import SessionLocal, Profile

def profile():
    # Seção: Cadastrar novo perfil
    with st.expander("➕ Criar novo Perfil"):
        new_name = st.text_input("Nome do Perfil")
        new_gerar_token = st.checkbox("Pode gerar token?")
        new_admin = st.checkbox("É administrador?")

        if st.button("Adicionar") and new_name.strip():
            add_profile(new_name.strip(), new_gerar_token, new_admin)

    st.divider()

    # Seção: Listar, editar e excluir perfis
    st.subheader("📋 Perfis Cadastrados")
    profiles = get_profiles()

    for p in profiles:
        with st.expander(f"🔧 {p.name}"):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                gerar_token_checkbox = st.checkbox("Pode gerar token", value=p.generate_token, key=f"token_{p.id}")
                admin_checkbox = st.checkbox("É admin", value=p.admin, key=f"admin_{p.id}")
            with col2:
                if st.button("💾 Salvar", key=f"save_{p.id}"):
                    update_profile(p.id, gerar_token_checkbox, admin_checkbox)
            with col3:
                if st.button("🗑️ Excluir", key=f"delete_{p.id}"):
                    delete_profile(p.id)

    st.info("⚠️ A exclusão de perfis não verifica se estão vinculados a usuários. Adicione proteção se necessário.")
