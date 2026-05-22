import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Dashboard League of Legends",
    layout="wide"
)

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0f1117;
        color: #f3f4f6;
    }

    section[data-testid="stSidebar"] {
        background-color: #161a23;
        border-right: 1px solid #2b2f3a;
    }

    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #f9fafb;
        margin-bottom: 0;
    }

    .subtitle {
        color: #9ca3af;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: #1a1f2b;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #2d3748;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.35);
    }

    .metric-title {
        font-size: 0.9rem;
        color: #9ca3af;
        margin-bottom: .3rem;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #f9fafb;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)

cores_elo = {
    "Master": "#6d28d9",
    "Grandmaster": "#b91c1c",
    "Challenger": "#22d3ee"
}

@st.cache_data
def carregar_dados():

    dim_elo = pd.read_csv("dados/dim_elo.csv")
    dim_game = pd.read_csv("dados/dim_game.csv")
    dim_team = pd.read_csv("dados/dim_team.csv")
    fato_partida = pd.read_csv("dados/fato_partida.csv")

    df = fato_partida.merge(dim_elo, on="elo_id", how="left")
    df = df.merge(dim_team, on="team_id", how="left")
    df = df.merge(dim_game, on="id_game", how="left")

    return df


def metric_card(titulo, valor):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{titulo}</div>
            <div class="metric-value">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def estilizar_figura(fig):

    fig.update_layout(
        paper_bgcolor="#1a1f2b",
        plot_bgcolor="#1a1f2b",
        font=dict(color="#f3f4f6"),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            bgcolor="#1a1f2b",
            bordercolor="#2d3748"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        color="#f3f4f6"
    )

    fig.update_yaxes(
        gridcolor="#2d3748",
        color="#f3f4f6"
    )

    return fig


df = carregar_dados()

# Sidebar

st.sidebar.title("Filtros")

elos = sorted(df["elo_name"].unique())

elo_selecionado = st.sidebar.multiselect(
    "Elo",
    elos,
    default=elos
)

times = sorted(df["team_name"].unique())

time_selecionado = st.sidebar.multiselect(
    "Time",
    times,
    default=times
)

df_filtrado = df[
    (df["elo_name"].isin(elo_selecionado)) &
    (df["team_name"].isin(time_selecionado))
]

# Título

st.markdown(
    '<div class="main-title">Dashboard League of Legends</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Análise OLAP de partidas ranqueadas.</div>',
    unsafe_allow_html=True
)

# Métricas

media_kda = round(df_filtrado["kda"].mean(), 2)
media_gold = int(df_filtrado["gold"].mean())
media_damage = int(df_filtrado["damage"].mean())
partidas = df_filtrado["id_game"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Partidas", partidas)

with col2:
    metric_card("KDA Médio", media_kda)

with col3:
    metric_card("Gold Médio", f"{media_gold:,}")

with col4:
    metric_card("Dano Médio", f"{media_damage:,}")

# Gráficos

col_esquerda, col_direita = st.columns(2)

with col_esquerda:

    st.subheader("Vitórias por Elo")

    wins_elo = (
        df_filtrado.groupby("elo_name")["wins"]
        .sum()
        .reset_index()
    )

    fig_wins = px.bar(
        wins_elo,
        x="elo_name",
        y="wins",
        color="elo_name",
        color_discrete_map=cores_elo
    )

    fig_wins.update_traces(
        marker_line_color="#d4af37",
        marker_line_width=2
    )

    st.plotly_chart(
        estilizar_figura(fig_wins),
        width="stretch"
    )

with col_direita:

    st.subheader("KDA Médio por Elo")

    kda_elo = (
        df_filtrado.groupby("elo_name")["kda"]
        .mean()
        .reset_index()
    )

    fig_kda = px.bar(
        kda_elo,
        x="elo_name",
        y="kda",
        color="elo_name",
        color_discrete_map=cores_elo
    )

    fig_kda.update_traces(
        marker_line_color="#d4af37",
        marker_line_width=2
    )

    st.plotly_chart(
        estilizar_figura(fig_kda),
        width="stretch"
    )

# Objetivos

col_obj1, col_obj2 = st.columns(2)

with col_obj1:

    st.subheader("Dragões por Elo")

    dragon = (
        df_filtrado.groupby("elo_name")["dragon_kills"]
        .mean()
        .reset_index()
    )

    fig_dragon = px.line(
        dragon,
        x="elo_name",
        y="dragon_kills",
        markers=True,
        color_discrete_sequence=["#d4af37"]
    )

    fig_dragon.update_traces(
        line_width=4,
        marker_size=10
    )

    st.plotly_chart(
        estilizar_figura(fig_dragon),
        width="stretch"
    )

with col_obj2:

    st.subheader("Torres por Elo")

    torres = (
        df_filtrado.groupby("elo_name")["tower_kills"]
        .mean()
        .reset_index()
    )

    fig_tower = px.line(
        torres,
        x="elo_name",
        y="tower_kills",
        markers=True,
        color_discrete_sequence=["#facc15"]
    )

    fig_tower.update_traces(
        line_width=4,
        marker_size=10
    )

    st.plotly_chart(
        estilizar_figura(fig_tower),
        width="stretch"
    )

# OLAP

st.subheader("Tabela OLAP")

dimensao = st.selectbox(
    "Dimensão",
    [
        "elo_name",
        "team_name"
    ]
)

medida = st.selectbox(
    "Métrica",
    [
        "kills",
        "deaths",
        "assists",
        "kda",
        "gold",
        "damage",
        "wins",
        "first_blood",
        "first_tower",
        "first_baron",
        "first_dragon",
        "dragon_kills",
        "baron_kills",
        "tower_kills"
    ]
)

if medida in [
    "wins",
    "first_blood",
    "first_tower",
    "first_baron",
    "first_dragon"
]:

    tabela_olap = (
        df_filtrado.groupby(dimensao)[medida]
        .sum()
        .reset_index()
        .sort_values(medida, ascending=False)
    )

else:

    tabela_olap = (
        df_filtrado.groupby(dimensao)[medida]
        .mean()
        .reset_index()
        .sort_values(medida, ascending=False)
    )

st.dataframe(
    tabela_olap,
    width="stretch",
    hide_index=True
)

# Dados detalhados

with st.expander("Dados detalhados"):

    st.dataframe(
        df_filtrado,
        width="stretch",
        hide_index=True
    )