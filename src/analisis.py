import pandas as pd
import os
import zipfile
from io import TextIOWrapper

def process_dataframe(df, nombre_archivo):
    df['FECHA_HORA_COMPLETA'] = pd.to_datetime(
        df['FECHA'] + ' ' + df['HORA'].astype(str) + ':' + df['MINUTOS'].astype(str) + ':' + df['SEGUNDOS'].astype(str),
        format='%d/%m/%Y %H:%M:%S'
    )
    columnas_clave = ['NROTARJETAEXTERNO', 'IDARCHIVOINTERCAMBIO', 'ID_POSICIONAMIENTO', 'FECHA_HORA_COMPLETA']
    df['CANTIDAD_REPETICIONES'] = df.groupby(columnas_clave)['FECHA_HORA_COMPLETA'].transform('count')
    duplicados_exactos = df[df['CANTIDAD_REPETICIONES'] > 1]
    df.sort_values(['NROTARJETAEXTERNO', 'FECHA_HORA_COMPLETA'], inplace=True)
    df['DIFERENCIA_SEGUNDOS'] = df.groupby(['NROTARJETAEXTERNO'])['FECHA_HORA_COMPLETA'].diff().dt.total_seconds()
    variaciones_pequenas = df[df['DIFERENCIA_SEGUNDOS'].between(0, 3, inclusive='right')]
    
    informe = [
        "=" * 70,
        f"Archivo analizado: {nombre_archivo}",
        "=" * 70,
        f"Total de registros analizados: {len(df)}",
        f"Duplicados exactos encontrados: {len(duplicados_exactos)}",
        f"Casos con diferencias de ≤ 3 segundos: {len(variaciones_pequenas)}",
        f"Aclaración: \"Casos con diferencias de ≤ 3 segundos\" hace referencia a transacciones de una misma tarjeta en las que la diferencia entre los tiempos registrados es menor o igual a 3 segundos. Esto podría representar casos correctos, como por ejemplo acompañantes que utilizan la misma tarjeta, o inconsistencias en el sistema, como errores de procesamiento o duplicaciones no esperadas.\n"
    ]
    return "\n".join(informe)

def analizar_csv(ruta_csv):
    try:
        df = pd.read_csv(ruta_csv, sep=";", encoding="latin1")
        nombre_archivo = os.path.splitext(os.path.basename(ruta_csv))[0]
        return process_dataframe(df, nombre_archivo)
    except Exception as e:
        raise ValueError(f"Error al analizar el archivo CSV {ruta_csv}: {str(e)}")

def analizar_gzip(ruta_gz):
    try:
        df = pd.read_csv(ruta_gz, sep=";", encoding="latin1", compression='gzip')
        nombre_archivo = os.path.splitext(os.path.basename(ruta_gz))[0]
        return process_dataframe(df, nombre_archivo)
    except Exception as e:
        raise ValueError(f"Error al analizar el archivo GZip {ruta_gz}: {str(e)}")

def analizar_csv_stream(stream, nombre_archivo):
    try:
        df = pd.read_csv(stream, sep=";", encoding="latin1")
        return process_dataframe(df, nombre_archivo)
    except Exception as e:
        raise ValueError(f"Error al analizar el stream de {nombre_archivo}: {str(e)}")

def analizar_archivos(lista_rutas):
    informes = []
    for ruta in lista_rutas:
        ext = os.path.splitext(ruta)[1].lower()
        try:
            if ext == ".csv":
                informe = analizar_csv(ruta)
                informes.append(informe)
            elif ext == ".gz":
                informe = analizar_gzip(ruta)
                informes.append(informe)
            elif ext == ".zip":
                with zipfile.ZipFile(ruta, "r") as z:
                    for fileinfo in z.infolist():
                        if fileinfo.filename.lower().endswith(".csv"):
                            with z.open(fileinfo) as f:
                                stream = TextIOWrapper(f, encoding="latin1")
                                informe = analizar_csv_stream(stream, fileinfo.filename)
                                informes.append(informe)
            else:
                informes.append(f"Tipo de archivo no soportado: {ruta}")
        except Exception as e:
            informes.append(f"Error al analizar {ruta}: {str(e)}")
    # Combinar los informes, separándolos con líneas divisorias
    informe_completo = "\n\n" + ("-" * 70 + "\n\n").join(informes)
    return informe_completo
