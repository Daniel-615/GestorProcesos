import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from proceso.Cola import Cola as c  
import os
from dotenv import load_dotenv

load_dotenv()

class Grafico(c): 
    def __init__(self):       
        super().__init__()
        self.contador = c.getContador() 
    
    def encolar(self, proceso):  
        super().encolar(proceso)
    
    def desencolar(self): 
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
    
    def prioridad_to_color(self, prioridad):
        if prioridad == "alta":
            return 'red'
        elif prioridad == "media":
            return 'orange'
        elif prioridad == "baja":
            return 'green'
        return 'gray'
   
    def visualizar_cola(self, file,title): 
        try:
            fig, ax = plt.subplots(figsize=(12, 8))  

            def actualizar(frame):
                ax.clear()
                procesos = self.obtener_procesos()
                if procesos:
                    anchos = [self.prioridad_to_width(p.prioridad) for p in procesos]
                    nombres_prioridades = [f"{p.proceso} ({p.prioridad.capitalize()})" for p in procesos]
                    colores = [self.prioridad_to_color(p.prioridad) for p in procesos]
                    
                    bars = ax.barh(range(len(procesos)), anchos, tick_label=nombres_prioridades, color=colores)
                    
                    for bar, prioridad in zip(bars, [p.prioridad for p in procesos]):
                        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                                f' {prioridad.capitalize()}', va='center')

                    handles = [
                        plt.Line2D([0], [0], color='red', lw=4, label='Alta'),
                        plt.Line2D([0], [0], color='orange', lw=4, label='Media'),
                        plt.Line2D([0], [0], color='green', lw=4, label='Baja')
                    ]
                    ax.legend(handles=handles, title='Prioridad')

                    ax.set_xlim(0, max(anchos) * 1.5)
                    #ax.set_xlabel('Ancho basado en Prioridad')
                    ax.set_title(title) 

            anim = FuncAnimation(fig, actualizar, frames=10, interval=1000)
            
            # Dibuja la figura antes de guardar
            fig.canvas.draw()
            
            # Guardar la imagen
            ruta = os.getenv("REPORTS_PATH_IMG")
            plt.savefig(f'{ruta}{file}.png', format='png')  
            print(f"Imagen guardada como '{file}.png'.")

        except Exception as e:
            print(f"Error al visualizar la Cola: {e}") 

