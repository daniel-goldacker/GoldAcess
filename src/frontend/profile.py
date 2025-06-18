import streamlit as st
from sqlalchemy.orm import Session
from db import SessionLocal, Profile

# Funções auxiliares
def get_profiles():
    session: Session = SessionLocal()
    profiles = session.query(Profile).all()
    session.close()
    return profiles

def add_profile(name, generate_token, admin):
    session = SessionLocal()
    existing = session.query(Profile).filter_by(name=name).first()
    if existing:
        st.warning("Perfil já existe!")
    else:
        profile = Profile(name=name, generate_token=generate_token, admin=admin)
        session.add(profile)
        session.commit()
        st.success("Perfil criado com sucesso.")
    session.close()

def update_profile(profile_id, generate_token, admin):
    session = SessionLocal()
    profile = session.query(Profile).filter_by(id=profile_id).first()
    if profile:
        profile.generate_token = generate_token
        profile.admin = admin
        session.commit()
        st.success("Perfil atualizado com sucesso.")
    else:
        st.error("Perfil não encontrado.")
    session.close()

def delete_profile(profile_id):
    session = SessionLocal()
    profile = session.query(Profile).filter_by(id=profile_id).first()
    if profile:
        session.delete(profile)
        session.commit()
        st.success("Perfil excluído com sucesso.")
    else:
        st.error("Perfil não encontrado.")
    session.close()

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
