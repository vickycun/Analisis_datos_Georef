import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from src.analisis import analizar_archivos
from datetime import datetime

# Variables globales para almacenar la lista de archivos seleccionados y el informe generado
lista_rutas = []
informe = ""
ruta_informe = ""

def seleccionar_archivos(entry):
    global lista_rutas
    lista_rutas = filedialog.askopenfilenames(
        filetypes=[
            ("Todos los archivos", "*.*"),
            ("Archivos soportados", "*.csv *.zip *.gz"),
            ("Archivos CSV", "*.csv"),
            ("Archivos ZIP", "*.zip"),
            ("Archivos GZip", "*.gz")
        ]
    )
    if lista_rutas:
        entry.delete(0, "end")
        entry.insert(0, ", ".join(lista_rutas))

def analizar_archivos_interfaz(text_informe):
    global informe
    informe = ""
    try:
        informe = analizar_archivos(lista_rutas)
        text_informe.delete("1.0", "end")
        text_informe.insert("1.0", informe)
        messagebox.showinfo("Éxito", "Análisis finalizado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def descargar_informe():
    global ruta_informe
    if informe:
        try:
            fecha_hora_actual = datetime.now().strftime("%Y%m%d_%H%M")  # Formato: YYYYMMDD_HHMM
            # Se guarda en la carpeta del primer archivo seleccionado
            carpeta = os.path.dirname(lista_rutas[0])
            nombre_original =  f"Analisis_Georef_{fecha_hora_actual}.txt" 
            ruta_informe = os.path.join(carpeta, nombre_original)
            with open(ruta_informe, "w", encoding="utf-8") as f:
                f.write(informe)
            messagebox.showinfo("Éxito", f"Informe guardado correctamente en:\n{ruta_informe}")
        except Exception as e:
            ruta_informe = ""
            messagebox.showerror("Error", f"No se pudo guardar el informe: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "No hay informe para guardar.")

def abrir_directorio():
    global ruta_informe
    if ruta_informe:
        try:
            carpeta = os.path.dirname(ruta_informe)
            os.startfile(carpeta)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el directorio: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "No se generó ningún informe.")

def iniciar_interfaz():
    root = Tk()
    root.title("Análisis de archivos 'Georeferenciales' Nación Servicios")
    root.geometry("600x500")

    icono_ruta = os.path.join(os.path.dirname(__file__), "../assets/icono.ico")
    if os.path.exists(icono_ruta):
        root.iconbitmap(icono_ruta)
    else:
        print(f"Advertencia: No se encontró el archivo del ícono en la ruta {icono_ruta}")

    Label(root, text="Seleccionar archivos CSV/ZIP/GZ:").pack(pady=5)
    entry_archivo = Entry(root, width=50)
    entry_archivo.pack(pady=5)
    Button(root, text="Seleccionar", command=lambda: seleccionar_archivos(entry_archivo)).pack(pady=5)

    Button(root, text="Analizar Archivos", command=lambda: analizar_archivos_interfaz(text_informe)).pack(pady=10)

    Label(root, text="Informe de análisis:").pack(pady=5)
    text_informe = ScrolledText(root, wrap="word", height=12)
    text_informe.pack(pady=5, expand=True, fill="both")

    Button(root, text="Descargar Informe", command=descargar_informe).pack(pady=10)
    Button(root, text="Abrir carpeta", command=abrir_directorio).pack(pady=5)

    root.mainloop()
