import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from proceso.Cola import Cola as c  
import os
from dotenv import load_dotenv

load_dotenv()

class Grafico(c): 
    def __init__(self, log, mensaje):       
        super().__init__()
        self.contador = c.getContador()
        self.log = log 
        self.title = mensaje
    
    def EstadoRobinGrafico(self, estado_grafico):
        self.estado = estado_grafico
    
    def setLog(self):
        super().setLog(self.log, self.title)
    
    def encolar(self, proceso):  
        super().encolar(proceso)
    
    def desencolar(self): 
        return super().desencolar()

    def esta_vacia(self):
        return super().esta_vacia()
    
    def obtener_procesos(self):
        return super().obtener_procesos()
    
    def getTiempos(self):
        return super().obtener_tiempos_procesos()

    def prioridad_to_width(self, prioridad):
        if prioridad == "alta":
            return 1.2
        elif prioridad == "media":
            return 0.8
        elif prioridad == "baja":
            return 0.5
        return 0.5

    def fifo_to_color(self, tipo, index=None):
        if tipo == "FIFO":
            colores_fifo = ['red', 'orange', 'green','blue','lightblue']
            if index is not None:
                return colores_fifo[(index - 1) % len(colores_fifo)]
            else:
                return 'gray'
        return 'gray'

    def sjf_to_color(self, tipo):
        if tipo == "SJF":
            tiempos = self.obtener_tiempos_procesos()
            colores = []
            for tiempo in tiempos:
                if tiempo <= 5:  
                    colores.append('green')
                elif 5 < tiempo <= 15:
                    colores.append('orange')
                else:
                    colores.append('red')
            return colores
        return ['gray'] * len(self.obtener_procesos())

    def robin_to_color(self, tipo):
        if tipo == "ROUND ROBIN":
            if self.estado == "Ejecutando":
                return 'blue'  
            elif self.estado == "Esperando":
                return 'lightblue' 
            elif self.estado == "Quantum agotado":
                return 'darkblue'  
            else:
                return 'gray'
        return 'gray'

    def prioridad_to_color(self, prioridad, tipo):
        if tipo == "PRIORIDAD":
            if prioridad == "alta":
                return 'red'
            elif prioridad == "media":
                return 'orange'
            elif prioridad == "baja":
                return 'green'
        return 'gray'

    def algorithm_to_color(self, prioridad, tipo, index):
        try:
            if tipo == "PRIORIDAD":
                return self.prioridad_to_color(prioridad, tipo)
            elif tipo == "FIFO":
                return self.fifo_to_color(tipo, index)
            elif tipo == "SJF":
                colores_sjf = self.sjf_to_color(tipo)
                return colores_sjf[index - 1] if index <= len(colores_sjf) else 'gray'
            elif tipo == "ROUND ROBIN":
                return self.robin_to_color(tipo)
            else:
                return 'gray'
        except Exception as e:
            log = self.getLog()
            message = f"Error al elegir el color: {e}"
            log.log_error(message)
            return 'gray'

    def handles_cola_event(self, plt, title):
        handles_dict = {
            "EJECUCION": [
            ],
            "LISTOS": [
            ],
            "BLOQUEADOS": [
            ]
        }
        return handles_dict.get(title, None)
    
    def handles_cola(self, plt, title):
        handles_dict = {
            "PRIORIDAD": [
                plt.Line2D([0], [0], color='red', lw=4, label='Alta'),
                plt.Line2D([0], [0], color='orange', lw=4, label='Media'),
                plt.Line2D([0], [0], color='green', lw=4, label='Baja')
            ],
            "FIFO": [
                plt.Line2D([0], [0], color='red', lw=4, label='Primero en la Cola'),
                plt.Line2D([0], [0], color='orange', lw=4, label='Segundo en la Cola'),
                plt.Line2D([0], [0], color='green', lw=4, label='Tercero en la Cola'),
                plt.Line2D([0], [0], color='green', lw=4, label='Cuarto en la Cola'),
                plt.Line2D([0], [0], color='green', lw=4, label='Quinto en la Cola')
            ],
            "ROUND ROBIN": [
                plt.Line2D([0], [0], color='gray', lw=4, label='Quantum agotado')
            ],
            "SJF": [
                plt.Line2D([0], [0], color='green', lw=4, label='Tarea corta'),
                plt.Line2D([0], [0], color='orange', lw=4, label='Tarea media'),
                plt.Line2D([0], [0], color='red', lw=4, label='Tarea larga')
            ]
        }
        return handles_dict.get(title, self.handles_cola_event(plt, title))

    def visualizar_cola(self, file, title):
        try:
            fig, ax = plt.subplots(figsize=(12, 8))

            def actualizar(frame):
                ax.clear()
                procesos = self.obtener_procesos()
                
                if procesos:
                    anchos = [self.prioridad_to_width(p.prioridad) for p in procesos]
                    nombres_prioridades = [f"{p.proceso} ({p.prioridad.capitalize()})" for p in procesos]
                    
                    # Asignamos los colores basados en el algoritmo y la prioridad
                    colores = [self.algorithm_to_color(p.prioridad, title, i+1) for i, p in enumerate(procesos)]
                    
                    bars = ax.barh(range(len(procesos)), anchos, tick_label=nombres_prioridades, color=colores)
                    
                    # Mejora: Agregar el tiempo de ejecución en un cuadro con formato más elegante
                    for bar, proceso in zip(bars, procesos):
                        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                                f'{proceso.rafaga_cpu} unidades',
                                va='center', ha='center',
                                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

                    handles = self.handles_cola(plt, title)
                    ax.legend(handles=handles, title='Prioridad')

                    ax.set_xlim(0, max(anchos) * 1.5)
                    ax.set_title(title)

            anim = FuncAnimation(fig, actualizar, frames=10, interval=1000)
            fig.canvas.draw()

            ruta = os.getenv("REPORTS_PATH_IMG")
            plt.savefig(f'{ruta}{file}.png', format='png')
            
            log = self.getLog()
            message = f"Imagen guardada como '{file}.png'."
            log.log_info(message)

        except Exception as e:
            log = self.getLog()
            message = f"Error al visualizar la Cola: {e}"
            log.log_error(message)
