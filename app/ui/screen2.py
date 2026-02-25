import streamlit as st
import plotly.express as px
from app.processador import ProcessadorDados

core = ProcessadorDados()

# 1️⃣ carregar
if not core.carregar_dados():
    st.error("Erro ao carregar o arquivo Excel.")
    st.stop()

# 2️⃣ limpar (boa prática)
core.limpar_dados()

# 3️⃣ processar
res = core.total_presos_por_guarnicao()

# 4️⃣ validar resultado
if res.empty:
    st.warning("Nenhum dado encontrado.")
    st.stop()

fig = px.bar(
    res,
    x='MÊS',
    y='PRESOS/APREENDIDOS',
    color='TIPO DE SERVIÇO',
    barmode='group'
)

st.plotly_chart(fig, use_container_width=True)