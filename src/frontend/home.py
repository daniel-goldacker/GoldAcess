import streamlit as st
from util import get_image_base64

def home():
    image_base64 = get_image_base64("img/GoldAcess.png")
    
    st.markdown(
    "<h3 style='text-align: center;'>Gerencie acessos com segurança e eficiência</h3>",
    unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style='text-align: center; padding: 5px 0 10px 0;'>
            <img src="data:image/png;base64,{image_base64}" alt="GoldAcess Logo" width="300"/>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""    
    O **GoldAcess Autenticação** é sua central de controle de autenticação e autorização de usuários, oferecendo uma interface intuitiva para administração de:
    
    - 👤 **Usuários**
    - 🛡️ **Perfis de acesso**
    - 🔐 **Tokens de autenticação**
    - 📊 **Monitoramento**  
    - ⚙️ **Configurações de segurança**
    
    ---
    
    ### 🚀 Principais Benefícios:
    - Autenticação baseada em **JWT**
    - Gerenciamento simples e seguro de usuários
    - Integração fácil com outras aplicações via API
    - Controle granular de visibilidade e perfis
    
    ---
    
    ### 🔧 Comece agora
    Utilize o menu lateral para navegar entre as funcionalidades do sistema.

    ---
    
    👨‍💻 Desenvolvido com carinho por nossa equipe para facilitar o seu trabalho com segurança digital.
    """)
