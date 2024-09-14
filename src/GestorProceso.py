from proceso.Grafico import Grafico
import os

from planificacion import FIFO, RoundRobin, SJF, PriorityScheduling as Prioridad  
class GestorProcesos:
    def __init__(self):
        self.cola_fifo = Grafico()  
        self.cola_rr = Grafico()  
        self.cola_sjf = Grafico()   
        self.cola_priority = Grafico()  
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
        # Dependiendo del tipo de planificación, el proceso será agregado a su cola correspondiente
        if proceso.tipo_planificacion== 'fifo':
            self.cola_fifo.encolar(proceso)
        elif proceso.tipo_planificacion == 'robin':
            self.cola_rr.encolar(proceso)
        elif proceso.tipo_planificacion == 'sjf':
            self.cola_sjf.encolar(proceso)
        elif proceso.tipo_planificacion == 'priority':
            self.cola_priority.encolar(proceso)
        else:
            print("Tipo de planificación no válida.")

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

    def getColaProcesos(self, decision):
        if decision == 1:
            return self.getProcesosNuevos()
        elif decision == 2:
            return self.getProcesosListos()
        elif decision == 3:
            return self.getProcesosEjecucion()
        elif decision == 4:
            return self.getProcesos()
        else:
            print("Decisión no válida, por favor selecciona un número entre 1 y 4.")
            return None

    # FIFO
    def ejecutar_fifo(self, cores):
        fifo_planificador = FIFO.Fifo(
            c_p=self.cola_fifo, 
            c_p_b=self.cola_procesos_bloqueados,
            max_cores=cores,
            gestor=self
        )
        fifo_planificador.ejecutar_procesos()

    # RoundRobin
    def ejecutar_robin(self):
        robin_planificador = RoundRobin.RoundRobin(
            c_p=self.cola_rr, 
            c_p_b=self.cola_procesos_bloqueados,
            gestor=self
        )
        robin_planificador.ejecutar_procesos()

    # SJF
    def ejecutar_sjf(self):
        sjf_planificador = SJF.SJF(
            c_p=self.cola_sjf, 
            c_p_b=self.cola_procesos_bloqueados,
            gestor=self
        )
        sjf_planificador.ejecutar_procesos()

    # Prioridad
    def ejecutar_priority(self):
        prioridad_planificador = Prioridad.PriorityScheduling(
            c_p=self.cola_priority,  
            c_p_b=self.cola_procesos_bloqueados,
            gestor=self
        )
        prioridad_planificador.ejecutar_procesos()

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
            self.cola_fifo.visualizar_cola('visualizacion_cola_fifo','FIFO')
        elif num == 2:
            self.cola_rr.visualizar_cola('visualizacion_cola_rr','ROUND ROBIN')
        elif num == 3:
            self.cola_sjf.visualizar_cola('visualizacion_cola_sjf','SJF')
        elif num == 4:
            self.cola_priority.visualizar_cola('visualizacion_cola_prioridad','PRIORIDAD')
        elif num==5:
            self.cola_procesos_nuevos.visualizar_cola('visualizacion_cola_nuevos','NUEVOS')
        elif num==6:
            self.cola_procesos_listos.visualizar_cola('visualizacion_cola_listos','LISTOS')
        elif num==7:
            self.cola_procesos_ejecucion.visualizar_cola('visualizacion_cola_ejecucion','EJECUCION')
        elif num==8:
            self.cola_procesos_bloqueados.visualizar_cola('visualizacion_cola_bloqueados','BLOQUEADOS')
        else:
            print("No has seleccionado una opción válida.")