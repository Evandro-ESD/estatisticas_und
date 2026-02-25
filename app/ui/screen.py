import streamlit as st
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np


# Configuração
st.set_page_config(
    page_title="Dashboard Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Título com HTML
st.markdown('<h1 class="main-header">📊 Dashboard Analytics</h1>',
            unsafe_allow_html=True)

# Sidebar com controles
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/FF4B4B/FFFFFF?text=LOGO")
    st.title("Controles")

    # Upload múltiplos arquivos
    # uploaded_files = st.file_uploader(
    #     "Upload CSV files",
    #     type=['csv'],
    #     accept_multiple_files=True
    # )

    st.divider()

    # Data range
    start_date = st.date_input(
        "Data inicial",
        datetime.now() - timedelta(days=30)
    )
    end_date = st.date_input(
        "Data final",
        datetime.now()
    )

    st.divider()

    # Botão de refresh
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()


# Função para carregar dados (com cache)
@st.cache_data
def load_data(files):
    if files:
        dfs = []
        for file in files:
            df = pd.read_csv(file)
            dfs.append(df)
        return pd.concat(dfs, ignore_index=True)
    else:
        # Dados de exemplo
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        return pd.DataFrame({
            'date': dates,
            'sales': np.random.randint(1000, 5000, len(dates)),
            'customers': np.random.randint(50, 200, len(dates)),
            'category': np.random.choice(['A', 'B', 'C'], len(dates)),
            'region': np.random.choice(['North', 'South', 'East', 'West'], len(dates))
        })


# Carregar dados
uploaded_files = []  # Placeholder para arquivos carregados
df = load_data(uploaded_files)


# Tabs para organização
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Visão Geral",
    "📊 Análise Detalhada",
    "🗺️ Mapas",
    "📑 Relatórios"
])

with tab1:
    # KPIs em cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Total Vendas</h3>
            <h2>R$ {:,.0f}</h2>
        </div>
        """.format(df['sales'].sum()), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Ticket Médio</h3>
            <h2>R$ {:,.2f}</h2>
        </div>
        """.format(df['sales'].mean()), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Total Clientes</h3>
            <h2>{:,.0f}</h2>
        </div>
        """.format(df['customers'].sum()), unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Dias Analisados</h3>
            <h2>{}</h2>
        </div>
        """.format(len(df)), unsafe_allow_html=True)

    # Gráficos
    col5, col6 = st.columns(2)

    with col5:
        fig = px.line(df, x='date', y='sales',
                      title='Vendas por Dia')
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        fig = px.pie(df, values='sales', names='category',
                     title='Distribuição por Categoria')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Análise detalhada com filtros
    col7, col8 = st.columns(2)

    with col7:
        category_filter = st.multiselect(
            "Categorias",
            options=df['category'].unique(),
            default=df['category'].unique()
        )

    with col8:
        region_filter = st.multiselect(
            "Regiões",
            options=df['region'].unique(),
            default=df['region'].unique()
        )

    # Aplicar filtros
    filtered_df = df[
        (df['category'].isin(category_filter)) &
        (df['region'].isin(region_filter))
        ]

    # Heatmap de correlação
    fig = px.imshow(
        filtered_df[['sales', 'customers']].corr(),
        text_auto=True,
        title='Matriz de Correlação'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tabela interativa
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "date": "Data",
            "sales": st.column_config.NumberColumn("Vendas", format="R$ %d"),
            "customers": "Clientes",
            "category": "Categoria",
            "region": "Região"
        }
    )

# Footer
st.divider()
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Dashboard criado com Python e Streamlit | "
    f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    "</p>",
    unsafe_allow_html=True
)