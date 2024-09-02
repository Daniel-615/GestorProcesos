class Cola:
    contador = 0

    def __init__(self):
        Cola.contador = 1
        self.cola = []

    @classmethod
    def getContador(cls):
        return Cola.contador

    def encolar(self, proceso):
        Cola.contador += 1
        self.cola.append(proceso)
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
        """Ordena solo los procesos que tienen tipo_planificacion igual a 'SJF' por tiempo de ráfaga en orden ascendente."""
        sjf_procesos = [p for p in self.cola if p.tipo_planificacion == 'SJF']
        no_sjf_procesos = [p for p in self.cola if p.tipo_planificacion != 'SJF']

        # Ordenar solo los procesos SJF
        sjf_procesos.sort(key=lambda proceso: proceso.rafaga_cpu)

        # Actualizar la cola combinando los procesos no SJF y los SJF ordenados
        self.cola = no_sjf_procesos + sjf_procesos
