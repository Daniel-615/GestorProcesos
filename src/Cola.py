class Cola:
    contador=0
    def __init__(self):
        Cola.contador=1
        self.cola = []
    @classmethod
    def getContador(self):
        return Cola.contador
    def encolar(self, proceso):
        Cola.contador+=1
        self.cola.append(proceso)
        print(f"Proceso {proceso.proceso} encolado con prioridad {proceso.prioridad}")

    def desencolar(self):
        if self.cola:
            return self.cola.pop(0)  
        else:
            return None  
    def esta_vacia(self):
        return len(self.cola) == 0
    
    def obtener_procesos(self):
        return self.cola
