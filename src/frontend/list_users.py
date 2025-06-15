
import streamlit as st
from auth import (
    update_password,
    delete_user,
    get_all_users,
    update_token,
    update_profile
)

def list_users(username_logged):
    if "edit_user_id" not in st.session_state:
        st.session_state.edit_user_id = None
    
    st.subheader("👥 Usuários cadastrados")

    for user in get_all_users():
        if user.username == "admin":
            continue  # pula o admin, não mostra na lista

        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
        col1.markdown(f"**👤 {user.username}**")
        col2.markdown(f"**🧩 {user.profile}**")
        col3.markdown(f"🕒 Token: `{user.token_exp_minutes} min`")

        edit_clicked = col4.button("✏️", key=f"edit_{user.id}")
        if (username_logged != user.username):
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
            with st.container():
                st.markdown("---")
                st.markdown(f"### ✏️ Editar usuário: `{user.username}`")

                new_password = st.text_input("🔑 Nova senha", type="password", key=f"pw_{user.id}")
                new_exp_minutes = st.number_input(
                    "⏱️ Novo tempo de expiração (minutos)",
                    min_value=1,
                    value=user.token_exp_minutes,
                    key=f"exp_{user.id}"
                )
                new_profile = st.selectbox(
                    "Perfil do usuário",
                    options=["Administrador", "APIs"],
                    index=["Administrador", "APIs"].index(user.profile) if user.profile in ["Administrador", "Sistema", "APIs"] else 0,
                    key=f"profile_{user.id}"
                )

                col_save, col_cancel = st.columns(2)

                with col_save:
                    if st.button("💾 Salvar alterações", key=f"save_{user.id}"):
                        senha_alterada = new_password.strip() != ""
                        exp_alterado = new_exp_minutes != user.token_exp_minutes
                        perfil_alterado = new_profile != user.profile

                        if not senha_alterada and not exp_alterado and not perfil_alterado:
                            st.warning("⚠️ Nenhuma alteração feita.")
                        else:
                            try:
                                if senha_alterada:
                                    update_password(user.username, new_password)
                                if exp_alterado:
                                    update_token(user.username, new_exp_minutes)
                                if perfil_alterado:
                                    update_profile(user.username, new_profile)

                                st.session_state.edit_user_id = None
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar usuário: {e}")

                with col_cancel:
                    if st.button("❌ Cancelar", key=f"cancel_{user.id}"):
                        st.session_state.edit_user_id = None
                        st.rerun()