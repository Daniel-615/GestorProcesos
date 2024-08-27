from Proceso import Proceso
from Grafico import Grafico
import concurrent.futures
import os
class GestorProcesos:
    def __init__(self):
        self.cola_procesos=Grafico()
        self.cola_procesos_nuevos=Grafico()
        self.cola_procesos_listos=Grafico()  
        self.cola_procesos_ejecucion=Grafico()
        self.cola_procesos_bloqueados=Grafico() 
    #Métodos Get y Set    
    def getCores(self):
        return self.cores
    def getProcesosNuevos(self):
        return self.cola_procesos_nuevos
    def getProcesosListos(self):
        return self.cola_procesos_listos
    def getProcesosEjecucion(self):
        return self.cola_procesos_bloqueados
    def getProcesos(self):
        return self.cola_procesos
        
    def agregar_proceso(self, proceso):
        self.cola_procesos.encolar(proceso)
    def mover_proceso_nuevo(self,proceso):
        self.cola_procesos_nuevos.encolar(proceso)
    def mover_proceso_listo(self,proceso):
        self.cola_procesos_listos.encolar(proceso)
    def mover_proceso_ejecucion(self,proceso):
        self.cola_procesos_ejecucion.encolar(proceso)
    def mover_proceso_bloqueados(self,proceso):
        self.cola_procesos_bloqueados.encolar(proceso)
    def desbloquear_proceso(self):
        if not self.cola_procesos_bloqueados.esta_vacia():
            proceso = self.cola_procesos_bloqueados.desencolar()
            self.mover_proceso_listo(proceso)    


    def ejecutar_procesos(self, max_cores):
        """Por medio de hilos, invoca a la clase Evento para obtener los estados dependiendo 
        el nivel de recursos en que solicite.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_cores) as executor:
            futuros = []
            procesos_completados = []

            while not self.cola_procesos.esta_vacia():
                proceso = self.cola_procesos.desencolar()
                if proceso:
                    evento = proceso.getEvento()
                    if evento.getEstado() == "Nuevo":
                        self.mover_proceso_nuevo(proceso)
                        evento.avanzarEstado(proceso)
                        if evento.getEstado()=="Listo":
                            futuro=executor.submit(proceso.ejecutar)
                            evento.avanzarEstado(proceso)
                            futuros.append((futuro,proceso))
                            if evento.getEstado()=="Ejecucion":
                                proceso.ejecutar_comando()
                                evento.avanzarEstado(proceso)
                                print(f"Proceso {proceso.getProceso()} está en ejecución.")
                                if evento.getEstado()=="Terminado":
                                    print(f"Proceso {proceso.getProceso()} terminado.")
                                    procesos_completados.append(proceso)
                    
            # Asegurarse de que todos los procesos han sido completados
            for futuro, proceso in futuros:
                futuro.result() 
                evento = proceso.getEvento()
                if evento.getEstado() == "En ejecucion":
                    evento.avanzarEstado()  
                procesos_completados.append(proceso)
                print("Proceso completado:", proceso.getProceso())
        
        return procesos_completados

    def consulta_cores(self):
        self.cores = os.cpu_count()
        print(f"Tienes {self.cores} cores")
        cores = int(input("¿Cuántos cores deseas utilizar? "))
        return cores
    
    def visualizar(self,num):
        if num==1:
            self.cola_procesos.visualizar_cola('visualizacion_cola')
        elif num==2:
            self.cola_procesos_nuevos.visualizar_cola('cola_nuevos')
        elif num==3:
            self.cola_procesos_listos.visualizar_cola('cola_listos')
        elif num==4:
            self.cola_procesos_ejecucion.visualizar_cola('cola_ejecucion')
        else:
            print("No has seleccionado una opción valida.")
gestor = GestorProcesos()
cores = gestor.consulta_cores()
# Agregar procesos
while True:
    action = input("¿Deseas agregar un nuevo proceso o empezar la ejecución? (agregar/empezar): ").strip().lower()
    
    if action == "agregar":
        if gestor.cola_procesos.contador <= cores:
            lista_comandos = Proceso.devolver_comandos()
            print(f"""
                  Lista Comandos:
                  {lista_comandos}
                  """)
            comando = input("¿Qué tipo de comando deseas ejecutar?: ")
            prioridad = input("¿Tipo de prioridad?: ")
            gestor.agregar_proceso(Proceso(prioridad, f"Proceso {gestor.cola_procesos.contador}", comando,gestor))
        else:
            print("Has alcanzado el número máximo de cores.")
    elif action == "empezar":
        if gestor.cola_procesos.contador > 0:
            # Visualizar antes de procesar
            gestor.visualizar(1)
            # Ejecutar procesos con el número de cores especificado
            gestor.ejecutar_procesos(max_cores=cores)
            num_decision=int(input("¿Deseas ver alguna cola? (Cola nuevos (2)/ Cola listos (3)/ Cola en ejecución (4)):"))
            gestor.visualizar(num_decision)
        else:
            print("No hay procesos en la cola. Agrega al menos un proceso antes de empezar.")
    else:
        print("Opción no válida, por favor ingresa 'agregar' o 'empezar'.")