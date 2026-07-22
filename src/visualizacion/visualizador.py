import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


class Visualizador:
    def __init__(self, df: pd.DataFrame):
        """Recibe el DataFrame ya procesado con las columnas derivadas."""
        self.df = df.copy()
        # Configuración estética global para los gráficos estáticos de Seaborn
        sns.set_theme(style="whitegrid")
        plt.rcParams["figure.figsize"] = (10, 6)

    def graficar_goles_por_edicion(self, guardar_ruta: str = None):
        """
        Historia: ¿En qué Mundiales se ha visto el fútbol más ofensivo?
        Muestra la evolución del promedio de goles por partido a lo largo de los años.
        """
        # Agrupar por año y calcular el promedio de la columna derivada 'total_goles'
        goles_edicion = self.df.groupby('anio')['total_goles'].mean().reset_index()

        plt.figure()
        sns.lineplot(data=goles_edicion, x='anio', y='total_goles', marker='o', color='purple', linewidth=2.5)

        plt.title("Promedio de Goles por Partido en la Historia de los Mundiales", fontsize=14, fontweight='bold')
        plt.xlabel("Año del Mundial", fontsize=12)
        plt.ylabel("Promedio de Goles", fontsize=12)

        if guardar_ruta:
            plt.savefig(guardar_ruta, bbox_inches='tight')
        plt.show()

    def graficar_mejor_diferencia_goles(self, top_n: int = 10):
        """
                Historia: ¿Cuáles son las verdaderas potencias históricas de los Mundiales?
                Muestra el Top N de selecciones con mejor diferencia de goles histórica acumulada.
                """
        goles_locales = self.df.groupby('home_team').agg(favor=('home_score', 'sum'), contra=('away_score', 'sum'))
        goles_visitantes = self.df.groupby('away_team').agg(favor=('away_score', 'sum'), contra=('home_score', 'sum'))

        historico_equipos = goles_locales.add(goles_visitantes, fill_value=0)
        historico_equipos['diferencia'] = historico_equipos['favor'] - historico_equipos['contra']

        top_potencias = historico_equipos.sort_values(by='diferencia', ascending=False).head(top_n).reset_index()

        plt.figure()

        sns.barplot(
            data=top_potencias,
            x='diferencia',
            y='home_team',
            hue='home_team',  # Asignamos la variable 'y' a 'hue'
            legend=False,  # Desactivamos la leyenda automática
            palette='viridis'
        )

        plt.title(f"Top {top_n} Selecciones con Mejor Diferencia de Goles Histórica", fontsize=14, fontweight='bold')
        plt.xlabel("Diferencia de Goles Acumulada", fontsize=12)
        plt.ylabel("Selección", fontsize=12)
        plt.show()

    def graficar_efecto_sede_plotly(self) -> go.Figure:
        """
        Historia: ¿El país sede realmente gana más? (Interactivo con Plotly)
        Compara los resultados de partidos donde el organizador juega en su propia casa (neutral = False).
        """
        # Filtrar partidos no neutrales (donde el equipo local es realmente el dueño de la casa)
        partidos_casa = self.df[self.df['neutral'] == False]

        # Contar la distribución de la columna derivada 'ganador'
        distribucion_ganadores = partidos_casa['ganador'].value_counts().reset_index()
        distribucion_ganadores.columns = ['Resultado', 'Cantidad']

        # Mapear colores temáticos
        colores = {'Local': '#2ca02c', 'Visitante': '#d62728', 'Empate': '#7f7f7f'}

        fig = px.pie(
            distribucion_ganadores,
            values='Cantidad',
            names='Resultado',
            title="Distribución de Resultados cuando el Equipo Local Juega en Casa",
            color='Resultado',
            color_discrete_map=colores,
            hole=0.4
        )

        fig.update_traces(textinfo='percent+label', pull=[0.1, 0, 0])
        return fig