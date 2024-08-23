from Proceso import Proceso
from Grafico import Grafico
import concurrent.futures
import os
class GestorProcesos:
    def __init__(self):
        self.cola_procesos=Grafico()
        self.cola_procesos_listos=Grafico()  #implementar esta funcionalidad
        self.cola_procesos_bloqueados=Grafico() #implementar esta funcionalidad
        
    def getCores(self):
        return self.cores
    def agregar_proceso(self, proceso):
        self.cola_procesos.encolar(proceso)
    def mover_proceso_listo(self,proceso):
        self.cola_procesos_listos.encolar(proceso)
    def mover_proceso_bloqueados(self,proceso):
        self.cola_procesos_bloqueados.encolar(proceso)
    def desbloquear_proceso(self):
        if not self.cola_procesos_bloqueados.esta_vacia():
            proceso = self.cola_procesos_bloqueados.desencolar()
            self.mover_proceso_listo(proceso)    


    def ejecutar_procesos(self, max_cores):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_cores) as executor:
            futuros = []
            procesos_completados = []

            while not self.cola_procesos.esta_vacia():
                proceso = self.cola_procesos.desencolar()
                if proceso:
                    evento = proceso.getEvento()
                    if evento.getEstado() == "Nuevo":
                        evento.avanzarEstado()
                        if evento.getEstado()=="Listo":
                            futuro=executor.submit(proceso.ejecutar)
                            evento.avanzarEstado()
                            futuros.append((futuro,proceso))
                            if evento.getEstado()=="Ejecucion":
                                proceso.ejecutar_comando()
                                evento.avanzarEstado()
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
    
    def visualizar(self):
        self.cola_procesos.visualizar_cola()

gestor = GestorProcesos()
cores = gestor.consulta_cores()
# Agregar procesos
for n in range(cores):
    if cores > gestor.getCores():
        print("Te has excedido de cores.")
        break
    else: 
            lista_comandos=Proceso.devolver_comandos()
            print(f"""
                    Lista Comandos:
                  {lista_comandos}
                  """)
            comando=input("¿Qué tipo de comando deseas ejecutar?: ")
            prioridad=input("¿Tipo de prioridad?: ")
            gestor.agregar_proceso(Proceso(prioridad, f"Proceso {n+1}", comando))
# Visualizar antes de procesar
gestor.visualizar()
# Ejecutar procesos con el número de cores especificado
gestor.ejecutar_procesos(max_cores=cores)

