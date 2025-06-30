    
import streamlit as st
import pandas as pd
import plotly.express as px
from bussines.token import get_all_tokens

def token():
    df_tokens = get_all_tokens()

    if not df_tokens.empty:
        df_tokens["Data"] = pd.to_datetime(df_tokens["Data"])
        df_tokens["DataDia"] = df_tokens["Data"].dt.date
        df_tokens["DataFormatada"] = df_tokens["Data"].dt.strftime("%d/%m/%Y")

    if df_tokens.empty :
        st.info("Nenhum dado registrado ainda.")
        return

    st.subheader("🎛️ Filtros de Tokens")

    usuarios = sorted(df_tokens["Usuário"].unique())
    usuario_selecionado = st.selectbox("👤 Filtrar por usuário", options=["Todos"] + usuarios, key="token_usuario")

    min_date, max_date = df_tokens["DataDia"].min(), df_tokens["DataDia"].max()
    col1, col2 = st.columns(2)
    with col1:
        data_inicial = st.date_input("📅 Data inicial", value=min_date, min_value=min_date, max_value=max_date, key="token_data_ini")
    with col2:
        data_final = st.date_input("📅 Data final", value=max_date, min_value=min_date, max_value=max_date, key="token_data_fim")

    df_filtrado = df_tokens[
        (df_tokens["DataDia"] >= data_inicial) & (df_tokens["DataDia"] <= data_final)
    ]
    if usuario_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Usuário"] == usuario_selecionado]

    st.metric("🔐 Tokens Gerados no Período", len(df_filtrado))

    if df_filtrado.empty:
        st.info("Nenhum token encontrado.")
    else:
        df_grouped = df_filtrado.groupby(["DataDia", "Usuário"]).size().reset_index(name="Quantidade")
        df_grouped["DataDia"] = df_grouped["DataDia"].apply(lambda x: x.strftime("%d/%m"))

        fig = px.bar(
            df_grouped,
            y="DataDia",
            x="Quantidade",
            color="Usuário",
            orientation="h",
            text="Quantidade",
            title="📊 Tokens Gerados por Data e Usuário",
        )

        fig.update_layout(
            yaxis_title="Data",
            xaxis_title="Quantidade de Tokens",
            barmode="stack",
            margin=dict(t=30, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

        df_por_usuario = df_filtrado.groupby("Usuário").size().reset_index(name="Total")
        fig_pizza = px.pie(df_por_usuario, names="Usuário", values="Total", hole=0.4,
                            title="🧑‍💼 Distribuição de Tokens por Usuário")
        st.plotly_chart(fig_pizza, use_container_width=True)

        with st.expander("📄 Ver dados em tabela"):
            df_tabela = df_filtrado.groupby(["DataDia", "Usuário"]).size().reset_index(name="Quantidade")
            df_tabela["DataDia"] = df_tabela["DataDia"].apply(lambda x: x.strftime("%d/%m/%Y"))
            st.dataframe(df_tabela, use_container_width=True)