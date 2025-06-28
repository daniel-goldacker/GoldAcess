import streamlit as st
import plotly.express as px
from bussines.token import get_all_tokens

def monitoring():
    st.markdown("<h2 style='text-align: center;'>📊 Painel de Geração de Tokens</h2>", unsafe_allow_html=True)
    st.markdown("---")

    df = get_all_tokens()

    if df.empty:
        st.info("Nenhum token gerado até o momento.")
        return

    # Filtros
    usuarios = sorted(df["Usuário"].unique())
    usuario_selecionado = st.selectbox("👤 Filtrar por usuário", options=["Todos"] + usuarios)

    min_data, max_data = df["Data"].min(), df["Data"].max()
    col1, col2 = st.columns(2)
    with col1:
        data_inicial = st.date_input("📅 Data inicial", value=min_data, min_value=min_data, max_value=max_data)
    with col2:
        data_final = st.date_input("📅 Data final", value=max_data, min_value=min_data, max_value=max_data)

    # Aplicar filtros
    df = df[(df["Data"] >= data_inicial) & (df["Data"] <= data_final)]
    if usuario_selecionado != "Todos":
        df = df[df["Usuário"] == usuario_selecionado]

    # Cartão total
    total = len(df)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(label="🔐 Total de Tokens no Período", value=total)

    # Gráfico de barras por dia e usuário
    df_grouped = df.groupby(["Data", "Usuário"]).size().reset_index(name="Quantidade")
    fig = px.bar(
        df_grouped,
        x="Data",
        y="Quantidade",
        color="Usuário",
        barmode="group",
        text="Quantidade",
        labels={"Data": "Data", "Quantidade": "Tokens"},
        height=400
    )
    fig.update_layout(margin=dict(t=10, b=20), xaxis_title=None, yaxis_title="Quantidade")
    st.plotly_chart(fig, use_container_width=True)

    # Tabela
    with st.expander("📄 Ver dados em tabela"):
        st.dataframe(df_grouped, use_container_width=True)

    # Gráficos complementares
    st.markdown("## 📊 Análises Complementares")
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Gráfico de linha acumulado
    with col1:
        df_cumulativo = df.groupby("Data").size().cumsum().reset_index(name="Tokens Acumulados")
        fig_cumulado = px.line(
            df_cumulativo, x="Data", y="Tokens Acumulados", markers=True,
            title="📈 Tokens Acumulados ao Longo do Tempo"
        )
        st.plotly_chart(fig_cumulado, use_container_width=True)

    # Gráfico de pizza por usuário
    with col2:
        df_por_usuario = df.groupby("Usuário").size().reset_index(name="Total")
        fig_pizza = px.pie(df_por_usuario, names="Usuário", values="Total",
                           title="🧑‍💼 Distribuição de Tokens por Usuário")
        st.plotly_chart(fig_pizza, use_container_width=True)