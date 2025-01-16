import pandas as pd
import os

def analizar_csv(ruta_csv):
    """
    Analiza un archivo CSV, detecta duplicados y pequeñas variaciones.
    Devuelve un informe como cadena de texto.
    """
    try:
        # Leer archivo CSV
        df = pd.read_csv(ruta_csv, sep=";", encoding="latin1")

        # Crear columna de fecha completa
        df['FECHA_HORA_COMPLETA'] = pd.to_datetime(
            df['FECHA'] + ' ' + df['HORA'].astype(str) + ':' + df['MINUTOS'].astype(str) + ':' + df['SEGUNDOS'].astype(str),
            format='%d/%m/%Y %H:%M:%S'
        )

        # Agrupar por claves principales
        columnas_clave = ['NROTARJETAEXTERNO', 'IDARCHIVOINTERCAMBIO', 'ID_POSICIONAMIENTO', 'FECHA_HORA_COMPLETA']
        df['CANTIDAD_REPETICIONES'] = df.groupby(columnas_clave)['FECHA_HORA_COMPLETA'].transform('count')

        # Detectar duplicados exactos
        duplicados_exactos = df[df['CANTIDAD_REPETICIONES'] > 1]

        # Detectar pequeñas variaciones
        df.sort_values(['NROTARJETAEXTERNO', 'FECHA_HORA_COMPLETA'], inplace=True)
        df['DIFERENCIA_SEGUNDOS'] = df.groupby(['NROTARJETAEXTERNO'])['FECHA_HORA_COMPLETA'].diff().dt.total_seconds()
        variaciones_pequenas = df[df['DIFERENCIA_SEGUNDOS'].between(0, 3, inclusive='right')]

        # Generar informe
        nombre_archivo = os.path.splitext(os.path.basename(ruta_csv))[0]
        informe = [
            f"Archivo analizado: {nombre_archivo}\n",
            "=" * 70,
            f"Total de registros analizados: {len(df)}",
            f"Duplicados exactos encontrados: {len(duplicados_exactos)}",
            f"Casos con diferencias de ≤ 3 segundos: {len(variaciones_pequenas)}",
            "\nAclaración: \"Casos con diferencias de ≤ 3 segundos\" hace referencia a transacciones de una misma tarjeta "
            "en las que la diferencia entre los tiempos registrados es menor o igual a 3 segundos. Esto podría representar "
            "casos correctos, como por ejemplo acompañantes que utilizan la misma tarjeta, o inconsistencias en el sistema, "
            "como por ejemplo errores de procesamiento o duplicaciones no esperadas."
        ]

        return "\n".join(informe)
    except Exception as e:
        raise ValueError(f"Error al analizar el archivo: {str(e)}")
