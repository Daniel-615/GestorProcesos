class Cola:
    contador = 0

    def __init__(self):
        Cola.contador = 1
        self.cola = []

    @classmethod
    def getContador(cls):
        return Cola.contador
    def setLog(self,log,title):
        self.log=log
        self.title=title
    def getLog(self):
        return self.log
    def encolar(self, proceso):
        Cola.contador += 1
        self.cola.append(proceso)
        log=self.getLog()
        message=f"Proceso {proceso.proceso} tipo {self.title} encolado con prioridad {proceso.prioridad}"
        log.log_info(message)
        print(f"Proceso {proceso.proceso} encolado con prioridad {proceso.prioridad}")

    def desencolar(self):
        if self.cola:
            self.contador-=1
            return self.cola.pop(0)
        else:
            return None

    def esta_vacia(self):
        return len(self.cola) == 0

    def obtener_procesos(self):
        return self.cola

    def ordenar_por_rafaga(self):
        """Ordena los procesos en la cola por la duración de ráfaga (SJF)."""
        procesos = self.obtener_procesos()
        procesos.sort(key=lambda p: p.rafaga_cpu)
        self.procesos = procesos  