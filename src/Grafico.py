import Pila
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class Grafico(Pila):
    def __init__(self):
        super().__init__()
    
    def apilarPila(self):
        Pila.apilar()
    def prioridad_to_width(self, prioridad):
        # Define el ancho de las barras basado en la prioridad
        if prioridad == "alta":
            return 1.2
        elif prioridad == "media":
            return 0.8
        elif prioridad == "baja":
            return 0.5
        return 0.5
    
    def visualizar_pila(self):
        fig, ax = plt.subplots(figsize=(12, 8))  # Ajusta el tamaño de la figura (ancho, alto)

        def actualizar(frame):
            ax.clear()
            procesos = self.obtener_procesos()
            if procesos:
                # Asignar anchos basados en la prioridad
                anchos = [self.prioridad_to_width(p.prioridad) for p in procesos]
                nombres_prioridades = [f"{p.proceso} ({p.prioridad.capitalize()})" for p in procesos]
                
                bars = ax.barh(range(len(procesos)), anchos, tick_label=nombres_prioridades)
                
                # Mostrar prioridad como texto en las barras
                for bar, prioridad in zip(bars, [p.prioridad for p in procesos]):
                    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                            f' {prioridad.capitalize()}', va='center')

            # Crear una leyenda
            handles = [
                plt.Line2D([0], [0], color='C0', lw=4, label='Alta'),
                plt.Line2D([0], [0], color='C1', lw=4, label='Media'),
                plt.Line2D([0], [0], color='C2', lw=4, label='Baja')
            ]
            ax.legend(handles=handles, title='Prioridad')

            ax.set_xlim(0, max(anchos) * 1.5)  # Ajusta el rango del eje x basado en los anchos
            ax.set_xlabel('Ancho basado en Prioridad')
            ax.set_title('Visualización de la Pila')

        # Suprimir advertencia configurando el parámetro frames
        anim = FuncAnimation(fig, actualizar, frames=1, interval=1000)
        plt.show()