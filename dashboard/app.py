import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px

# Configuración del entorno para detectar el módulo 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gestor.gestor import GestorPartidos
from src.visualizacion.visualizador import Visualizador

# 1. Configuracion del page
st.set_page_config(
    page_title="World Cup Insights | Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la estética general
st.markdown("""
    <style>
    .main-title { font-size: 38px !important; font-weight: 700 !important; color: #8A1538; }
    .subtitle { font-size: 18px !important; color: #555555; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)


# 2. Carga de los datos
@st.cache_data
def inicializar_componentes():
    gestor = GestorPartidos()
    visualizador = Visualizador(gestor.df)
    return gestor, visualizador


gestor, visualizador = inicializar_componentes()
df_completo = gestor.df

# 3. Encabezado
st.markdown('<p class="main-title">🏆 World Cup Insights Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Análisis Exploratorio de Datos Avanzado (EDA) - Historial de la Copa Mundial de la FIFA</p>',
    unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# SECCIÓN DE MÉTRICAS GLOBALES (KPIs)
# ==========================================
# Calculamos datos generales para las tarjetas del tope
total_partidos = len(df_completo)
total_goles = df_completo['total_goles'].sum()
promedio_goles = df_completo['total_goles'].mean()
ediciones = df_completo['anio'].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="⚽ Total Goles Históricos", value=f"{total_goles:,}")
with kpi2:
    st.metric(label="🏃‍♂️ Partidos Disputados", value=total_partidos)
with kpi3:
    st.metric(label="📊 Promedio Goles/Partido", value=f"{promedio_goles:.2f}")
with kpi4:
    st.metric(label="📅 Ediciones Analizadas", value=ediciones)

st.markdown("---")

# ==========================================
# ESTRUCTURA DE PESTAÑAS (TABS)
# ==========================================
tab_analisis, tab_consultas = st.tabs(["📊 Análisis Histórico e Historias", "🔍 Buscador e Historial"])

# ------------------------------------------
# PESTAÑA 1: ANÁLISIS HISTÓRICO (HISTORIAS VISUALES)
# ------------------------------------------
with tab_analisis:
    st.header("Análisis de Tendencias e Historias de Datos")
    st.caption("Cada gráfico responde a una hipótesis clave sobre la evolución del torneo.")

    # Fila 1: Efecto Sede (Gráfico interactivo de Plotly)
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        fig_sede = visualizador.graficar_efecto_sede_plotly()
        st.plotly_chart(fig_sede, use_container_width=True)

    with col_der:
        st.subheader("💡 El Efecto de la Localía")
        st.write(
            "Tradicionalmente en el fútbol se habla de la ventaja de jugar en casa. "
            "Al aislar los partidos donde el organizador juega en su propio país (excluyendo sedes neutrales), "
            "descubrimos la verdad estadística."
        )
        stats = gestor.ventaja_local()
        st.info(
            f"**Datos clave encontrados:**\n"
            f"* Partidos bajo localía real: **{stats['partidos_con_localia_real']}**\n"
            f"* Victorias del organizador: **{stats['victorias_del_organizador']}**\n"
            f"* Efectividad en casa: **{stats['porcentaje_victoria_sede']}%**\n\n"
            f"Esto confirma que la ventaja de campo es un factor crítico en el éxito mundialista."
        )

    st.markdown("---")

    # Dentro de tab_analisis, abajo del todo puedes agregar:
    st.markdown("---")
    st.subheader("🧮 Estadística Avanzada del EDA")

    col_eda1, col_eda2 = st.columns(2)

    with col_eda1:
        st.markdown("**Forma de la Distribución de Goles**")
        # Instanciamos el procesador temporalmente usando los datos del gestor
        from src.eda.procesador import ProcesadorEDA

        proc = ProcesadorEDA(df_completo)

        forma = proc.analizar_asimetria_y_curtosis()
        st.json(forma)

    with col_eda2:
        st.markdown("**Top 3 Partidos Atípicos (Outliers Estadísticos)**")
        outliers = proc.detectar_partidos_atipicos_iqr().head(3)
        for idx, row in outliers.iterrows():
            st.error(
                f"🚨 **{row['home_team']} {row['home_score']} - {row['away_score']} {row['away_team']}** ({row['anio']}) — Total Goles: {row['total_goles']}")

    # Fila 2: Tendencias de Goles y Potencias
    st.subheader("Evolución del Juego y Selección de Élite")
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.markdown("**¿Se anotan más o menos goles ahora?**")
        # Generamos la figura interactiva de evolución de goles usando un line chart rápido de Plotly
        goles_edicion = df_completo.groupby('anio')['total_goles'].mean().reset_index()
        fig_goles = px.line(
            goles_edicion, x='anio', y='total_goles',
            markers=True, title="Promedio de Goles por Partido a lo Largo del Tiempo",
            labels={'anio': 'Año del Mundial', 'total_goles': 'Promedio de Goles'}
        )
        fig_goles.update_traces(line_color='#8A1538')
        st.plotly_chart(fig_goles, use_container_width=True)

    with col_graf2:
        st.markdown("**Diferencia de Goles Histórica Acumulada**")
        # Reutilizamos la lógica del Top N Potencias en formato interactivo rápido
        g_locales = df_completo.groupby('home_team').agg(favor=('home_score', 'sum'), contra=('away_score', 'sum'))
        g_visitantes = df_completo.groupby('away_team').agg(favor=('away_score', 'sum'), contra=('home_score', 'sum'))
        historico = g_locales.add(g_visitantes, fill_value=0)
        historico['diferencia'] = historico['favor'] - historico['contra']
        top_10 = historico.sort_values(by='diferencia', ascending=False).head(10).reset_index()

        fig_potencias = px.bar(
            top_10, x='diferencia', y='home_team', orientation='h',
            title="Top 10 Selecciones con Mejor Rendimiento Goleador Neto",
            labels={'diferencia': 'Diferencia de Goles', 'home_team': 'Selección'},
            color='diferencia', color_continuous_scale='Bluered_r'
        )
        fig_potencias.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_potencias, use_container_width=True)

# ------------------------------------------
# PESTAÑA 2: BUSCADOR E HISTORIAL (GESTIÓN DE CONSULTAS)
# ------------------------------------------
with tab_consultas:
    st.header("Módulo de Consultas Personalizadas")
    st.caption("Filtre la base de datos procesada según los criterios del sistema.")

    filtro_tipo = st.radio("Seleccione el método de búsqueda:",
                           ["Por Selección", "Por Año de Edición", "Por País Sede"])

    if filtro_tipo == "Por Selección":
        lista_equipos = sorted(list(set(df_completo['home_team'].unique()) | set(df_completo['away_team'].unique())))
        equipo = st.selectbox("Elija un equipo nacional:", lista_equipos)
        resultado = gestor.get_por_equipo(equipo)
        st.subheader(f"Historial de Partidos de {equipo}")
        st.dataframe(resultado, use_container_width=True)

    elif filtro_tipo == "Por Año de Edición":
        lista_anios = sorted(list(df_completo['anio'].unique()), reverse=True)
        anio = st.selectbox("Elija el año del Mundial:", lista_anios)
        resultado = gestor.get_por_anio(anio)
        st.subheader(f"Partidos Disputados en el Mundial de {anio}")
        st.dataframe(resultado, use_container_width=True)

    elif filtro_tipo == "Por País Sede":
        lista_sedes = sorted(list(df_completo['country'].unique()))
        sede = st.selectbox("Elija el país organizador:", lista_sedes)
        resultado = gestor.get_por_sede(sede)
        st.subheader(f"Partidos Celebrados en la Sede: {sede}")
        st.dataframe(resultado, use_container_width=True)