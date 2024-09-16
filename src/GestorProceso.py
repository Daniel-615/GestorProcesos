from proceso.Grafico import Grafico
import os
from Log import Log
from planificacion import FIFO, RoundRobin, SJF, PriorityScheduling as Prioridad

class GestorProcesos:
    def __init__(self):
        self.log = Log()
        self.cola_fifo = Grafico(self.log, "FIFO")
        self.cola_rr = Grafico(self.log, "ROUND ROBIN")
        self.cola_sjf = Grafico(self.log, "SJF")
        self.cola_priority = Grafico(self.log, "PRIORIDAD")
        self.cola_procesos_nuevos = Grafico(self.log, "NUEVOS")
        self.cola_procesos_listos = Grafico(self.log, "LISTOS")
        self.cola_procesos_ejecucion = Grafico(self.log, "EJECUCION")
        self.cola_procesos_bloqueados = Grafico(self.log, "BLOQUEADOS")
        self.cores = None

    # Métodos Get y Set
    def getLog(self):
        return self.log

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
        if proceso.tipo_planificacion == 'fifo':
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
    def ejecutar_fifo(self):
        cores = self.consulta_cores()
        fifo_planificador = FIFO.Fifo(
            c_p=self.cola_fifo,
            c_p_b=self.cola_procesos_bloqueados,
            max_cores=cores,
            gestor=self
        )
        fifo_planificador.ejecutar_procesos()

    # RoundRobin
    def ejecutar_robin(self):
        cores = self.consulta_cores()
        robin_planificador = RoundRobin.RoundRobin(
            c_p=self.cola_rr,
            c_p_b=self.cola_procesos_bloqueados,
            max_cores=cores,
            gestor=self
        )
        robin_planificador.ejecutar_procesos()

    # SJF
    def ejecutar_sjf(self):
        cores = self.consulta_cores()
        sjf_planificador = SJF.SJF(
            c_p=self.cola_sjf,
            c_p_b=self.cola_procesos_bloqueados,
            max_cores=cores,
            gestor=self
        )
        sjf_planificador.ejecutar_procesos()

    # Prioridad
    def ejecutar_priority(self):
        cores = self.consulta_cores()
        prioridad_planificador = Prioridad.PriorityScheduling(
            c_p=self.cola_priority,
            c_p_b=self.cola_procesos_bloqueados,
            max_cores=cores,
            gestor=self
        )
        prioridad_planificador.ejecutar_procesos()

    def consulta_cores(self):
        self.cores = os.cpu_count()
        if self.cores < 5:
            print(f"Advertencia: solo tienes {self.cores} cores disponibles. El programa intentará ejecutarse con esta cantidad.")
        else:
            print(f"Tienes {self.cores} cores disponibles.")
        
        # Usa hasta 5 cores, o menos si el sistema tiene menos de 5
        cores = min(5, self.cores)
        print(f"Usando {cores} cores.")
        return cores

    def visualizar(self, num):
        if num == 1:
            self.cola_fifo.visualizar_cola('visualizacion_cola_fifo', 'FIFO')
        elif num == 2:
            self.cola_rr.visualizar_cola('visualizacion_cola_rr', 'ROUND ROBIN')
        elif num == 3:
            self.cola_sjf.visualizar_cola('visualizacion_cola_sjf', 'SJF')
        elif num == 4:
            self.cola_priority.visualizar_cola('visualizacion_cola_prioridad', 'PRIORIDAD')
        elif num == 5:
            self.cola_procesos_nuevos.visualizar_cola('visualizacion_cola_nuevos', 'NUEVOS')
        elif num == 6:
            self.cola_procesos_listos.visualizar_cola('visualizacion_cola_listos', 'LISTOS')
        elif num == 7:
            self.cola_procesos_ejecucion.visualizar_cola('visualizacion_cola_ejecucion', 'EJECUCION')
        elif num == 8:
            self.cola_procesos_bloqueados.visualizar_cola('visualizacion_cola_bloqueados', 'BLOQUEADOS')
        else:
            print("No has seleccionado una opción válida.")
