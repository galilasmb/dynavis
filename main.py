import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import asyncio
import streamlit as st
import plotly.express as px
import base64
import io
import warnings

pd.set_option('display.max_columns', 200)
warnings.filterwarnings('ignore')

def image_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.set_page_config(
    page_title="Painel de Indicadores SAPS",
    page_icon="imgs/icon.jpg",
    layout="wide"
)

# Logo
img_path_left = "imgs/logo_gov.png"
img_path_right = "imgs/logo_ms_brasil.png"
img_base64_left = image_to_base64(img_path_left)
img_base64_right = image_to_base64(img_path_right)

HEADER_HEIGHT_PX = 70
LOGO_PADDING_RIGHT_PX = 330

st.markdown(
    f"""
    <style>
    /* --- Sidebar Styles --- */
    section[data-testid="stSidebar"] {{
        background-color: #003366 !important;
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .st-emotion-cache-10trblm {{
        color: white !important;
    }}
    section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] div[class*="-placeholder"] {{
        color: black !important;
    }}

    /* --- CUSTOM-HEADER FIXO --- */
    .custom-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #003366;
        padding: 10px {LOGO_PADDING_RIGHT_PX}px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        z-index: 1031;
        box-sizing: border-box;
        height: {HEADER_HEIGHT_PX}px;
    }}
    .custom-header h1 {{
        font-size: 20px;
        text-align: center;
        margin: 0;
        color: white;
    }}

    .custom-header .logo-esquerda {{
        position: absolute;
        left: {LOGO_PADDING_RIGHT_PX}px; 
        top: 50%; 
        transform: translateY(-50%); 
        height: 40px;
        flex-shrink: 0;
    }}

    .custom-header .logo-direita {{
        position: absolute;
        right: {LOGO_PADDING_RIGHT_PX}px; 
        top: 50%; 
        transform: translateY(-50%); 
        height: 40px;
        flex-shrink: 0;
    }}

    /* --- STREAMLIT DEFAULT HEADER --- */
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
        border-bottom: none !important;
        box-shadow: none !important;
    }}

    /* --- BOTÃO DA SIDEBAR --- */
    button[title="Expand sidebar"], button[title="Collapse sidebar"],
    button[aria-label="Expand sidebar"], button[aria-label="Collapse sidebar"],
    button[data-testid="stBaseButton-headerNoPadding"] {{
        position: relative; z-index: 1032 !important;
    }}
    button[title="Expand sidebar"] svg, button[title="Collapse sidebar"] svg,
    button[aria-label="Expand sidebar"] svg, button[aria-label="Collapse sidebar"] svg,
    button[data-testid="stBaseButton-headerNoPadding"] svg {{
        fill: white !important;
    }}

    /* --- Ajuste para o CONTEÚDO PRINCIPAL --- */
    div.main, section[data-testid="stAppViewContainer"] {{
        padding-top: {HEADER_HEIGHT_PX}px !important;
    }}
    </style>

    <div class="custom-header">
        <img src="data:image/png;base64,{img_base64_left}" class="logo-esquerda">
        <h1>Painel de Cadastros de Saúde da APS</h1>
        <img src="data:image/png;base64,{img_base64_right}" class="logo-direita">        
    </div>
    """,
    unsafe_allow_html=True
)

# Interface de Upload
with st.sidebar:
    st.header("Configuração")
    uploaded_file = st.file_uploader("Carregue o arquivo CSV", type=["csv"])

if uploaded_file is not None:
    # Carregar o arquivo CSV do upload
    df = pd.read_csv(uploaded_file, sep=',')
    
    columns = df.columns.tolist()

    selected_cols = st.multiselect(
        "Selecione 1 a 3 colunas:",
        columns,
        max_selections=3,
        placeholder="Escolha as colunas desejadas..."
    )
            
    if not selected_cols:
        st.warning("Por favor, selecione ao menos uma coluna.")
    else:

        for col in selected_cols:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass

        # substituir valores nulos por uma string para evitar problemas em value_counts
        safe_df = df[selected_cols].fillna('SEM INFORMAÇÃO')

        group = safe_df.value_counts(dropna=False).reset_index()
        group.columns = selected_cols + ['total']
        group['percentual'] = (group['total'] / group['total'].sum()) * 100 

        aba_tabela, aba_graficos = st.tabs(["Tabela", "Gráficos"])

        with aba_tabela:
            st.dataframe(group.style.format({'percentual': '{:.2f}%'}), use_container_width=True)

            # CSV e botão de download
            csv_buffer = io.StringIO()
            group.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Baixar dados",
                data=csv_buffer.getvalue(),
                file_name="tabela_agrupada.csv",
                mime="text/csv"
            )

        with aba_graficos:
            st.subheader("Visualizações")

            if len(selected_cols) == 1:
                col = selected_cols[0]
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Barras Verticais**")
                    st.plotly_chart(px.bar(group, x=col, y='total', text='total',
                                           labels={col: col, 'total': 'Contagem'}), use_container_width=True)

                with col2:
                    st.markdown("**Pizza**")
                    st.plotly_chart(px.pie(group, names=col, values='total', hole=0.3), use_container_width=True)

                st.markdown("**Barras Horizontais**")
                st.plotly_chart(px.bar(group, y=col, x='total', orientation='h', text='total'), use_container_width=True)

                st.markdown("**Treemap**")
                st.plotly_chart(px.treemap(group, path=[col], values='total'), use_container_width=True)

            elif len(selected_cols) == 2:
                col1, col2 = selected_cols

                numeric_col = next((col for col in selected_cols if pd.api.types.is_numeric_dtype(df[col])), None)
                categorical_col = next((col for col in selected_cols if not pd.api.types.is_numeric_dtype(df[col])), None)

                date_cols = [col for col in selected_cols if pd.api.types.is_datetime64_any_dtype(df[col])]
    
                if date_cols:
                    time_col = date_cols[0]
                    value_col = [col for col in selected_cols if col != time_col][0]

                    st.markdown("**Série Temporal**")
                    time_data = df[[time_col, value_col]].copy()
                    time_data['Contagem'] = 1
                    time_grouped = time_data.groupby([time_col, value_col]).count().reset_index()

                    fig = px.line(time_grouped, x=time_col, y="Contagem", color=value_col)
                    st.plotly_chart(fig, use_container_width=True)
    
                if all(pd.api.types.is_numeric_dtype(df[col]) for col in selected_cols):
                    st.markdown("**Dispersão (Scatter)**")
                    st.plotly_chart(px.scatter(df, x=selected_cols[0], y=selected_cols[1]), use_container_width=True)

                if numeric_col and categorical_col:
                    st.markdown("**Boxplot**")
                    st.plotly_chart(px.box(df, x=categorical_col, y=numeric_col), use_container_width=True)

                    st.markdown("**Violin Plot**")
                    st.plotly_chart(px.violin(df, x=categorical_col, y=numeric_col, box=True, points="all"), use_container_width=True)


                st.markdown("**Barras Agrupadas**")
                st.plotly_chart(px.bar(group, x=col1, y='total', color=col2, barmode='group', text='total'), use_container_width=True)

                st.markdown("**Heatmap Categórico**")
                pivot = group.pivot(index=col1, columns=col2, values='total').fillna(0)
                fig = px.imshow(pivot, text_auto=True, aspect="auto", labels=dict(color="Contagem"))
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("**Treemap**")
                st.plotly_chart(px.treemap(group, path=[col1, col2], values='total'), use_container_width=True)

                st.markdown("**Sunburst**")
                st.plotly_chart(px.sunburst(group, path=[col1, col2], values='total'), use_container_width=True)

            elif len(selected_cols) == 3:
                col1, col2, col3 = selected_cols

                st.markdown("**Barras Agrupadas (2 níveis)**")
                st.plotly_chart(px.bar(group, x=col1, y='total', color=col2,
                                       facet_col=col3, barmode='group', text='total'), use_container_width=True)

                st.markdown("**Sunburst**")
                st.plotly_chart(px.sunburst(group, path=[col1, col2, col3], values='total'), use_container_width=True)

                st.markdown("**Treemap**")
                st.plotly_chart(px.treemap(group, path=[col1, col2, col3], values='total'), use_container_width=True)

# Rodapé
img_path = "imgs/logo_ms_brasil.png"
img_base64 = image_to_base64(img_path)
footer = f"""
<style>
.footer {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #003366;  /* Azul escuro */
    padding: 10px 20px;
    font-size: 13px;
    color: white;  /* Texto branco */
    text-align: center;
    border-top: 1px solid #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
    width: 100%;
    box-sizing: border-box;
}}

.footer img {{
    height: 40px;
    margin-right: 15px;
}}

.stSidebar .footer {{
    left: 260px;
    width: calc(100% - 260px);
}}

.footer .footer-content {{
    display: inline-block;
    text-align: center;
}}

</style>

<div class="footer">
    <div class="footer-content">
        Secretaria de Atenção Primária à Saúde - SAPS<br>
        Coordenação Geral de Monitoramento, Avaliação e Inteligência Analítica - CGMAIA<br>
        Ministério da Saúde 2025 - Todos os direitos reservados.
    </div>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
