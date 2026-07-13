import os
import pandas as pd


class CargadorDatos:
    def __init__(self):
        # URL oficial provista en los requerimientos
        self.url_fuente = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
        self.ruta_raw = "../data/raw/partidos-mundial.csv"
        self.ruta_processed = "../data/processed/partidos-limpios.csv"

    def descargar_y_filtrar_raw(self) -> pd.DataFrame:
        """Se descarga el CSV completo, filtra por 'FIFA World Cup' y lo guarda en raw."""
        print("Descargando datos desde el repositorio de GitHub...")
        # Cargar datos desde la URL pública
        df_completo = pd.read_csv(self.url_fuente)

        # Filtrar únicamente los partidos de la Copa Mundial
        print("Filtrando partidos únicamente de la Copa Mundial de la FIFA...")
        df_mundial = df_completo[df_completo['tournament'] == 'FIFA World Cup'].copy()

        # Se valida si existe el directorio
        os.makedirs(os.path.dirname(self.ruta_raw), exist_ok=True)

        # Guardar el set filtrado en la ruta especificada
        df_mundial.to_csv(self.ruta_raw, index=False)
        print(f"Archivo raw guardado exitosamente en: {self.ruta_raw}")
        return df_mundial

    def guardar_procesado(self, df: pd.DataFrame):
        """Guarda el DataFrame final procesado (con columnas derivadas) en la carpeta processed."""
        os.makedirs(os.path.dirname(self.ruta_processed), exist_ok=True)
        df.to_csv(self.ruta_processed, index=False)
        print(f"Archivo procesado guardado exitosamente en: {self.ruta_processed}")