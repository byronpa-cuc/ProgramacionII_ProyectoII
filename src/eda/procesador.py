import pandas as pd
import numpy as np


class ProcesadorEDA:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def limpieza_datos(self) -> pd.DataFrame:
        """Realiza la limpieza básica de tipos de datos y manejo de nulos."""
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['home_score'] = pd.to_numeric(self.df['home_score'], errors='coerce').fillna(0).astype(int)
        self.df['away_score'] = pd.to_numeric(self.df['away_score'], errors='coerce').fillna(0).astype(int)
        print("Limpieza de datos completada.")
        return self.df

    def generar_columnas_derivadas(self) -> pd.DataFrame:
        """Crea las columnas obligatorias: año, total_goles, diferencia_goles y ganador."""
        self.df['anio'] = self.df['date'].dt.year
        self.df['total_goles'] = self.df['home_score'] + self.df['away_score']
        self.df['diferencia_goles'] = self.df['home_score'] - self.df['away_score']

        condiciones = [
            self.df['home_score'] > self.df['away_score'],
            self.df['home_score'] < self.df['away_score']
        ]
        opciones = ['Local', 'Visitante']
        self.df['ganador'] = np.select(condiciones, opciones, default='Empate')
        return self.df

    def resumen_descriptivo(self) -> pd.DataFrame:
        """Retorna las estadísticas descriptivas básicas de las columnas numéricas."""
        return self.df[['home_score', 'away_score', 'total_goles', 'diferencia_goles']].describe()

    def analizar_asimetria_y_curtosis(self) -> dict:
        """
        Mide la forma de la distribución de los goles.
        Asimetría > 0: Indica que la mayoría de partidos tienen pocos goles, con una cola hacia partidos muy goleadores.
        Curtosis: Mide el nivel de concentración de los datos alrededor de la media (presencia de extremos).
        """
        asimetria = self.df['total_goles'].skew()
        curtosis = self.df['total_goles'].kurt()

        return {
            "Asimetría (Skewness) de Goles": round(asimetria, 4),
            "Curtosis de Goles": round(curtosis, 4),
            "Interpretación": "Distribución asimétrica positiva (cola a la derecha), típica en deportes donde los marcadores abultados son poco frecuentes."
        }

    def detectar_partidos_atipicos_iqr(self) -> pd.DataFrame:
        """
        Detecta 'Outliers' o partidos con un volumen de goles anormalmente alto
        utilizando la regla del Rango Intercuartílico (IQR).
        """
        q1 = self.df['total_goles'].quantile(0.25)
        q3 = self.df['total_goles'].quantile(0.75)
        iqr = q3 - q1

        # Umbral superior para considerar un marcador como atípico u outlier
        umbral_superior = q3 + (1.5 * iqr)

        # Filtrar partidos que superen el umbral
        partidos_atipicos = self.df[self.df['total_goles'] > umbral_superior]

        print(f"Identificados {len(partidos_atipicos)} partidos con marcadores atípicos (goles > {umbral_superior}).")
        return partidos_atipicos.sort_values(by='total_goles', ascending=False)

    def obtener_top_goleadas_historicas(self, top_n: int = 5) -> pd.DataFrame:
        """Identifica los partidos con la mayor diferencia de goles absoluta en la historia."""
        self.df['dif_absoluta'] = self.df['diferencia_goles'].abs()
        top_goleadas = self.df.sort_values(by='dif_absoluta', ascending=False).head(top_n)
        return top_goleadas[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'total_goles']]

    def matriz_correlacion(self) -> pd.DataFrame:
        """Retorna la matriz de correlación de las variables numéricas clave."""
        columnas_numericas = self.df[['home_score', 'away_score', 'total_goles', 'diferencia_goles']]
        return columnas_numericas.corr()