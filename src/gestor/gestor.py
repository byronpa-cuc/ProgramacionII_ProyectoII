import pandas as pd

class GestorPartidos:
    def __init__(self, ruta_procesado: str = "../data/processed/partidos-limpios.csv"):
        # Carga el dataset ya limpio y procesado
        self._df = pd.read_csv(ruta_procesado)

    @property
    def df(self) -> pd.DataFrame:
        """Propiedad de solo lectura para exponer el DataFrame si es necesario."""
        return self._df.copy()

    def get_partido(self, idx: int) -> pd.Series:
        """Retorna un partido específico mediante su índice jerárquico o ID."""
        try:
            return self._df.iloc[idx]
        except IndexError:
            return pd.Series(dtype=object)

    def get_por_equipo(self, equipo: str) -> pd.DataFrame:
        """Filtra todos los partidos donde el equipo jugó como local o visitante."""
        return self._df[(self._df['home_team'] == equipo) | (self._df['away_team'] == equipo)]

    def get_por_anio(self, anio: int) -> pd.DataFrame:
        """Retorna los partidos jugados en una edición de mundial específica."""
        return self._df[self._df['anio'] == anio]

    def get_por_sede(self, pais: str) -> pd.DataFrame:
        """Retorna los partidos que se disputaron en un país sede específico."""
        return self._df[self._df['country'] == pais]

    def ventaja_local(self) -> dict:
        """Calcula estadísticas para evaluar el impacto de jugar en casa."""
        total_partidos = len(self._df)
        # Filtrar partidos donde NO se jugó en territorio neutral
        partidos_no_neutrales = self._df[self._df['neutral'] == False]

        victorias_local_casa = len(partidos_no_neutrales[partidos_no_neutrales['ganador'] == 'Local'])
        total_no_neutrales = len(partidos_no_neutrales)

        porcentaje_efectividad = (victorias_local_casa / total_no_neutrales) * 100 if total_no_neutrales > 0 else 0

        return {
            "total_partidos_historicos": total_partidos,
            "partidos_con_localia_real": total_no_neutrales,
            "victorias_del_organizador": victorias_local_casa,
            "porcentaje_victoria_sede": round(porcentaje_efectividad, 2)
        }