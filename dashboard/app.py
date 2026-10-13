import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px

st.set_page_config(
    page_title="AGI Core - Control Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠 AGI Core Engine - Dashboard de Monitoramento em Tempo Real")
st.markdown("---")

# Sidebar - Configurações de Controle
st.sidebar.header("⚙️ Painel de Controle de Execução")
num_workers = st.sidebar.slider("Ray Workers Ativos", 1, 16, 4)
mcts_sims = st.sidebar.slider("Simulações MCTS (Tipo-2)", 10, 100, 30)
safety_active = st.sidebar.checkbox("Guardrails de Segurança Ativos", value=True)
run_simulation = st.sidebar.button("▶ Executar Ciclo Cognitivo", type="primary")

# Layout de Métrica
col1, col2, col3, col4 = st.columns(4)
col1.metric("Status do Sistema", "ONLINE", "Normativo")
col2.metric("Ray Workers Cluster", f"{num_workers} Ativos", "+2")
col3.metric("Nós MCTS Avaliados/s", f"{mcts_sims * 10}", "+15%")
col4.metric("Intervenções de Segurança", "03", "-12%")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Desempenho e Recompensa", "🌲 Árvore MCTS & Decisão", "🕸️ Grafo Neo4j & Ontologia"])

with tab1:
    st.subheader("Métricas de Recompensa em Tempo Real (Workers Ray)")
    chart_data = pd.DataFrame(
        np.random.randn(20, num_workers),
        columns=[f"Worker {i+1}" for i in range(num_workers)]
    ).cumsum()
    fig = px.line(chart_data, labels={"value": "Recompensa Acumulada", "index": "Passo Temporal"})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Visualizador de Decisão e Exploração MCTS")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.write("**Estatísticas do Nó Raiz MCTS:**")
        st.json({
            "visit_count": mcts_sims,
            "c_puct": 1.4,
            "best_action_index": 1,
            "prior_probability": 0.33
        })
    with col_b:
        mcts_df = pd.DataFrame({
            "Ação": ["Rotação Esquerda", "Manter Força", "Rotação Direita"],
            "Visitas MCTS": [5, mcts_sims - 8, 3],
            "Valor Esperado Q": [-0.8, 2.4, -1.2]
        })
        st.bar_chart(mcts_df.set_index("Ação"))

with tab3:
    st.subheader("Estrutura do Grafo de Conhecimento Causal (Neo4j)")
    st.info("Conectado ao nó Neo4j em bolt://localhost:7687")
    edges_df = pd.DataFrame([
        {"Origem": "ESTADO_ESTÁVEL", "Ação": "MANTER", "Destino": "ESTADO_ESTÁVEL", "Recompensa": 1.0},
        {"Origem": "LIMITE_CRÍTICO_POSITIVO", "Ação": "REVERTER", "Destino": "ESTADO_ESTÁVEL", "Recompensa": 2.5},
        {"Origem": "LIMITE_CRÍTICO_NEGATIVO", "Ação": "ACELERAR", "Destino": "ESTADO_ALERTA", "Recompensa": -5.0},
    ])
    st.dataframe(edges_df, use_container_width=True)
