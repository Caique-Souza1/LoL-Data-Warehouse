# Data Warehouse - League of Legends

Projeto desenvolvido para a disciplina de Sistemas de Apoio a Decisão, utilizando dados de partidas ranqueadas do League of Legends.

O objetivo do projeto foi realizar um processo completo de ETL com Python e Pandas, organizando os dados em um modelo dimensional (Star Schema) com tabelas fato e dimensões, além da criação de um dashboard analítico utilizando Streamlit.


## Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- Plotly


## Estrutura do projeto

### Arquivos presentes inicialmente

```text
dados/
├── Challenger_Ranked_Games.csv
├── Grandmaster_Ranked_Games.csv
└── Master_Ranked_Games.csv

etl.py
app.py
requirements.txt
README.md
```

### Arquivos gerados após executar o ETL

```text
dados/
├── dim_elo.csv
├── dim_game.csv
├── dim_team.csv
└── fato_partida.csv
```


## Modelo dimensional

### Dimensões

- `dim_elo`
- `dim_game`
- `dim_team`

### Tabela fato

- `fato_partida`

A tabela fato foi modelada com granularidade por time em cada partida, ou seja:

- 1 registro para o time blue
- 1 registro para o time red


## Funcionalidades

- Processo ETL completo
- Tratamento e normalização dos dados
- Criação de tabelas dimensão e fato
- Cálculo de métricas como KDA
- Dashboard interativo com filtros OLAP
- Visualização de métricas por elo
- Análise de objetivos:
  - Dragões
  - Barões
  - Torres
  - First Blood
- Tabelas analíticas dinâmicas


## Instalação

Clone o repositório:

```bash
git clone https://github.com/Caique-Souza1/LoL-Data-Warehouse.git
cd LoL-Data-Warehouse
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```


## Executando o ETL

```bash
python etl.py
```

O script irá:

- Extrair os dados dos CSVs originais
- Transformar os dados
- Gerar as dimensões
- Gerar a tabela fato normalizada

Após executar o ETL, os arquivos de dimensão e fato serão criados automaticamente na pasta `dados/`.


## Executando o dashboard

```bash
streamlit run app.py
```


## Dataset utilizado

Dataset disponível no Kaggle:

- https://www.kaggle.com/datasets/gyejr95/league-of-legends-challenger-ranked-games2020?resource=download

Créditos ao criador do dataset no Kaggle.


## Preview do dashboard

O dashboard contém:

- KPIs gerais
- Gráficos interativos
- Filtros por elo e time
- Visualizações OLAP
- Dados detalhados das partidas


## Autor

Projeto acadêmico desenvolvido por Caique Souza.
