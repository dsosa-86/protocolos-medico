# Generador de Protocolos PDF

Este proyecto es una aplicación para generar protocolos médicos en formato PDF utilizando Kivy para la interfaz gráfica y ReportLab para la generación de PDFs.

## Requisitos

- Python 3.6+
- Kivy
- ReportLab
- Pandas

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/protocolos_medicos.git
    cd protocolos_medicos
    ```

2. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

### Interfaz Gráfica

Para ejecutar la aplicación con interfaz gráfica, usa el siguiente comando:
```sh
python protocolos_medicos_visual_kivy.py
```

### Línea de Comandos

Para generar PDFs desde un archivo Excel usando la línea de comandos, usa el siguiente comando:
```sh
python protocolos.py <ruta_al_archivo_excel>
```

## Estructura del Proyecto

- `protocolos_medicos_visual_kivy.py`: Archivo principal de la aplicación con interfaz gráfica.
- `protocolos.py`: Script para generar PDFs desde un archivo Excel.
- `requirements.txt`: Archivo de dependencias.
- `README.md`: Documentación del proyecto.

## Dependencias

- Kivy: Biblioteca para la creación de interfaces gráficas.
- ReportLab: Biblioteca para la generación de documentos PDF.
- Pandas: Biblioteca para la manipulación y análisis de datos.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.