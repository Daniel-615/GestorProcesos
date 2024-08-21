class Cola:
    def __init__(self):
        self.cola = []

    def encolar(self, proceso):
        self.cola.append(proceso)
        print(f"Proceso {proceso.proceso} encolado con prioridad {proceso.prioridad}")

    def desencolar(self):
        if self.cola:
            return self.cola.pop(0)  # Elimina y retorna el primer elemento de la cola
        else:
            return None  

    def esta_vacia(self):
        return len(self.cola) == 0
    
    def obtener_procesos(self):
        return self.cola
