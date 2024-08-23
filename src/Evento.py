from Recursos import Recursos

class Evento():
    contador = 0

    def __init__(self):
        Evento.contador += 1
        self.numero_evento = Evento.contador
        self.setEstadoNuevo()
        self.recursos = Recursos()

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
    
    def avanzarEstado(self):
        if self.estado == "Nuevo":
            self.setEstadoListo()
        elif self.estado == "Listo":
            self.setEstadoEjecucion()
        elif self.estado == "Ejecucion":
            self.setEstadoTerminado()
