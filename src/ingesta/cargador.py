import os
import pandas as pd
from src.helpers.utilidades import Utilidades


class CargadorDatos:
    def __init__(self):
        # URL oficial del csv
        self.url_fuente = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"

        #Definicion de rutas
        self.ruta_raw = Utilidades.obtener_ruta_raiz("data/raw/partidos-mundial.csv")
        self.ruta_processed = Utilidades.obtener_ruta_raiz("data/processed/partidos-limpios.csv")

    def descargar_y_filtrar_raw(self) -> pd.DataFrame:
        """
        Intenta descargar el CSV completo desde GitHub y filtrarlo.
        Contingencia: Si falla la conexión o el enlace,
        intenta leer el archivo 'partidos-mundial.csv' guardado localmente.
        """
        try:
            print("Intentando descargar datos desde el repositorio de GitHub...")
            # Cargar datos desde la URL pública
            df_completo = pd.read_csv(self.url_fuente)

            # Filtrar únicamente los partidos de la Copa Mundial
            print("Filtrando partidos únicamente de la Copa Mundial de la FIFA...")
            df_mundial = df_completo[df_completo['tournament'] == 'FIFA World Cup'].copy()

            # Validar que el DataFrame descargado tenga las columnas obligatorias
            columnas_criticas = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament']
            Utilidades.validar_columnas_esenciales(df_mundial, columnas_criticas)

            # Crear directorio si no existe y guardar el respaldo local
            os.makedirs(os.path.dirname(self.ruta_raw), exist_ok=True)
            df_mundial.to_csv(self.ruta_raw, index=False)
            print(f"Archivo raw descargado y respaldado exitosamente en: {self.ruta_raw}")
            return df_mundial

        except Exception as e:
            print(f"Advertencia: No se pudo conectar al repositorio remoto ({e}).")
            print("Activando mecanismo de contingencia: Intentando cargar archivo local...")

            # Verificar si existe el respaldo local en data/raw/
            if os.path.exists(self.ruta_raw):
                df_mundial = pd.read_csv(self.ruta_raw)
                print(f"Contingencia exitosa: Datos cargados desde el almacenamiento local ({self.ruta_raw}).")
                return df_mundial
            else:
                raise FileNotFoundError(
                    f"Error crítico: No hay conexión a Internet y tampoco existe el archivo "
                    f"de respaldo en la ruta local: {self.ruta_raw}"
                )

    def guardar_procesado(self, df: pd.DataFrame):
        """Guarda el DataFrame final procesado en la carpeta processed."""
        os.makedirs(os.path.dirname(self.ruta_processed), exist_ok=True)
        df.to_csv(self.ruta_processed, index=False)
        print(f"Archivo procesado guardado exitosamente en: {self.ruta_processed}")