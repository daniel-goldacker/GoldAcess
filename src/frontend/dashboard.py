import streamlit as st
from frontend.analytics.http_status import http_status
from frontend.analytics.token import token   

def dashboard():

    st.subheader("📊 Painel de Monitoramento")

    aba_token, aba_http = st.tabs(["🔐 Geração de Tokens", "🌐 Status HTTP"])

    with aba_token:
        token()
      
    with aba_http:
        http_status()
      