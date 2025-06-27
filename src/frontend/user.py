import streamlit as st
from bussines.user import add_user, update_user, delete_user, get_all_users
from bussines.profile import get_all_profiles, get_profiles
from config import ConfigParametersApplication, ConfigParametersAdmin

def users():
    st.subheader("👤 Gerenciar Usuários")

    defaults = {
        "username": "",
        "password": "",
        "exp_minutes": ConfigParametersApplication.TOKEN_EXP_MINUTES_NEW_USER,
        "clear_fields": False,
        "is_visible": True,
        "is_active": True
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.get("clear_fields", True):
        st.session_state.username = ""
        st.session_state.password = ""
        st.session_state.exp_minutes = ConfigParametersApplication.TOKEN_EXP_MINUTES_NEW_USER
        st.session_state.clear_fields = False
        st.session_state.is_visible = True
        st.session_state.is_active = True

    with st.expander("➕ Criar novo usuário"):
        username = st.text_input("Usuário", key="username")
        password = st.text_input("Senha", type="password", key="password")
        exp_minutes = st.number_input("Minutos até expiração do token", min_value=0, key="exp_minutes")
               
        profiles = get_all_profiles(st.session_state.profile_logger)

        if not profiles:
            st.warning("⚠ Nenhum perfil encontrado no banco de dados.")
            return

        profile_map = {p.name: p.id for p in profiles}
        selected_label = st.selectbox("Perfil do usuário", options=list(profile_map.keys()))
        selected_profile_id = profile_map[selected_label]
        if st.session_state.profile_logger == ConfigParametersApplication.PROFILE_SISTEMA:
            is_visible = st.checkbox("Visivel?", key=f"is_visible")
            is_active = st.checkbox("Ativo?", key=f"is_active")
        else:
            is_visible = True
            is_active = True    
        
        if st.button("Criar"):
            if not username or not password:
                st.warning("Usuário e senha são obrigatórios.")
            else:
                try:
                    add_user(username, password, exp_minutes, selected_profile_id, is_visible, is_active)
                    st.session_state.clear_fields = True
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar usuário: {e}")

    st.markdown("---")
    st.subheader("👥 Lista de usuários")

    if "edit_user_id" not in st.session_state:
        st.session_state.edit_user_id = None

    users = get_all_users(st.session_state.profile_logger)
    profiles = get_all_profiles(st.session_state.profile_logger)

    for user in users:
        profile = get_profiles(user.profile_id)
        
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 1, 1, 1])
        col1.markdown(f"<div style='white-space: nowrap;'><strong>👤 {user.username}</strong></div>", unsafe_allow_html=True)
        col2.markdown(f"<div style='white-space: nowrap;'><strong>🧩 {profile.name}</strong></div>", unsafe_allow_html=True)
        col3.markdown(f"<div style='white-space: nowrap;'>🕒 Token: <code>{user.token_exp_minutes} min</code></div>", unsafe_allow_html=True)

        ativo_status = "✅ Ativo" if user.is_active else "❌ Inativo"
        col4.markdown(f"<div style='white-space: nowrap;'><strong>{ativo_status}</strong></div>", unsafe_allow_html=True)

        if (ConfigParametersAdmin.NAME_ADMIN == user.username):
            edit_clicked = col5.button("✏️", key=f"edit_{user.id}", disabled=True)
            delete_clicked = col6.button("🗑️", key=f"delete_{user.id}", disabled=True)
        else:    
            edit_clicked = col5.button("✏️", key=f"edit_{user.id}")
            delete_clicked = col6.button("🗑️", key=f"delete_{user.id}")

        if delete_clicked:
            try:
                delete_user(user.id)
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
            new_exp_minutes = st.number_input("⏱️ Novo tempo de expiração (minutos)", min_value=0, value=user.token_exp_minutes, key=f"exp_{user.id}")

            new_profile_map = {p.name: p.id for p in profiles}
            current_profile_name = next((p.name for p in profiles if p.id == user.profile_id), None)
            new_profile_label = st.selectbox(
                                                "Perfil do usuário",
                                                options=list(new_profile_map.keys()),
                                                index=list(new_profile_map.keys()).index(current_profile_name) if current_profile_name else 0,
                                                key=f"profile_{user.id}"
                                            )
            new_profile_id = new_profile_map[new_profile_label]
           
            if st.session_state.profile_logger == ConfigParametersApplication.PROFILE_SISTEMA:
                new_is_visible = st.checkbox("Visivel?", key=f"is_visible_{user.id}", value=user.is_visible)
                new_is_active = st.checkbox("Ativo?", key=f"is_active_{user.id}", value=user.is_active)
            else:
                new_is_visible = True
                new_is_active  = True 
            
            col_save, col_cancel = st.columns(2)

            if col_save.button("💾 Salvar alterações", key=f"save_{user.id}"):
                try:
                    new_password_clean = new_password.strip()
                    senha_alterada = bool(new_password_clean)
                    exp_alterado = new_exp_minutes != user.token_exp_minutes
                    perfil_alterado = new_profile_id != user.profile_id
                    is_visible_alterado = new_is_visible != user.is_visible
                    is_active_alterado = new_is_active != user.is_active

                    if not senha_alterada and not exp_alterado and not perfil_alterado and not is_visible_alterado and not is_active_alterado:
                        st.warning("⚠️ Nenhuma alteração feita.")
                    else:
                        update_user(
                            user_id=user.id,
                            new_password=new_password_clean if senha_alterada else None,
                            new_token_exp_minutes=new_exp_minutes if exp_alterado else None,
                            new_profile_id=new_profile_id if perfil_alterado else None,
                            new_is_visible=new_is_visible if is_visible_alterado else None,
                            new_is_active=new_is_active if is_active_alterado else None
                        )

                        st.session_state.edit_user_id = None
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao atualizar usuário: {e}")

            if col_cancel.button("❌ Cancelar", key=f"cancel_{user.id}"):
                st.session_state.edit_user_id = None
                st.rerun()