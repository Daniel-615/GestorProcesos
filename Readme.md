GestorProcesos

Descripción
GestorProcesos es una aplicación diseñada para simular la gestión de procesos en un sistema operativo. Implementa varios algoritmos de planificación de procesos, como Round Robin, SJF (Shortest Job First), FIFO, y planificación por prioridad. Además, el proyecto incluye la capacidad de generar reportes y visualizaciones de los estados de los procesos y los recursos del sistema.

Características
Simulación de la planificación de procesos utilizando algoritmos comunes.
Gestión de colas de procesos listos y bloqueados.
Monitoreo de recursos del sistema (CPU, memoria, disco, etc.).
Generación de reportes en diferentes formatos (JSON, PDF, imágenes).
Visualización gráfica de la ejecución de los procesos.
Modularidad y extensibilidad para agregar nuevos algoritmos o funcionalidades.

Instalación:

- Python 3x
- Paquetes listados en requirements.txt

Instalación de dependencias:

- git clone https://github.com/Daniel-615/GestorProcesos.git
- cd GestorProcesos
- pip install -r requirements.txt

Configuración
Crear un archivo .env en el directorio raíz del proyecto. Este archivo debe contener las siguientes variables de entorno:

- REPORTS_PATH_IMG=path/a/tu/carpeta/img
- REPORTS_PATH_DOC=path/a/tu/carpeta/doc
- REPORTS_PATH_PDF=path/a/tu/carpeta/pdf
- Discord_TOKEN=tu_token_de_discord

REPORTS_PATH_IMG: Directorio donde se almacenarán las imágenes generadas.
REPORTS_PATH_DOC: Directorio donde se guardarán los documentos generados.
REPORTS_PATH_PDF: Directorio donde se generarán los reportes en formato PDF.
Discord_TOKEN: (Si usas algún bot de Discord) Token de autenticación de Discord.
Configura el archivo config.json si necesitas personalizar más parámetros del sistema

Uso:

- Ejecutar el archivo principal (main)
  python src/proceso/Main.py
- Los reportes se generarán automáticamente en la carpeta outputs.

Licencia
Este proyecto está bajo la licencia MIT.

Autor
Daniel - Desarrollador Principal - Daniel-615
