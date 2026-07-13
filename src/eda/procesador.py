import pandas as pd
import numpy as np


class ProcesadorEDA:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def limpieza_datos(self) -> pd.DataFrame:
        """Realiza la limpieza básica de tipos de datos y manejo de nulos."""
        # Se convierte la columna de fecha a tipo datetime
        self.df['date'] = pd.to_datetime(self.df['date'])

        # Se convierten los marcadores a numéricos y eliminar nulos si existieran
        self.df['home_score'] = pd.to_numeric(self.df['home_score'], errors='coerce').fillna(0).astype(int)
        self.df['away_score'] = pd.to_numeric(self.df['away_score'], errors='coerce').fillna(0).astype(int)

        print("Limpieza de datos completada.")
        return self.df

    def generar_columnas_derivadas(self) -> pd.DataFrame:
        """Crea las columnas obligatorias: año, total_goles, diferencia_goles y ganador."""
        # 1. Año derivado de la fecha
        self.df['anio'] = self.df['date'].dt.year

        # 2. Total de goles en el partido
        self.df['total_goles'] = self.df['home_score'] + self.df['away_score']

        # 3. Diferencia de goles (Local - Visitante)
        self.df['diferencia_goles'] = self.df['home_score'] - self.df['away_score']

        # 4. Determinar el ganador (Local / Visitante / Empate)
        condiciones = [
            self.df['home_score'] > self.df['away_score'],
            self.df['home_score'] < self.df['away_score']
        ]
        opciones = ['Local', 'Visitante']
        self.df['ganador'] = np.select(condiciones, opciones, default='Empate')

        print("Columnas derivadas agregadas exitosamente.")
        return self.df

    def resumen_descriptivo(self) -> pd.DataFrame:
        """Retorna las estadísticas descriptivas de las columnas numéricas."""
        return self.df.describe()

    def matriz_correlacion(self) -> pd.DataFrame:
        """Retorna la matriz de correlación de las variables numéricas."""
        columnas_numericas = self.df.select_dtypes(include=[np.number])
        return columnas_numericas.corr()