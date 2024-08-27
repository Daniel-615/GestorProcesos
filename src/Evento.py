from Recursos import Recursos

class Evento():
    contador = 0

    def __init__(self,gestor):
        Evento.contador += 1
        self.numero_evento = Evento.contador
        self.setEstadoNuevo()
        self.recursos = Recursos()
        self.gestor=gestor
        

    def getEstado(self):
        return self.estado
    
    """Defino los métodos para cada Estado, Nuevo, Listo, Bloqueado, Terminado, En ejecución."""
    def setEstadoNuevo(self):
        self.estado = "Nuevo"
    
    def setEstadoListo(self):
        cpu = self.recursos.obtener_uso_cpu()
        memoria = self.recursos.obtener_info_memoria()
 
        if cpu < 80 and memoria > 2:  
            self.estado = "Listo"
        else:
            self.estado = "Bloqueado"

    def setEstadoBlock(self):
        self.estado = "Bloqueado"
    
    def setEstadoTerminado(self):
        self.estado = "Terminado"
    
    def setEstadoEjecucion(self):
        cpu = self.recursos.obtener_uso_cpu()
        memoria = self.recursos.obtener_info_memoria()
        if cpu < 50 and memoria > 4: 
            self.estado = "Ejecucion"
        else:
            self.setEstadoBlock()
    
    def avanzarEstado(self,proceso):
        """Avanza el estado, encola y desencola dependiendo el estado en que se encuentre.
        """
        try:
            gestor=self.gestor
            cola_proceso_listo=gestor.getProcesosListos()
            cola_proceso_nuevo=gestor.getProcesosNuevos()
            cola_proceso_ejecucion=gestor.getProcesosEjecucion()
            if self.estado == "Nuevo":
                self.setEstadoListo()
                gestor.mover_proceso_listo(proceso)
                cola_proceso_nuevo.desencolar()
            elif self.estado == "Listo":
                self.setEstadoEjecucion()
                gestor.mover_proceso_ejecucion(proceso)
                cola_proceso_listo.desencolar()
            elif self.estado == "Ejecucion":
                self.setEstadoTerminado()
                cola_proceso_ejecucion.desencolar()
        except Exception as e:
            print("Error al avanzar estado: ",e)
