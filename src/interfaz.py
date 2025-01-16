import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from src.analisis import analizar_csv

ruta_csv = ""  # Ruta del archivo CSV seleccionado
ruta_informe = ""  # Ruta del informe generado
informe = ""  # Contenido del informe

def seleccionar_archivo(entry):
    global ruta_csv
    ruta_csv = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if ruta_csv:
        entry.delete(0, "end")
        entry.insert(0, ruta_csv)

def analizar_archivo(text_informe):
    global informe
    informe = ""
    try:
        informe = analizar_csv(ruta_csv)
        text_informe.delete("1.0", "end")
        text_informe.insert("1.0", informe)
        messagebox.showinfo("Éxito", "Análisis finalizado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def descargar_informe():
    global ruta_informe
    if informe:
        try:
            # Obtener el directorio del archivo CSV original
            carpeta = os.path.dirname(ruta_csv)
            nombre_original = os.path.splitext(os.path.basename(ruta_csv))[0]
            # Crear la ruta del informe
            ruta_informe = os.path.join(carpeta, f"analisis_{nombre_original}.txt")
            # Guardar el informe
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
    root.title("Análisis de archivo 'Georeferenciales' Nación Servicios")
    root.geometry("600x500")

    icono_ruta = os.path.join("assets", "icono.ico")
    if os.path.exists(icono_ruta):
        root.iconbitmap(icono_ruta)

    Label(root, text="Seleccionar archivo CSV:").pack(pady=5)
    entry_archivo = Entry(root, width=50)
    entry_archivo.pack(pady=5)
    Button(root, text="Seleccionar", command=lambda: seleccionar_archivo(entry_archivo)).pack(pady=5)

    Button(root, text="Analizar Archivo", command=lambda: analizar_archivo(text_informe)).pack(pady=10)

    Label(root, text="Informe de análisis:").pack(pady=5)
    text_informe = ScrolledText(root, wrap="word", height=12)
    text_informe.pack(pady=5, expand=True, fill="both")

    Button(root, text="Descargar Informe", command=descargar_informe).pack(pady=10)
    Button(root, text="Abrir carpeta", command=abrir_directorio).pack(pady=5)

    root.mainloop()
