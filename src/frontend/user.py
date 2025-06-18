import streamlit as st
from bussines.user import create_user, update_user, delete_user, get_all_users
from config import ConfigParametersApplication
from db import SessionLocal, Profile


def users():
    st.subheader("👤 Gerenciar Usuários")

    # Valores padrão dos campos
    defaults = {
        "username": "",
        "password": "",
        "exp_minutes": ConfigParametersApplication.DEFAULT_EXP_MINUTES,
        "clear_fields": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Reset após criação
    if st.session_state.get("clear_fields", True):
        st.session_state.username = ""
        st.session_state.password = ""
        st.session_state.exp_minutes = ConfigParametersApplication.DEFAULT_EXP_MINUTES
        st.session_state.clear_fields = False

    # --- Formulário de Criação ---
    with st.expander("➕ Criar novo usuário"):
        username = st.text_input("Usuário", key="username")
        password = st.text_input("Senha", type="password", key="password")
        exp_minutes = st.number_input("Minutos até expiração do token", min_value=1, key="exp_minutes")

        # Buscar perfis
        session = SessionLocal()
        profiles = session.query(Profile).all()
        session.close()

        if not profiles:
            st.warning("⚠ Nenhum perfil encontrado no banco de dados.")
            return

        profile_map = {p.name: p.id for p in profiles}
        selected_label = st.selectbox("Perfil do usuário", options=list(profile_map.keys()))
        selected_profile_id = profile_map[selected_label]

        if st.button("Criar"):
            if not username or not password:
                st.warning("Usuário e senha são obrigatórios.")
            else:
                try:
                    create_user(username, password, exp_minutes, selected_profile_id)
                    st.success(f"✅ Usuário '{username}' criado com sucesso.")
                    st.session_state.clear_fields = True
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar usuário: {e}")

    st.markdown("---")
    st.subheader("👥 Lista de usuários")

    if "edit_user_id" not in st.session_state:
        st.session_state.edit_user_id = None

    users = get_all_users()
    session = SessionLocal()
    profile_dict = {p.id: p.name for p in session.query(Profile).all()}
    session.close()

    for user in users:
        if user.username == "admin":
            continue

        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
        col1.markdown(f"**👤 {user.username}**")
        col2.markdown(f"**🧩 {profile_dict.get(user.profile_id, 'Desconhecido')}**")
        col3.markdown(f"🕒 Token: `{user.token_exp_minutes} min`")

        edit_clicked = col4.button("✏️", key=f"edit_{user.id}")
        delete_clicked = col5.button("🗑️", key=f"delete_{user.id}")

        if delete_clicked:
            try:
                delete_user(user.username)
                if st.session_state.edit_user_id == user.id:
                    st.session_state.edit_user_id = None
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao excluir usuário: {e}")

        if edit_clicked:
            st.session_state.edit_user_id = user.id

        if st.session_state.edit_user_id == user.id:
            st.markdown("---")
            st.markdown(f"### ✏️ Editar usuário: `{user.username}`")

            new_password = st.text_input("🔑 Nova senha", type="password", key=f"pw_{user.id}")
            new_exp_minutes = st.number_input("⏱️ Novo tempo de expiração (minutos)", min_value=1, value=user.token_exp_minutes, key=f"exp_{user.id}")
            new_profile_label = st.selectbox("Perfil do usuário", options=list(profile_map.keys()), index=list(profile_map.keys()).index(profile_dict.get(user.profile_id, "Administrador")), key=f"profile_{user.id}")
            new_profile_id = profile_map[new_profile_label]

            col_save, col_cancel = st.columns(2)

            if col_save.button("💾 Salvar alterações", key=f"save_{user.id}"):
                try:
                    # Só envia o que foi alterado
                    new_password_clean = new_password.strip()
                    senha_alterada = bool(new_password_clean)
                    exp_alterado = new_exp_minutes != user.token_exp_minutes
                    perfil_alterado = new_profile_id != user.profile_id

                    if not senha_alterada and not exp_alterado and not perfil_alterado:
                        st.warning("⚠️ Nenhuma alteração feita.")
                    else:
                        update_user(
                            username=user.username,
                            new_password=new_password_clean if senha_alterada else None,
                            new_token_exp_minutes=new_exp_minutes if exp_alterado else None,
                            new_profile_id=new_profile_id if perfil_alterado else None
                        )

                        st.success("✅ Alterações salvas com sucesso.")
                        st.session_state.edit_user_id = None
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao atualizar usuário: {e}")

            if col_cancel.button("❌ Cancelar", key=f"cancel_{user.id}"):
                st.session_state.edit_user_id = None
                st.rerun()