class Evento():
    contador=0
    def __init__(self):
        self.contador+=1
        self.numero_evento=Evento.contador
        self.estado="Nuevo"
    def setEstado(self,estado):
        self.estado=estado
    def getEstado(self):
        return self.estado