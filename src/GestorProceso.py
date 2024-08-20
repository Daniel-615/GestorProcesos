from Proceso import Proceso
from Grafico import Grafico
import concurrent.futures
import os
class GestorProcesos:
    def __init__(self):
        self.pila_procesos=Grafico()
    
    def agregar_proceso(self, proceso):
        self.pila_procesos.apilar(proceso)

    def ejecutar_procesos(self, max_cores):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_cores) as executor:
            futuros = []
            while not self.pila_procesos.esta_vacia():
                proceso = self.pila_procesos.desapilar()
                if proceso:
                    futuro = executor.submit(proceso.ejecutar)
                    futuros.append(futuro)
            
            for futuro in concurrent.futures.as_completed(futuros):
                futuro.result()

    def consulta_cores(self):
        self.cores = os.cpu_count()
        print(f"Tienes {self.cores} cores")
        cores = int(input("¿Cuántos cores deseas utilizar? "))
        return cores
    
    def visualizar(self):
        self.pila_procesos.visualizar_pila()

gestor = GestorProcesos()
cores = gestor.consulta_cores()

# Agregar procesos
for n in range(cores):
    comando=input("¿Qué tipo de comando deseas ejecutar?")
    gestor.agregar_proceso(Proceso("alta", f"Proceso {n+1}", comando))
    
# Visualizar antes de procesar
gestor.visualizar()

# Ejecutar procesos con el número de cores especificado
gestor.ejecutar_procesos(max_cores=cores)

