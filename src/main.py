from src.ingesta.cargador import CargadorDatos
from src.eda.procesador import ProcesadorEDA
from src.gestor.gestor import GestorPartidos


def main():
    print("=== INICIANDO PIPELINE WORLD CUP INSIGHTS ===")

    # 1. Ingesta
    cargador = CargadorDatos()
    df_raw = cargador.descargar_y_filtrar_raw()

    # 2. Procesamiento EDA
    procesador = ProcesadorEDA(df_raw)
    procesador.limpieza_datos()
    df_procesado = procesador.generar_columnas_derivadas()

    # 3. Persistencia
    cargador.guardar_procesado(df_procesado)

    # 4. Pruebas de Consulta (Gestor)
    gestor = GestorPartidos()
    print("\n--- Probando Consultas del Gestor ---")
    print(f"Partidos totales cargados en gestor: {len(gestor.df)}")

    # Ejemplo de consulta analítica de ventaja local
    stats_localia = gestor.ventaja_local()
    print(f"¿El país sede gana más? Efectividad organizador: {stats_localia['porcentaje_victoria_sede']}%")


if __name__ == "__main__":
    main()