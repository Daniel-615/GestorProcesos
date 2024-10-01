import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QMessageBox, QInputDialog, QLabel, QListWidget, QHBoxLayout
)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from proceso.Proceso import Proceso
from GestorProceso import GestorProcesos
from proceso.Json import Json
from bot.Bot import Bot  
from output.Reportes import Reportes
from output.Voz import Voz

class BotThread(QThread):
    finished_signal = pyqtSignal()

    def run(self):
        try:
            iniciarBot()  # Ejecuta la función del bot
        except Exception as e:
            print(f"Error en BotThread: {e}")
        finally:
            self.finished_signal.emit()  # Emite la señal de finalización

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Procesos")
        self.setGeometry(100, 100, 800, 600)

        # Inicializar componentes
        self.voz = Voz()
        self.gestor = GestorProcesos()
        self.json_config = Json()
        self.cores = self.gestor.consulta_cores()
        self.n = 1  # Contador de procesos

        # Layout principal
        self.layout = QVBoxLayout()

        # Configuración Inicial
        self.btn_configurar = QPushButton("Configuración Inicial")
        self.btn_configurar.clicked.connect(self.configurar)
        self.layout.addWidget(self.btn_configurar)

        # Botón para Agregar Proceso
        self.btn_agregar = QPushButton("Agregar Proceso")
        self.btn_agregar.clicked.connect(self.agregar_proceso_gui)
        self.layout.addWidget(self.btn_agregar)

        # Botón para Iniciar Ejecución
        self.btn_empezar = QPushButton("Empezar Ejecución")
        self.btn_empezar.clicked.connect(self.ejecutar_procesos_gui)
        self.layout.addWidget(self.btn_empezar)

        # Botón para Iniciar Bot
        self.btn_bot = QPushButton("Iniciar Bot")
        self.btn_bot.clicked.connect(self.iniciar_bot_gui)
        self.layout.addWidget(self.btn_bot)

        # Botón para Salir
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.clicked.connect(self.salir_gui)
        self.layout.addWidget(self.btn_salir)

        # Sección para mostrar las colas
        self.seccion_colas = QWidget()
        self.layout_colas = QHBoxLayout()

        # FIFO
        self.lista_fifo = QListWidget()
        self.lista_fifo.setFixedWidth(180)
        self.layout_colas.addWidget(self.lista_fifo)
        self.label_fifo = QLabel("Cola FIFO")
        self.layout_colas.addWidget(self.label_fifo)

        # Round Robin
        self.lista_rr = QListWidget()
        self.lista_rr.setFixedWidth(180)
        self.layout_colas.addWidget(self.lista_rr)
        self.label_rr = QLabel("Cola Round Robin")
        self.layout_colas.addWidget(self.label_rr)

        # SJF
        self.lista_sjf = QListWidget()
        self.lista_sjf.setFixedWidth(180)
        self.layout_colas.addWidget(self.lista_sjf)
        self.label_sjf = QLabel("Cola SJF")
        self.layout_colas.addWidget(self.label_sjf)

        # Priority
        self.lista_priority = QListWidget()
        self.lista_priority.setFixedWidth(180)
        self.layout_colas.addWidget(self.lista_priority)
        self.label_priority = QLabel("Cola Priority")
        self.layout_colas.addWidget(self.label_priority)

        self.seccion_colas.setLayout(self.layout_colas)
        self.layout.addWidget(self.seccion_colas)

        # Configuración de la ventana principal
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Timer para actualizar las colas periódicamente
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_colas)
        self.timer.start(5000)  # Actualizar cada 5 segundos

        # Inicializar el BotThread como None
        self.bot_thread = None

    def configurar(self):
        """Configuración Inicial mediante cuadros de diálogo."""
        try:
            show_colas = QMessageBox.question(
                self, "Configuración",
                "¿Deseas mostrar las colas por cada evento?",
                QMessageBox.Yes | QMessageBox.No
            ) == QMessageBox.Yes

            enviar_reportes = QMessageBox.question(
                self, "Configuración",
                "¿Deseas que se envíen los reportes por medio de Discord?",
                QMessageBox.Yes | QMessageBox.No
            ) == QMessageBox.Yes

            self.json_config.setColas(show_colas)
            self.json_config.setDc(enviar_reportes)
            self.json_config.crear_json_configuracion()
            QMessageBox.information(self, "Configuración", "Configuración guardada exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la configuración: {e}")

    def agregar_proceso_gui(self):
        """Agregar un nuevo proceso mediante la GUI."""
        try:
            total_procesos = (
                self.gestor.cola_fifo.contador +
                self.gestor.cola_rr.contador +
                self.gestor.cola_sjf.contador +
                self.gestor.cola_priority.contador
            )

            if total_procesos > self.cores:
                QMessageBox.warning(
                    self, "Límite de Procesos",
                    f"Has alcanzado el número máximo de procesos asignados a {self.cores} cores."
                )
                return

            lista_comandos = Proceso.devolver_comandos()
            comando, ok = QInputDialog.getText(
                self, "Agregar Proceso",
                f"Lista de Comandos:\n{lista_comandos}\n¿Qué tipo de comando deseas ejecutar?"
            )
            if not ok or not comando.strip():
                return

            prioridad, ok = QInputDialog.getItem(
                self, "Agregar Proceso",
                "¿Tipo de prioridad?",
                ["baja", "media", "alta"], 0, False
            )
            if not ok:
                return
            prioridad = prioridad.lower()

            planificacion, ok = QInputDialog.getItem(
                self, "Agregar Proceso",
                "¿Tipo de Planificación?",
                ["FIFO", "Robin", "SJF", "Priority"], 0, False
            )
            if not ok:
                return
            planificacion = planificacion.lower()

            proceso = Proceso(
                prioridad=prioridad, 
                proceso=f"Proceso {self.n}", 
                tipo_proceso=comando, 
                gestor=self.gestor, 
                tipo_planificacion=planificacion
            )

            self.gestor.agregar_proceso(proceso)
            self.n += 1
            message = f"Proceso {self.n -1} agregado correctamente a la cola de {planificacion.upper()}."
            self.infLog(message)
            QMessageBox.information(self, "Éxito", message)
        except Exception as e:
            message = f"Error al agregar el proceso: {e}"
            self.errLog(message)
            QMessageBox.critical(self, "Error", message)

    def ejecutar_procesos_gui(self):
        """Ejecutar los procesos mediante la GUI."""
        try:
            total_procesos = (
                self.gestor.cola_fifo.contador +
                self.gestor.cola_rr.contador +
                self.gestor.cola_sjf.contador +
                self.gestor.cola_priority.contador
            )

            if total_procesos == 0:
                QMessageBox.information(
                    self, "Información",
                    "No hay procesos en la cola. Agrega al menos un proceso antes de empezar."
                )
                return

            if not self.gestor.cola_fifo.esta_vacia():
                self.infLog("Ejecutando procesos FIFO...")
                self.gestor.visualizar(1)
                self.gestor.ejecutar_fifo()

            if not self.gestor.cola_rr.esta_vacia():
                self.infLog("Ejecutando procesos Round Robin...")
                self.gestor.visualizar(2)
                self.gestor.ejecutar_robin()

            if not self.gestor.cola_sjf.esta_vacia():
                self.infLog("Ejecutando procesos SJF...")
                self.gestor.visualizar(3)
                self.gestor.ejecutar_sjf()

            if not self.gestor.cola_priority.esta_vacia():
                self.infLog("Ejecutando procesos por prioridad...")
                self.gestor.visualizar(4)
                self.gestor.ejecutar_priority()

            if (self.gestor.cola_priority.esta_vacia() and
                self.gestor.cola_sjf.esta_vacia() and
                self.gestor.cola_fifo.esta_vacia() and
                self.gestor.cola_rr.esta_vacia()):
                
                reportes = Reportes()
                nombre_pdf_imagenes = "graficos"
                reportes.convertir_imagenes_a_pdf(nombre_pdf_imagenes, self.gestor)
                self.infLog(f"{nombre_pdf_imagenes} convertidos a pdf.")
                QMessageBox.information(self, "Éxito", "Procesos ejecutados y reportes generados.")
        except Exception as e:
            message = f"Error al ejecutar procesos: {e}"
            self.errLog(message)
            QMessageBox.critical(self, "Error", message)

    def iniciar_bot_gui(self):
        """Iniciar el bot mediante la GUI."""
        try:
            self.json_config.cargar_configuracion()
            enviar_reportes = self.json_config.getDc()
            if enviar_reportes:
                message = "Mandando reportes"
                self.voz.hablar(message)
                
                self.bot_thread = BotThread()
                self.bot_thread.finished_signal.connect(self.on_bot_finished)
                self.bot_thread.start()

                QMessageBox.information(self, "Bot", "Bot iniciado correctamente.")
            else:
                QMessageBox.information(
                    self, "Bot",
                    "La configuración indica que no se deben enviar reportes por Discord."
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar el bot: {e}")

    def on_bot_finished(self):
        """Método llamado cuando el bot ha terminado su ejecución."""
        QMessageBox.information(self, "Bot", "El bot ha finalizado. Cerrando la aplicación.")
        QApplication.quit()

    def salir_gui(self):
        """Salir de la aplicación."""
        try:
            self.voz.hablar("La planificación ha sido un éxito. ¡Hasta la próxima!")
        except Exception as e:
            print(f"Error al reproducir el mensaje de salida: {e}")
        QApplication.quit()

    def infLog(self, message):
        """Registrar información en el log."""
        log = self.gestor.getLog()
        log.log_info(message)

    def errLog(self, message):
        """Registrar errores en el log."""
        log = self.gestor.getLog()
        log.log_error(message)

    def actualizar_colas(self):
        """Actualizar la visualización de las colas en la GUI."""
        try:
            self.lista_fifo.clear()
            for proceso in self.gestor.cola_fifo.obtener_procesos():
                self.lista_fifo.addItem(proceso.proceso)

            self.lista_rr.clear()
            for proceso in self.gestor.cola_rr.obtener_procesos():
                self.lista_rr.addItem(proceso.proceso)

            self.lista_sjf.clear()
            for proceso in self.gestor.cola_sjf.obtener_procesos():
                self.lista_sjf.addItem(proceso.proceso)

            self.lista_priority.clear()
            for proceso in self.gestor.cola_priority.obtener_procesos():
                self.lista_priority.addItem(proceso.proceso)
        except Exception as e:
            print(f"Error al actualizar las colas: {e}")

def iniciarBot():
    bot = Bot()
    bot.start()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
