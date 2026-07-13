import os
import pandas as pd


class Utilidades:

    @staticmethod
    def validar_columnas_esenciales(df: pd.DataFrame, columnas_requeridas: list) -> bool:
        """
        Valida si un DataFrame contiene todas las columnas necesarias para el análisis.
        Devuelve True si es válido, o levanta un ValueError si falta alguna.
        """
        columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
        if columnas_faltantes:
            raise ValueError(f"Error de Ingesta: Faltan las siguientes columnas obligatorias: {columnas_faltantes}")
        return True

    @staticmethod
    def limpiar_y_estandarizar_texto(texto: str) -> str:
        """
        Elimina espacios en blanco innecesarios y estandariza nombres de equipos
        para evitar duplicados por errores de escritura (ej: " Colombia " -> "Colombia").
        """
        if pd.isna(texto) or not isinstance(texto, str):
            return ""
        return texto.strip().title()

    @staticmethod
    def obtener_ruta_raiz(sub_ruta: str = "") -> str:
        """
        Resuelve rutas de archivos de forma segura sin importar si el código se ejecuta
        desde main.py, un Notebook o el Dashboard de Streamlit.
        """
        # Encuentra la carpeta principal del proyecto
        ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        return os.path.join(ruta_base, sub_ruta)