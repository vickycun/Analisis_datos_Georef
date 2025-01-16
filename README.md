# Análisis de Datos Georeferenciales (AnalisisArchivosNNSA)

Este proyecto permite analizar archivos CSV con datos de tarjetas SUBE, detectando duplicados y patrones inconsistentes en las transacciones.

## **Características**
- Análisis de duplicados exactos y transacciones con diferencias menores o iguales a 3 segundos.
- Informe detallado de los resultados directamente en la interfaz gráfica.
- Descarga del informe en formato .txt.

## **Estructura del Proyecto**
analisisDatosNNSS/
├── main.py                # Archivo principal que ejecuta el programa
├── src/
│   ├── analisis.py        # Lógica de análisis
│   └── interfaz.py        # Configuración de la interfaz gráfica
├── assets/
│   └── icono.ico          # Ícono del programa
└── README.md              # Documentación del proyecto


##  **Cómo Iniciar la Aplicación**
### **Requisitos Previos**

    - **Python 3.8 o superior**

    - Ejecutar desde el Código Fuente
        Clonar el repositorio: git clone https://github.com/tuusuario/analisisDatosGeoreferencialesCSV.git

    - Activar el entorno virtual:
        source env/bin/activate   # En Linux/Mac
        env\Scripts\activate      # En Windows

    - Ejecutar el script principal: python main.py


## **Cómo usar el programa**
1. Seleccionar un archivo CSV
2. Analizar los datos
3. Descargar el informe


## **Generar el ejecutable**
Para crear un ejecutable con PyInstaller, usar el siguiente comando desde la raíz del proyecto:

`pyinstaller --onefile --name "AnalisisArchivosNNSA" --icon="assets/icono.ico" --add-data "assets/icono.ico;assets" --noconsole main.py`

El ejecutable se generará en la carpeta dist.


## **Licencia**  
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles