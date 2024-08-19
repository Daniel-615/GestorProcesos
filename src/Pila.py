class Pila:
    def __init__(self):
        self.pila = []

    def apilar(self, proceso):
        self.pila.append(proceso)
        print(f"Proceso {proceso.proceso} apilado con prioridad {proceso.prioridad}")
    #Lifo
    def desapilar(self):
        if self.pila:
            return self.pila.pop() 
        else:
            return None  

    def esta_vacia(self):
        return len(self.pila) == 0
    
    def obtener_procesos(self):
        return self.pila
