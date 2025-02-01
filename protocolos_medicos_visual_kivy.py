import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import textwrap
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView

# Fixed values for "Indica Dr/a" and "Matrícula del Médico"
INDICA_MEDICO = "Mario Cesar Olivera"
MATRICULA_MEDICO = "112102"
ESTADO = "BUENO"
RESPUESTA = "FAVORABLE"
SALA = "SI"

# Anestesiólogos y sus matrículas
ANESTESIOLOGOS = {
    "Dr. TORREALDAY GUSTAVO": "111387",
    "Dra. ANANIA LUCIA": "125886",
}

# Estudio options
ESTUDIO = [
    "BLOQUEO TERAPÉUTICO DEL DOLOR",
    "TERMOLESION POR RADIOFRECUENCIA",
]

class ProtocoloApp(App):
    def build(self):
        self.title = "Generador de Protocolos PDF"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input fields
        self.entry_paciente = TextInput(hint_text="Paciente", multiline=False)
        self.entry_afiliacion = TextInput(hint_text="Número de afiliación", multiline=False)
        self.entry_fecha = TextInput(hint_text="Fecha (DD-MM-YYYY)", multiline=False)
        self.entry_indicacion = TextInput(hint_text="Indicacion", multiline=False)
        
        self.variable_estudio = Spinner(
            text=ESTUDIO[0],
            values=ESTUDIO
        )
        
        self.variable_anestesiologo = Spinner(
            text=list(ANESTESIOLOGOS.keys())[0],
            values=list(ANESTESIOLOGOS.keys())
        )
        
        self.entry_anestesiologo_matricula = TextInput(text=ANESTESIOLOGOS[self.variable_anestesiologo.text], multiline=False, readonly=True)
        self.variable_anestesiologo.bind(text=self.actualizar_matricula_anestesiologo)
        
        # Add widgets to layout
        layout.add_widget(Label(text="Paciente:"))
        layout.add_widget(self.entry_paciente)
        layout.add_widget(Label(text="Número de afiliación:"))
        layout.add_widget(self.entry_afiliacion)
        layout.add_widget(Label(text="Fecha (DD-MM-YYYY):"))
        layout.add_widget(self.entry_fecha)
        layout.add_widget(Label(text="Estudio:"))
        layout.add_widget(self.variable_estudio)
        layout.add_widget(Label(text="Indicacion:"))
        layout.add_widget(self.entry_indicacion)
        layout.add_widget(Label(text="Anestesiólogo:"))
        layout.add_widget(self.variable_anestesiologo)
        layout.add_widget(Label(text="Matrícula del Anestesiólogo:"))
        layout.add_widget(self.entry_anestesiologo_matricula)
        
        # Buttons
        boton_generar = Button(text="Generar PDF", on_press=self.generar_pdf_desde_interfaz)
        boton_salir = Button(text="Salir", on_press=self.cerrar_aplicacion)
        boton_directorio = Button(text="Seleccionar Directorio", on_press=self.seleccionar_directorio)
        
        layout.add_widget(boton_generar)
        layout.add_widget(boton_salir)
        layout.add_widget(boton_directorio)
        
        # List of input fields for navigation
        self.inputs = [
            self.entry_paciente,
            self.entry_afiliacion,
            self.entry_fecha,
            self.variable_estudio,
            self.entry_indicacion,
            self.variable_anestesiologo,
            self.entry_anestesiologo_matricula
        ]
        
        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)
        
        # Default output directory
        self.output_dir = os.path.join(os.getcwd(), "protocolos")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        return layout

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key in (9, 13):  # Tab or Enter key
            focused = next((i for i, input in enumerate(self.inputs) if input.focus), None)
            if focused is not None:
                next_index = (focused + 1) % len(self.inputs)
                self.inputs[next_index].focus = True
                return True
        return False

    def actualizar_matricula_anestesiologo(self, spinner, text):
        self.entry_anestesiologo_matricula.text = ANESTESIOLOGOS.get(text, "")

    def seleccionar_directorio(self, instance):
        content = FileChooserIconView(on_submit=self.directorio_seleccionado)
        self.popup = Popup(title="Seleccionar Directorio", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def directorio_seleccionado(self, filechooser, selection, touch):
        if selection:
            self.output_dir = selection[0]
        self.popup.dismiss()

    def generar_pdf_desde_interfaz(self, instance):
        datos = {
            'Paciente': self.entry_paciente.text.upper(),
            'Afiliacion': self.entry_afiliacion.text.upper(),
            'Fecha': self.entry_fecha.text.upper(),
            'Estudio': self.variable_estudio.text.upper(),
            'Indicacion': self.entry_indicacion.text.upper(),
            'Anestesiologo': self.variable_anestesiologo.text.upper(),
            'Anestesiologo Matricula': self.entry_anestesiologo_matricula.text.upper(),
            'Estado': ESTADO,
            'Respuesta': RESPUESTA,
            'Sala': SALA
        }
        paciente_nombre = datos.get('Paciente', 'N/A').replace(' ', '_')
        metodo = datos.get('Estudio', 'N/A').replace(' ', '_')
        if paciente_nombre == 'N/A':
            paciente_nombre = "Paciente"
        if metodo == 'N/A':
            metodo = "Estudio"
        output_filename = f"Protocolo_{INDICA_MEDICO.replace(' ', '_')}_{metodo}_{paciente_nombre}.pdf"
        output_filepath = os.path.join(self.output_dir, output_filename)
        generar_pdf(datos, output_filepath)
        popup = Popup(title='Éxito', content=Label(text='PDF generado correctamente.'), size_hint=(0.6, 0.4))
        popup.open()
        
        # Clear input fields
        self.entry_paciente.text = ""
        self.entry_afiliacion.text = ""
        self.entry_fecha.text = ""
        self.entry_indicacion.text = ""
        self.variable_estudio.text = ESTUDIO[0]
        self.variable_anestesiologo.text = list(ANESTESIOLOGOS.keys())[0]
        self.actualizar_matricula_anestesiologo(self.variable_anestesiologo, self.variable_anestesiologo.text)

    def cerrar_aplicacion(self, instance):
        App.get_running_app().stop()

def generar_pdf(datos, output_filename):
    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setFont("Helvetica", 16)
    
    # Título
    c.drawRightString(550, 800, "TOMOGRAFÍA COMPUTADA")
    
    # Datos del paciente
    c.drawRightString(550, 780, f"Sr/a: {datos.get('Paciente', 'N/A')}")
    c.drawRightString(550, 760, f"Número de afiliación: {datos.get('Afiliacion', 'N/A')}")
    c.drawRightString(550, 740, f"Indica Dr/a: {INDICA_MEDICO}")
    c.drawRightString(550, 720, f"MN: {MATRICULA_MEDICO}")
    
    # Formatear la fecha para mostrar en formato DD-MM-YYYY
    fecha = datos.get('Fecha', 'N/A')
    if isinstance(fecha, datetime):
        fecha = fecha.strftime("%d-%m-%Y")
    else:
        try:
            fecha = datetime.strptime(fecha, "%d-%m-%Y").strftime("%d-%m-%Y")
        except ValueError:
            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
            except ValueError:
                fecha = 'N/A'
    c.drawRightString(550, 700, f"Fecha: {fecha}")
    estudio = datos.get('Estudio', 'N/A')

    c.setFontSize(12)
    # Procedimiento
    if estudio != 'N/A':
        c.drawString(50, 680, f"Estudio: {estudio}")
    else:
        c.drawString(50, 680, "Estudio: N/A")
    c.drawString(50, 660, "Se efectuó tomografía computada como guía para la realización")
    
    # Wrap the indicacion text
    indicacion_text = f" de: {datos.get('Indicacion', 'N/A')} por LUMBALGIA."
    wrapped_text = textwrap.wrap(indicacion_text, width=80)
    y_position = 640
    for line in wrapped_text:
        c.drawString(50, y_position, line)
        y_position -= 20
     
    # Técnica
    c.drawString(50, y_position - 40, "TECNICA:")
    c.drawString(70, y_position - 60, "Paciente en decúbito ventral bajo neuroleptoanalgesia con globos oculares protegidos")
    c.drawString(70, y_position - 80, f"por Anestesiólogo {datos.get('Anestesiologo', 'N/A')}: MN: {datos.get('Anestesiologo Matricula', 'N/A')}.")
    c.drawString(70, y_position - 100, "Embrocado con iodopovidona de la zona a infiltrar, marcado con tomógrafo en piel,")
    c.drawString(70, y_position - 120, "infiltración de piel local con lidocaína, colocación de la aguja espinal raquídea N° 21,")
    c.drawString(70, y_position - 140, "se constata posición de la aguja raquídea bajo TAC.")
    if estudio != 'N/A':
        if 'BLOQUEO' in estudio:
            c.drawString(70, y_position - 160, "Se infiltra con suspensión analgésica y antiinflamatoria de acción prolongada ")
            c.drawString(70, y_position - 180, "(Bupivacaína) y corticoide de acción prolongada (TRIAMCINOLONA).")
        elif 'RADIO' in estudio:
            c.drawString(70, y_position - 160, "Se realiza RADIOFREQUENCIA por TERMOLESION facetaria bilateral y se infiltra")
            c.drawString(70, y_position - 180, "con suspensión anestesica")    
    else:
        c.drawString(70, y_position - 160, "ERROR DE IMPORTACION DE DATOS DE EXEL")
    # Complicaciones
    c.drawString(70, y_position - 220, "No se presentan complicaciones inherentes al método. Se envían registros obtenidos antes")
    c.drawString(70, y_position - 240, "y durante el procedimiento.")
    
    # Estado del paciente y recomendaciones
    c.drawString(50, y_position - 280, f"Estado general del paciente: {datos.get('Estado', 'N/A')}")
    c.drawString(50, y_position - 300, f"Respuesta al procedimiento: {datos.get('Respuesta', 'N/A')}")
    c.drawString(50, y_position - 320, f"Sala de recuperación: {datos.get('Sala', 'N/A')}")
    c.drawString(50, y_position - 360, "Recomendaciones: Reposo por 48 hs, analgésico vía oral, calor local Y control por C. EXTERNOS ")
    c.drawString(50, y_position - 380, "MEDICO")
    
    c.setFontSize(16)
    # Firma del médico
    c.drawRightString(550, y_position - 500, f"Dr. {INDICA_MEDICO}")
    c.drawRightString(550, y_position - 520, f"MN: {MATRICULA_MEDICO}")
    c.drawRightString(550, y_position - 540, "TRAUMATÓLOGO")
    
    c.save()

if __name__ == "__main__":
    ProtocoloApp().run()
