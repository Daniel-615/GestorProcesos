from Proceso import Proceso
from Grafico import Grafico

import os

from planificacion import FIFO, RoundRobin
class GestorProcesos:
    def __init__(self):
        self.cola_procesos = Grafico()
        self.cola_procesos_nuevos = Grafico()
        self.cola_procesos_listos = Grafico()  
        self.cola_procesos_ejecucion = Grafico()
        self.cola_procesos_bloqueados = Grafico()
        self.cores = None

    # Métodos Get y Set    
    def getCores(self):
        return self.cores

    def getProcesosNuevos(self):
        return self.cola_procesos_nuevos

    def getProcesosListos(self):
        return self.cola_procesos_listos

    def getProcesosEjecucion(self):
        return self.cola_procesos_ejecucion

    def getProcesos(self):
        return self.cola_procesos

    def agregar_proceso(self, proceso):
        self.cola_procesos.encolar(proceso)

    def mover_proceso_nuevo(self, proceso):
        self.cola_procesos_nuevos.encolar(proceso)

    def mover_proceso_listo(self, proceso):
        self.cola_procesos_listos.encolar(proceso)

    def mover_proceso_ejecucion(self, proceso):
        self.cola_procesos_ejecucion.encolar(proceso)

    def mover_proceso_bloqueado(self, proceso):
        self.cola_procesos_bloqueados.encolar(proceso)

    def desbloquear_proceso(self):
        if not self.cola_procesos_bloqueados.esta_vacia():
            proceso = self.cola_procesos_bloqueados.desencolar()
            self.mover_proceso_listo(proceso)
    
    # FIFO
    def ejecutar_fifo(self, cores):
        fifo_planificador = FIFO.Fifo(
            c_p=self.cola_procesos,
            c_p_b=self.cola_procesos_bloqueados,
            max_cores=cores,
            gestor=self
        )
        fifo_planificador.ejecutar_procesos()
    #RoundRobin
    def ejecutar_robin(self):
        robin_planificador=RoundRobin.RoundRobin(
            c_p=self.cola_procesos,
            c_p_b=self.cola_procesos_bloqueados,
            gestor=self
        )
        robin_planificador.ejecutar_procesos()

    def consulta_cores(self):
        self.cores = os.cpu_count()
        print(f"Tienes {self.cores} cores disponibles.")
        while True:
            try:
                cores = int(input("¿Cuántos cores deseas utilizar? "))
                if cores > 0 and cores <= self.cores:
                    return cores
                else:
                    print(f"Por favor, ingresa un número entre 1 y {self.cores}.")
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número.")

    def visualizar(self, num):
        if num == 1:
            self.cola_procesos.visualizar_cola('visualizacion_cola')
        elif num == 2:
            self.cola_procesos_nuevos.visualizar_cola('cola_nuevos')
        elif num == 3:
            self.cola_procesos_listos.visualizar_cola('cola_listos')
        elif num == 4:
            self.cola_procesos_ejecucion.visualizar_cola('cola_ejecucion')
        else:
            print("No has seleccionado una opción válida.")

def main():
    gestor = GestorProcesos()
    cores = gestor.consulta_cores()

    while True:
        action = input("¿Deseas agregar un nuevo proceso o empezar la ejecución? (agregar/empezar): ").strip().lower()

        if action == "agregar":
            if gestor.cola_procesos.contador <= cores:
                lista_comandos = Proceso.devolver_comandos()
                print(f"Lista de Comandos:\n{lista_comandos}\n")
                comando = input("¿Qué tipo de comando deseas ejecutar?: ")
                prioridad = input("¿Tipo de prioridad? (baja/media/alta): ").strip().lower()
                
                if prioridad in ["baja", "media", "alta"]:
                    planificacion = input("¿Tipo de Planificación? (FIFO/Robin/SJF/Priority): ").strip().lower()
                    if planificacion in ["fifo", "robin", "sjf", "priority"]:
                        proceso = Proceso(
                            prioridad, 
                            f"Proceso {gestor.cola_procesos.contador}", 
                            comando, 
                            gestor, 
                            planificacion
                        )
                        gestor.agregar_proceso(proceso)
                    else: 
                        print("Error: La planificación ingresada no es válida.")
                else: 
                    print("Error: La prioridad ingresada no es válida.")
            else:
                print(f"Has alcanzado el número máximo de procesos asignados a {cores} cores.")
        elif action == "empezar":
            if gestor.cola_procesos.contador > 0:
                gestor.visualizar(1)
                if planificacion=="fifo":
                    gestor.ejecutar_fifo(cores)
                if planificacion=="robin":
                    gestor.ejecutar_robin()
                if planificacion=="sjf":
                    pass
                if planificacion=="priority":
                    pass 
                try:
                    num_decision = int(input("¿Deseas ver alguna cola? (Cola nuevos (2)/ Cola listos (3)/ Cola en ejecución (4)): "))
                    gestor.visualizar(num_decision)
                except ValueError:
                    print("Entrada no válida. Debes ingresar un número.")
            else:
                print("No hay procesos en la cola. Agrega al menos un proceso antes de empezar.")
        else:
            print("Opción no válida, por favor ingresa 'agregar' o 'empezar'.")

if __name__ == "__main__":
    main()
