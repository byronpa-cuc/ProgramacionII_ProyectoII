import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px

# Configuración del entorno para detectar el módulo 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gestor.gestor import GestorPartidos
from src.visualizacion.visualizador import Visualizador

# 1. Configuración de la página
st.set_page_config(
    page_title="World Cup Insights | Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS personalizado para estética ejecutiva y limpia
st.markdown("""
    <style>
    .main-title { 
        font-size: 36px !important; 
        font-weight: 700 !important; 
        color: #8A1538; 
        margin-bottom: 0px;
    }
    .subtitle { 
        font-size: 16px !important; 
        color: #555555; 
        margin-bottom: 25px; 
    }
    div[data-testid="stMetric"] {
        background-color: #767676;
        border: 1px solid #E9ECEF;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px !important;
        color: #6C757D !important;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        color: #8A1538 !important;
    }
    </style>
""", unsafe_allow_html=True)


# 3. Carga y caching de componentes
@st.cache_data
def inicializar_componentes():
    gestor = GestorPartidos()
    visualizador = Visualizador(gestor.df)
    return gestor, visualizador


gestor, visualizador = inicializar_componentes()
df_completo = gestor.df

# 4. Encabezado Principal
st.markdown('<p class="main-title">World Cup Insights Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Análisis Exploratorio de Datos Avanzado (EDA) - Historial de la Copa Mundial de la FIFA</p>',
    unsafe_allow_html=True
)

# 5. Tarjetas de Métricas Clave (KPIs)
total_partidos = len(df_completo)
total_goles = df_completo['total_goles'].sum()
promedio_goles = df_completo['total_goles'].mean()
ediciones = df_completo['anio'].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="Total Goles Históricos", value=f"{total_goles:,}")
with kpi2:
    st.metric(label="Partidos Disputados", value=f"{total_partidos:,}")
with kpi3:
    st.metric(label="Promedio Goles / Partido", value=f"{promedio_goles:.2f}")
with kpi4:
    st.metric(label="Ediciones Analizadas", value=ediciones)

st.markdown("---")

# 6. Estructura de Pestañas
tab_analisis, tab_consultas = st.tabs(["Análisis Histórico e Historias", "Buscador e Historial"])


# ==========================================
# PESTAÑA 1: ANÁLISIS HISTÓRICO
# ==========================================
with tab_analisis:
    st.header("Análisis de Tendencias e Historias de Datos")
    st.caption("Evaluación visual de las hipótesis clave sobre el desempeño histórico del torneo.")

    # Seccion A: Efecto Sede
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        fig_sede = visualizador.graficar_efecto_sede_plotly()
        st.plotly_chart(fig_sede, use_container_width=True)

    with col_der:
        st.subheader("El Efecto de la Localía")
        st.write(
            "Al aislar los partidos donde el país organizador disputó encuentros en su propio territorio "
            "(excluyendo sedes neutrales), se evalúa el impacto real del apoyo local en los resultados."
        )
        stats = gestor.ventaja_local()
        st.info(
            f"**Resumen estadístico:**\n\n"
            f"- Partidos bajo localía real: **{stats['partidos_con_localia_real']}**\n"
            f"- Victorias del organizador: **{stats['victorias_del_organizador']}**\n"
            f"- Rendimiento en casa: **{stats['porcentaje_victoria_sede']}%**\n\n"
            f"Los datos confirman que disputar el torneo como anfitrión representa una ventaja competitiva cuantificable."
        )

    st.markdown("---")

    # Sección B: Top 10 Goleadores por Edición
    st.subheader("Top 10 Selecciones más Goleadoras por Edición")
    st.caption("Seleccione un año de torneo para evaluar la distribución ofensiva de esa cita mundialista.")

    df_mundiales = df_completo[df_completo['tournament'] == 'FIFA World Cup']
    lista_anios_mundial = sorted(df_mundiales['anio'].unique(), reverse=True)

    anio_seleccionado = st.selectbox(
        "Seleccione el Año del Mundial:",
        lista_anios_mundial,
        key="selector_goleadores_anio"
    )

    df_mundial_filtrado = df_mundiales[df_mundiales['anio'] == anio_seleccionado]

    goles_home = df_mundial_filtrado.groupby('home_team')['home_score'].sum().reset_index()
    goles_home.columns = ['team', 'goles']

    goles_away = df_mundial_filtrado.groupby('away_team')['away_score'].sum().reset_index()
    goles_away.columns = ['team', 'goles']

    goles_totales = pd.concat([goles_home, goles_away]).groupby('team')['goles'].sum().reset_index()
    top_10_goleadores = goles_totales.sort_values(by='goles', ascending=False).head(10)

    if not top_10_goleadores.empty and top_10_goleadores['goles'].sum() > 0:
        fig_goleadores = px.bar(
            top_10_goleadores,
            x='goles',
            y='team',
            orientation='h',
            title=f"Máximos Anotadores - Copa Mundial {anio_seleccionado}",
            labels={'goles': 'Goles Anotados', 'team': 'Selección'},
            color='goles',
            color_continuous_scale='burg'
        )
        fig_goleadores.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_goleadores, use_container_width=True)
    else:
        st.warning(f"No se registraron datos de anotaciones para la edición de {anio_seleccionado}.")

    st.markdown("---")

    # Sección C: Evolución y Potencias
    st.subheader("Evolución del Juego y Rendimiento Histórico")
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.markdown("**Evolución del Promedio de Goles**")
        goles_edicion = df_completo.groupby('anio')['total_goles'].mean().reset_index()
        fig_goles = px.line(
            goles_edicion, x='anio', y='total_goles',
            markers=True, title="Promedio de Goles por Partido (1930 - Presente)",
            labels={'anio': 'Año', 'total_goles': 'Promedio de Goles'}
        )
        fig_goles.update_traces(line_color='#8A1538')
        st.plotly_chart(fig_goles, use_container_width=True)

    with col_graf2:
        st.markdown("**Diferencia de Goles Acumulada**")
        g_locales = df_completo.groupby('home_team').agg(favor=('home_score', 'sum'), contra=('away_score', 'sum'))
        g_visitantes = df_completo.groupby('away_team').agg(favor=('away_score', 'sum'), contra=('home_score', 'sum'))
        historico = g_locales.add(g_visitantes, fill_value=0)
        historico['diferencia'] = historico['favor'] - historico['contra']
        top_10_diferencia = historico.sort_values(by='diferencia', ascending=False).head(10).reset_index()

        fig_potencias = px.bar(
            top_10_diferencia, x='diferencia', y='home_team', orientation='h',
            title="Top 10 Selecciones por Balance Goleador Neto",
            labels={'diferencia': 'Diferencia de Goles', 'home_team': 'Selección'},
            color='diferencia', color_continuous_scale='Bluered_r'
        )
        fig_potencias.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_potencias, use_container_width=True)

    st.markdown("---")

    # Sección D: Métrica Técnica EDA
    st.subheader("Métricas de Distribución Avanzada (EDA)")
    col_eda1, col_eda2 = st.columns(2)

    with col_eda1:
        st.markdown("**Forma de la Distribución de Goles**")
        from src.eda.procesador import ProcesadorEDA
        proc = ProcesadorEDA(df_completo)
        forma = proc.analizar_asimetria_y_curtosis()
        st.json(forma)

    with col_eda2:
        st.markdown("**Registros Atípicos Identificados (IQR)**")
        outliers = proc.detectar_partidos_atipicos_iqr().head(3)
        for idx, row in outliers.iterrows():
            st.error(
                f"**{row['home_team']} {row['home_score']} - {row['away_score']} {row['away_team']}** "
                f"({row['anio']}) — Total Goles: {row['total_goles']}"
            )


# ==========================================
# PESTAÑA 2: BUSCADOR E HISTORIAL
# ==========================================
with tab_consultas:
    st.header("Módulo de Consultas Personalizadas")
    st.caption("Filtre la base de datos procesada según los criterios seleccionados.")

    filtro_tipo = st.radio(
        "Seleccione el método de búsqueda:",
        ["Por Selección", "Por Año de Edición", "Por País Sede"]
    )

    if filtro_tipo == "Por Selección":
        home_teams = set(df_completo['home_team'].dropna().unique())
        away_teams = set(df_completo['away_team'].dropna().unique())
        lista_equipos = sorted(list(home_teams | away_teams))

        equipo = st.selectbox("Elija una selección:", lista_equipos)
        resultado = gestor.get_por_equipo(equipo)
        st.subheader(f"Historial de Partidos de {equipo}")
        st.dataframe(resultado, use_container_width=True)

    elif filtro_tipo == "Por Año de Edición":
        lista_anios = sorted(list(df_completo['anio'].dropna().unique()), reverse=True)
        anio = st.selectbox("Elija el año del Mundial:", lista_anios)
        resultado = gestor.get_por_anio(anio)
        st.subheader(f"Partidos Disputados en la Edición {anio}")
        st.dataframe(resultado, use_container_width=True)

    elif filtro_tipo == "Por País Sede":
        lista_sedes = sorted(list(df_completo['country'].dropna().unique()))
        sede = st.selectbox("Elija el país organizador:", lista_sedes)
        resultado = gestor.get_por_sede(sede)
        st.subheader(f"Partidos Celebrados en la Sede: {sede}")
        st.dataframe(resultado, use_container_width=True)