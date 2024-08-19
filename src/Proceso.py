import time
class Proceso:
    contador=0
    def __init__(self,prioridad,proceso,tipo_proceso):
        self.contador+=1
        self.prioridad=prioridad
        self.proceso=proceso
        self.tipo_proceso=tipo_proceso
    def ejecutar(self):
        if self.prioridad=="alta":
            self.tiempo=2
        if self.prioridad=="media":
            self.tiempo=4
        if self.prioridad=="baja":
            self.tiempo=8
        print(f"ejecutando proceso con prioridad {self.prioridad} tipo: ({self.tipo_proceso}) ")
        time.sleep(self.tiempo)
        print(f"Proceso {self.proceso} completado en {self.tiempo} segundos")
