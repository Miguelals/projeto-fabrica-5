import streamlit as st
import pandas as pd
import plotly.express as px
import time

# =====================
# Configuração da página
# =====================
st.set_page_config(
    page_title="🌍 Crescimento Populacional Animado",
    page_icon="📊",
    layout="centered"
)

st.title("🌍 Crescimento Populacional — Brasil vs Argentina")
st.markdown("""
Visualize a evolução ano a ano das populações e veja quando o **Brasil ultrapassa a Argentina**! 🇧🇷🇦🇷
""")

# =====================
# Entradas de dados
# =====================
col1, col2 = st.columns(2)
with col1:
    pop_brasil = st.number_input("População inicial do Brasil", min_value=1, step=1000, value=80000)
    taxa_brasil = st.number_input("Taxa anual de crescimento do Brasil (%)", min_value=0.0, step=0.1, value=3.0)
with col2:
    pop_argentina = st.number_input("População inicial da Argentina", min_value=1, step=1000, value=200000)
    taxa_argentina = st.number_input("Taxa anual de crescimento da Argentina (%)", min_value=0.0, step=0.1, value=1.5)

st.markdown("---")

# =====================
# Botão de cálculo e animação
# =====================
if st.button("📊 Calcular e Animar"):
    anos = 0
    brasil, argentina = pop_brasil, pop_argentina
    historico = {"Ano": [], "Brasil 🇧🇷": [], "Argentina 🇦🇷": []}

    # Caso impossível
    if taxa_brasil <= taxa_argentina and brasil < argentina:
        st.warning("⚠️ Com estas taxas, o Brasil nunca alcançará a Argentina.")
    else:
        # Cálculo anual e coleta de histórico
        while brasil < argentina:
            anos += 1
            brasil += brasil * (taxa_brasil / 100)
            argentina += argentina * (taxa_argentina / 100)
            historico["Ano"].append(anos)
            historico["Brasil 🇧🇷"].append(brasil)
            historico["Argentina 🇦🇷"].append(argentina)

        # Adiciona o último ano
        historico["Ano"].append(anos)
        historico["Brasil 🇧🇷"].append(brasil)
        historico["Argentina 🇦🇷"].append(argentina)

        st.success(f"✅ Após **{anos} anos**, o Brasil alcança ou ultrapassa a Argentina.")
        st.markdown("**População final estimada:**")
        st.markdown(f"- Brasil 🇧🇷: {brasil:,.0f} habitantes")
        st.markdown(f"- Argentina 🇦🇷: {argentina:,.0f} habitantes")

        # =====================
        # Cria DataFrame
        # =====================
        df = pd.DataFrame(historico)

        # =====================
        # Animação ano a ano com Plotly
        # =====================
        st.info("📈 Animação da evolução populacional:")

        placeholder = st.empty()

        for i in range(1, len(df) + 1):
            df_plot = df.iloc[:i]
            fig = px.line(df_plot, x="Ano", y=["Brasil 🇧🇷", "Argentina 🇦🇷"],
                          labels={"value": "População", "Ano": "Ano"},
                          title=f"Evolução da População Brasil x Argentina - Ano {df_plot['Ano'].iloc[-1]}",
                          template="plotly_white",
                          color_discrete_map={"Brasil 🇧🇷": "#FF5733", "Argentina 🇦🇷": "#3498DB"})
            
            fig.update_traces(mode="lines+markers", marker=dict(size=10))
            fig.update_layout(hovermode="x unified")
            placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(0.3)
