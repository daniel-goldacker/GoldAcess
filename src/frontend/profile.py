import streamlit as st
from bussines.profile import get_all_profiles, add_profile, update_profile, delete_profile
from config import ConfigParametersAdmin

def profile():
    st.subheader("🧩 Gerenciar Perfis")

    # Campos padrão
    defaults = {
        "profile_name": "",
        "generate_token": False,
        "admin": False,
        "clear_fields": False,
        "edit_profile_id": None,
        "visible": True
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.get("clear_fields", True):
        st.session_state.profile_name = ""
        st.session_state.generate_token = False
        st.session_state.admin = False
        st.session_state.visible = True
        st.session_state.clear_fields = False


    # Formulário de criação
    with st.expander("➕ Criar novo perfil"):
        profile_name = st.text_input("Nome do Perfil", key="profile_name")
        generate_token = st.checkbox("Pode gerar token?", key="generate_token")
        admin = st.checkbox("É administrador?", key="admin")

        if st.session_state.profile_logger == ConfigParametersAdmin.PROFILE_ADMIN:
            visible = st.checkbox("Visivel ?", key="visible")
        else:
            visible = True 
        

        if st.button("Criar"):
            if not profile_name.strip():
                st.warning("⚠️ O nome do perfil é obrigatório.")
            else:
                try:
                    add_profile(profile_name.strip(), generate_token, admin, visible)
                    st.success("✅ Perfil criado com sucesso.")
                    st.session_state.clear_fields = True
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar perfil: {e}")

    st.markdown("---")
    st.subheader("📋 Lista de Perfis")

    profiles = get_all_profiles(st.session_state.profile_logger)

    for profile in profiles:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1]) 
        col1.markdown(f"**🧩 {profile.name}**")
        col2.markdown(f"**{'🔑 Gera token' if profile.generate_token else '❌ Não gera token'}**")
        col3.markdown( f"**{'👑 Admin' if profile.admin else '👤 Padrão'}**")
        edit_clicked = col4.button("✏️", key=f"edit_{profile.id}")
        delete_clicked = col5.button("🗑️", key=f"delete_{profile.id}")

        if delete_clicked:
            try:
                delete_profile(profile.id)
                if st.session_state.edit_profile_id == profile.id:
                    st.session_state.edit_profile_id = None
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao excluir perfil: {e}")

        if edit_clicked:
            st.session_state.edit_profile_id = profile.id

        if st.session_state.edit_profile_id == profile.id:
            st.markdown("---")
            st.markdown(f"### ✏️ Editar perfil: `{profile.name}`")

            new_generate_token = st.checkbox("Pode gerar token?", value=profile.generate_token, key=f"token_{profile.id}")
            new_admin = st.checkbox("É administrador?", value=profile.admin, key=f"admin_{profile.id}")
            
            if st.session_state.profile_logger == ConfigParametersAdmin.PROFILE_ADMIN:
                new_visible = st.checkbox("Visivel?", value=profile.visible, key=f"visible_{profile.id}")
            else:
                new_visible = True 
                
            col_save, col_cancel = st.columns(2)

            if col_save.button("💾 Salvar alterações", key=f"save_{profile.id}"):
                try:
                    update_profile(profile.id, new_generate_token, new_admin, new_visible)
                    st.success("✅ Alterações salvas com sucesso.")
                    st.session_state.edit_profile_id = None
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao atualizar perfil: {e}")

            if col_cancel.button("❌ Cancelar", key=f"cancel_{profile.id}"):
                st.session_state.edit_profile_id = None
                st.rerun()
