import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Cola import Cola as c  # Cambia el alias de `p` a `c`
import os
from dotenv import load_dotenv

load_dotenv()

class Grafico(c):  # Cambia la herencia de Pila a Cola
    def __init__(self):
        super().__init__()
    
    def encolar(self, proceso):  # Cambia `apilar` por `encolar`
        super().encolar(proceso)
    
    def desencolar(self):  # Cambia `desapilar` por `desencolar`
        return super().desencolar()

    def esta_vacia(self):
        return super().esta_vacia()
    
    def obtener_procesos(self):
        return super().obtener_procesos()

    def prioridad_to_width(self, prioridad):
        if prioridad == "alta":
            return 1.2
        elif prioridad == "media":
            return 0.8
        elif prioridad == "baja":
            return 0.5
        return 0.5
    
    def visualizar_cola(self):  # Cambia el nombre de `visualizar_pila` a `visualizar_cola`
        try:
            fig, ax = plt.subplots(figsize=(12, 8))  # Ajusta el tamaño de la figura

            def actualizar(frame):
                ax.clear()
                procesos = self.obtener_procesos()
                if procesos:
                    anchos = [self.prioridad_to_width(p.prioridad) for p in procesos]
                    nombres_prioridades = [f"{p.proceso} ({p.prioridad.capitalize()})" for p in procesos]
                    
                    bars = ax.barh(range(len(procesos)), anchos, tick_label=nombres_prioridades)
                    
                    for bar, prioridad in zip(bars, [p.prioridad for p in procesos]):
                        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                                f' {prioridad.capitalize()}', va='center')

                    handles = [
                        plt.Line2D([0], [0], color='C0', lw=4, label='Alta'),
                        plt.Line2D([0], [0], color='C1', lw=4, label='Media'),
                        plt.Line2D([0], [0], color='C2', lw=4, label='Baja')
                    ]
                    ax.legend(handles=handles, title='Prioridad')

                    ax.set_xlim(0, max(anchos) * 1.5)
                    ax.set_xlabel('Ancho basado en Prioridad')
                    ax.set_title('Visualización de la Cola')  # Cambia el título para reflejar que es una cola

            anim = FuncAnimation(fig, actualizar, frames=10, interval=1000)
            
            # Asegúrate de dibujar la figura antes de guardar
            fig.canvas.draw()
            
            # Guardar la imagen
            ruta = os.getenv("REPORTS_PATH")
            plt.savefig(f'{ruta}visualizacion_cola.png', format='png')  # Cambia el nombre del archivo guardado
            print("Imagen guardada como 'visualizacion_cola.png'.")
            
            # Mostrar la figura después de guardar
            plt.show()

        except Exception as e:
            print(f"Error al visualizar la Cola: {e}")  # Cambia el mensaje de error para reflejar que es una cola
