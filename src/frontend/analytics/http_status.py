import streamlit as st
import plotly.express as px
import pandas as pd
from bussines.token import get_all_request_logs

def http_status():
    df_http = get_all_request_logs()

    if not df_http.empty:
        df_http["Data"] = pd.to_datetime(df_http["Data"])
        df_http["DataDia"] = df_http["Data"].dt.date
        df_http["DataFormatada"] = df_http["Data"].dt.strftime("%d/%m/%Y")

    if df_http.empty and df_http.empty:
        st.info("Nenhum dado registrado ainda.")
        return

    st.subheader("🛰️ Análise de Status HTTP")

    if df_http.empty:
        st.info("Nenhuma requisição registrada.")
    else:
        with st.expander("🎛️ Filtros de HTTP Status", expanded=True):
            col1, col2 = st.columns(2)

            min_http, max_http = df_http["DataDia"].min(), df_http["DataDia"].max()
            with col1:
                filtro_data_ini = st.date_input("📅 Data inicial", value=min_http, min_value=min_http, max_value=max_http, key="http_data_ini")
            with col2:
                filtro_data_fim = st.date_input("📅 Data final", value=max_http, min_value=min_http, max_value=max_http, key="http_data_fim")

            status_unicos = sorted(df_http["Status HTTP"].unique())
            status_selecionados = st.multiselect("🔢 Filtrar por códigos de status", options=status_unicos, default=status_unicos, key="http_status_codes")

        df_http_filtros = df_http[
            (df_http["DataDia"] >= filtro_data_ini) &
            (df_http["DataDia"] <= filtro_data_fim) &
            (df_http["Status HTTP"].isin(status_selecionados))
        ]

        if df_http_filtros.empty:
            st.warning("Nenhum dado encontrado com os filtros selecionados.")
        else:
            st.metric("🌐 Total de Requisições no Período", len(df_http_filtros))

            col1, col2 = st.columns(2)
            with col1:
                for status_code in status_selecionados:
                    count = len(df_http_filtros[df_http_filtros["Status HTTP"] == status_code])
                    st.metric(f"Status {status_code}", count)

            with col2:
                df_http_total = df_http_filtros.groupby("Status HTTP").size().reset_index(name="Total")
                fig_http_pizza = px.pie(df_http_total, names="Status HTTP", values="Total", hole=0.4,
                                        title="📊 Distribuição de Códigos HTTP")
                st.plotly_chart(fig_http_pizza, use_container_width=True)

            with st.expander("📈 Ver Evolução por Requisição"):
                df_http_grouped = df_http_filtros.groupby(["DataDia", "Status HTTP"]).size().reset_index(name="Quantidade")
                fig_http = px.bar(df_http_grouped, x="DataDia", y="Quantidade", color="Status HTTP", text="Quantidade")
                fig_http.update_layout(xaxis_title="Data", margin=dict(t=10, b=20))
                fig_http.update_xaxes(tickformat="%d/%m/%Y")
                st.plotly_chart(fig_http, use_container_width=True)

            with st.expander("📋 Ver tabela detalhada"):
                df_http_total["Percentual"] = round(100 * df_http_total["Total"] / df_http_total["Total"].sum(), 2)
                st.dataframe(df_http_total, use_container_width=True)
