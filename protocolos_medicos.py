import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import argparse
from datetime import datetime
import os

#Import para Interfas de usuario
import tkinter as tk
from tkinter import filedialog, messagebox




def generar_pdf(datos, output_filename):
    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setFont("Helvetica", 14)
    
    # Título
    c.drawRightString(550, 800, "TOMOGRAFÍA COMPUTADA")
    
    # Datos del paciente
    c.drawRightString(550, 780, f"Sr/a: {datos.get('Paciente', 'N/A')}")
    c.drawRightString(550, 760, f"Número de afiliación: {datos.get('Afiliacion', 'N/A')}")
    c.drawRightString(550, 740, f"Indica Dr/a: {datos.get('Medico', 'N/A')}")
    
    # Formatear la fecha para mostrar solo la fecha y no la hora
    fecha = datos.get('Fecha', 'N/A')
    if isinstance(fecha, datetime):
        fecha = fecha.strftime("%Y-%m-%d")
    else:
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        except ValueError:
            fecha = 'N/A value error'
    c.drawRightString(550, 720, f"Fecha: {fecha}")
    estudio = datos.get('Estudio', 'N/A')

    c.setFontSize(12)
    # Procedimiento
    if estudio != 'N/A':
        c.drawString(50, 700, f"Estudio: {estudio}")
    else:
        c.drawString(50, 700, "Estudio: N/A")
    #c.drawString(50, 700, "Estudio: BLOQUEO TERAPÉUTICO DEL DOLOR")
    c.drawString(50, 680, "Se efectuó tomografía computada como guía para la realización")
    c.drawString(50, 660, f" de: {datos.get('Zona', 'N/A')} por LUMBALGIA.")
     
    # Técnica
    c.drawString(50, 640, "TECNICA:")
    c.drawString(70, 620, "Paciente en decúbito ventral bajo neuroleptoanalgesia con globos oculares protegidos")
    c.drawString(70, 600, f"por Anestesiólogo {datos.get('Anestesiologo', 'N/A')}.")
    c.drawString(70, 580, "Embrocado con iodopovidona de la zona a infiltrar, marcado con tomógrafo en piel,")
    c.drawString(70, 560, "infiltración de piel local con lidocaína, colocación de la aguja espinal raquídea N° 21,")
    c.drawString(70, 540, "se constata posición de la aguja raquídea bajo TAC.")
    if estudio != 'N/A':
        if 'BLOQUEO' in estudio:
            c.drawString(70, 520, "Se infiltra con suspensión analgésica y antiinflamatoria de acción prolongada ")
            c.drawString(70, 500, "(Bupivacaína) y corticoide de acción prolongada (TRIAMCINOLONA).")
        elif 'RADIOFREQUENCIA' in estudio:
            c.drawString(70, 520, "Se realiza radiofrecuencia por TERMOLESION facetaria bilateral y se infiltra")
            c.drawString(70, 500, "con suspensión anestesica")    
    else:
        c.drawString(70, 520, "ERROR DE IMPORTACION DE DATOS DE EXEL")
    # Complicaciones
    c.drawString(70, 480, "No se presentan complicaciones inherentes al método. Se envían registros obtenidos antes")
    c.drawString(70, 460, "y durante el procedimiento.")
    
    # Estado del paciente y recomendaciones
    c.drawString(50, 440, f"Estado general del paciente: {datos.get('Estado', 'N/A')}")
    c.drawString(50, 420, f"Respuesta al procedimiento: {datos.get('Respuesta', 'N/A')}")
    c.drawString(50, 400, f"Sala de recuperación: {datos.get('Sala', 'N/A')}")
    c.drawString(50, 380, "Recomendaciones: Reposo por 48 hs, analgésico vía oral, calor local Y control por C. EXTERNOS ")
    c.drawString(50, 360, "MEDICO")
    
    c.setFontSize(14)
    # Firma del médico
    c.drawString(50, 300, f"Dr. {datos.get('Medico', 'N/A')}")
    c.drawString(50, 280, f"MN: {datos.get('Matricula Medico', 'N/A')}")
    c.drawString(50, 260, "TRAUMATÓLOGO")
    
    c.save()

def leer_datos_excel(archivo_excel):
    df = pd.read_excel(archivo_excel, header=None)
    keys = df.iloc[:, 0].tolist()
    protocolos = [df.iloc[:, i].tolist() for i in range(1, df.shape[1])]
    datos_list = [{keys[j]: protocolo[j] for j in range(len(keys))} for protocolo in protocolos]
    return datos_list


def seleccionar_archivo():
    archivo_excel = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
    if not archivo_excel:
        return
    
    datos_paciente_list = leer_datos_excel(archivo_excel)
    if not datos_paciente_list:
        messagebox.showerror("Error", "El archivo Excel no contiene datos.")
        return
    
    for i, datos in enumerate(datos_paciente_list):
        paciente_nombre = datos.get('Paciente', 'N/A').replace(' ', '_')
        metodo = datos.get('Estudio', 'N/A').replace(' ', '_')
        medico = datos.get('Medico', 'N/A').replace(' ', '_')
        output_filename = f"Protocolo_{medico}_{metodo}_{paciente_nombre}.pdf"
        output_filename = os.path.join(os.path.dirname(archivo_excel), output_filename)
        generar_pdf(datos, output_filename)
    
    messagebox.showinfo("Éxito", "PDFs generados correctamente.")

def cerrar_aplicacion():
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Generador de Protocolos PDF")
    root.geometry("400x200")
    
    label = tk.Label(root, text="Seleccione el archivo Excel:")
    label.pack(pady=10)
    
    boton_seleccionar = tk.Button(root, text="Seleccionar Archivo", command=seleccionar_archivo)
    boton_seleccionar.pack(pady=5)
    
    boton_salir = tk.Button(root, text="Salir", command=cerrar_aplicacion)
    boton_salir.pack(pady=5)
    
    root.mainloop()









"""""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Procesar un archivo Excel y generar un PDF.')
    parser.add_argument("archivo_excel", type=str, help="Ruta al archivo Excel con los datos del paciente")
    args = parser.parse_args()
    datos_paciente_list = leer_datos_excel(args.archivo_excel)
    if not datos_paciente_list:
        print("El archivo Excel no contiene datos.")
    else:
        for i, datos in enumerate(datos_paciente_list):
            paciente_nombre = datos.get('Paciente', 'N/A').replace(' ', '_')
            metodo = datos.get('Estudio', 'N/A').replace(' ', '_')
            medico = datos.get('Medico', 'N/A').replace(' ', '_')
            if paciente_nombre == 'N/A':
                paciente_nombre = f"Paciente_{i+1}"
            if metodo == 'N/A':
                metodo = f"Estudio_{i+1}"
            if medico == 'N/A':
                medico = f"Medico_{i+1}"
            output_filename = f"Protocolo_{medico}_{metodo}_{paciente_nombre}.pdf"
            output_filename = os.path.join(os.path.dirname(args.archivo_excel), output_filename)
            generar_pdf(datos, output_filename)
"""