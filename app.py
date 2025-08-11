import streamlit as st
import pandas as pd
import plotly.express as px
from bubbly.bubbly import bubbleplot

df = px.data.gapminder()

#st.set_page_config(layout="wide", page_title="Dashboard Gapminder")


st.title("🌍 Dashboard Gapminder – Streamlit + Plotly")


st.sidebar.header("Filtros")
anos = sorted(df["year"].unique())
ano_selecionado = st.sidebar.slider("Ano", min_value=min(anos), 
                                    max_value=max(anos), 
                                    value=2007, step=5)

continentes = df["continent"].unique().tolist()
continente_selecionado = st.sidebar.multiselect("Continente", continentes, default=continentes)

paises = df['country'].unique().tolist()
pais_selecionado = st.sidebar.multiselect("País", paises, default=["Brazil", "Bolivia"])
df_pais_filtrado = df[df['country'].isin(pais_selecionado)]

df_agrupado_continentes = df.groupby(['continent', 'year']).mean(numeric_only=True).reset_index()

df_filtrado = df[(df["year"] == ano_selecionado) & (df["continent"].isin(continente_selecionado))]

col1, col2 = st.columns(2)

with col1:
    st.subheader("PIB per capita vs Expectativa de Vida")
    fig_disp = px.scatter(
        df_filtrado,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
        labels={"gdpPercap": "PIB per Capita", "lifeExp": "Expectativa de Vida"},
        title=f"Dispersão por país – {ano_selecionado}"
    )
    st.plotly_chart(fig_disp, use_container_width=True)


with col2:
    st.subheader("🗺 Mapa: Expectativa de Vida")
    fig_mapa = px.choropleth(
        df_filtrado,
        locations="iso_alpha",
        color="lifeExp",
        hover_name="country",
        color_continuous_scale="Viridis",
        labels={"lifeExp": "Expectativa de Vida"},
        title=f"Expectativa de Vida por País – {ano_selecionado}"
    )
    st.plotly_chart(fig_mapa, use_container_width=True)
    
# col3, col4 = st.columns(2)
# with col3:
st.subheader("A desigualdade do PIB per capita entre regiões geográficas está aumentando ao longo do tempo")
fig_desig = px.scatter(
    df_agrupado_continentes,
    x="year",
    y="gdpPercap",
    size="pop",
    color="continent",
    hover_name="continent",
    # log_x=True,
    size_max=60,
    labels={"gdpPercap": "PIB per Capita", "year": "Ano"},
    title=f"Dispersão por país – {ano_selecionado}"
)
st.plotly_chart(fig_desig, use_container_width=True)
    
# with col4:
st.subheader("PIB per capita e expectativa de vida ao longo do tempo")
fig_expect_tempo = px.scatter(
    df_pais_filtrado,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="year",
    hover_name="country",
    size_max=60,
    color_continuous_scale="Viridis",
    labels={"country": "País", "lifeExp": "Expectativa de Vida", "gdpPercap": "PIB per Capita"},
    title=f"Países Selecionados – {', '.join(pais_selecionado)}"
)
st.plotly_chart(fig_expect_tempo, use_container_width=True)

st.subheader("PIB per capita e expectativa de vida por continente ao longo do tempo")
fig_pib_continent = px.scatter(
    df_filtrado,
    x='gdpPercap',
    y='lifeExp',
    color='continent',
    size='pop',
    size_max=60,
    hover_name="country",
    facet_col = "continent",
    labels={"continent": "Continente", "lifeExp": "Expectativa de Vida", "gdpPercap": "PIB per Capita"},
    title=f"Ano – {ano_selecionado}",
    log_x=True)
st.plotly_chart(fig_pib_continent, use_container_width=True)

# Tabela com os dados
st.markdown("### 📋 Tabela de Dados Filtrados")
st.dataframe(df_filtrado.reset_index(drop=True))