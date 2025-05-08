# Dynavis - Painel Interativo de Indicadores SAPS

**Dynavis** é um painel interativo desenvolvido com [Streamlit](https://streamlit.io/) para a visualização dinâmica de indicadores de cadastros da Atenção Primária à Saúde (APS). Ele permite carregar dados CSV, selecionar até 3 colunas de interesse e gerar automaticamente visualizações e tabelas personalizadas.

## Funcionalidades

- Upload de arquivos CSV com separador vírgula (`,`)
- Seleção de 1 a 3 colunas para análise
- Agrupamento e cálculo de totais e percentuais
- Geração automática de gráficos com base no tipo de dado:
  - Barras verticais e horizontais
  - Gráficos de pizza, treemap, sunburst
  - Séries temporais, boxplot, violin plot e heatmap
- Interface visual elegante com personalização via CSS
- Exportação dos dados agregados para CSV

## Requisitos

- Python 3.12 ou superior
- [Streamlit](https://streamlit.io/)
- Pandas, Numpy, Matplotlib, Seaborn
- Plotly, base64

Instale as dependências com:

```bash
pip install -r requirements.txt
````

### Exemplo do `requirements.txt`:

```text
streamlit
pandas
numpy
matplotlib
seaborn
plotly
```

## Como executar

1. Clone o repositório:

```bash
git clone https://github.com/galilasmb/dynavis.git
cd dynavis
```

2. Execute o painel:

```bash
streamlit run main.py
```

3. Acesse no navegador: `http://localhost:8501`

## Estrutura do Projeto

```
dynavis/
│
├── main.py               # Código principal do painel
├── imgs/                # Logos e imagens
│   ├── logo_gov.png
│   ├── logo_ms_brasil.png
│   └── icon.jpg
├── requirements.txt     # Dependências Python
└── README.md            # Este arquivo
```
