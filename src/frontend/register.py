import streamlit as st
from bussines.user import add_user
from bussines.profile import get_default_profile
from util import time_sleep
from config import ConfigParametersApplication

@st.dialog("📝 Criar nova conta")
def register():
    st.markdown("Preencha os dados abaixo para solicitar seu acesso:")

    new_username = st.text_input("👤 Novo usuário", key="cadastro_user")
    new_password = st.text_input("🔑 Nova senha", type="password", key="cadastro_senha")
    confirm_password = st.text_input("🔁 Confirme a senha", type="password", key="cadastro_confirm")

    if st.button("📨 Enviar solicitação", key="enviar_cadastro"):
        if not new_username or not new_password or not confirm_password:
            st.warning("Por favor, preencha todos os campos.")
        elif new_password != confirm_password:
            st.warning("As senhas não coincidem. Tente novamente.")
        else:
            try:
                add_user(
                    username=new_username,
                    password=new_password,
                    token_exp_minutes=ConfigParametersApplication.TOKEN_EXP_MINUTES_AUTOMATIC_USER_CREATION,
                    profile_id=get_default_profile(),
                    is_visible=True,
                    is_active=False 
                )
                st.success("✅ Cadastro enviado! Aguarde liberação de um administrador.")
                time_sleep()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao cadastrar: {e}")


                

        