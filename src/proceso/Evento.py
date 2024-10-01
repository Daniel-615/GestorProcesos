from proceso.Recursos import Recursos
from proceso.Json import Json
from output.Voz import Voz

class Evento():
    contador = 0

    def __init__(self,gestor,proceso):
        Evento.contador += 1
        self.numero_evento = Evento.contador
        self.setEstadoNuevo()
        self.recursos = Recursos()
        self.gestor=gestor
        self.voz=Voz()
        self.proceso=proceso

    def getEstado(self):
        return self.estado
    
    """Defino los métodos para cada Estado, Nuevo, Listo, Bloqueado, Terminado, En ejecución.
    """
    def setEstadoNuevo(self):
        self.estado = "Nuevo"
    
    def setEstadoListo(self):
        cpu = self.recursos.obtener_uso_cpu()
        memoria = self.recursos.obtener_info_memoria()
 
        if cpu < 80 and memoria > 2:  
            self.estado = "Listo"
            message=f"El {self.proceso} ha entrado en estado {self.estado}"
            self.voz.hablar(message)
        else:
            self.setEstadoBlock()

    def setEstadoBlock(self):
        self.estado = "Bloqueado"
        message=f"El {self.proceso} ha entrado en estado {self.estado}"
        self.voz.hablar(message)    
    def setEstadoTerminado(self):
        self.estado = "Terminado"
        message=f"El {self.proceso} ha sido {self.estado}."
        self.voz.hablar(message)
    
    def setEstadoEjecucion(self):
        """Cambia estado a ejecución, dependiendo el nivel de recursos disponibles que tenga.
        """
        cpu = self.recursos.obtener_uso_cpu()
        memoria = self.recursos.obtener_info_memoria()
        if cpu < 50 and memoria > 4: 
            self.estado = "Ejecucion"
            message=f"El {self.proceso} ha entrado en estado {self.estado}"
            self.voz.hablar(message)
        else:
            self.setEstadoBlock()
    def intentar_desbloquear(self):
        """Revisa si el proceso bloqueado puede ser desbloqueado.
        """
        cpu = self.recursos.obtener_uso_cpu()
        memoria = self.recursos.obtener_info_memoria()
        if cpu < 80 and memoria > 2:
            self.setEstadoListo()
            message=f"El {self.proceso} ha sido desbloqueado"
            self.voz.hablar(message)
            return True
        return False
    def visualizarColaEvento(self,gestor):
        json_config=Json()
        try:
            json_config.cargar_configuracion()
            
            if json_config.getColas() == True:
                if self.getEstado() == "Nuevo":
                    gestor.visualizar(5)
                elif self.getEstado() == "Listo":
                    gestor.visualizar(6)
                elif self.getEstado() == "Ejecucion":
                    gestor.visualizar(7)
                elif self.getEstado() == "Bloqueado":
                    gestor.visualizar(8)
            else:
                return 
        except Exception as e:
            raise ValueError(e)
        
        
        
    def avanzarEstado(self,proceso):
        """Avanza el estado, encola y desencola dependiendo el estado en que se encuentre.
        """
        try:
            cpu=self.recursos.obtener_uso_cpu()
            memoria=self.recursos.obtener_info_memoria()
            gestor=self.gestor
            cola_proceso_listo=gestor.getProcesosListos()
            cola_proceso_nuevo=gestor.getProcesosNuevos()
            cola_proceso_ejecucion=gestor.getProcesosEjecucion()
            if self.estado == "Nuevo" and not gestor.getColaProcesos(1).esta_vacia():
                self.setEstadoListo()
                gestor.mover_proceso_listo(proceso)
                self.visualizarColaEvento(gestor)
                cola_proceso_nuevo.desencolar()
            elif self.estado == "Listo" and not gestor.getColaProcesos(2).esta_vacia():
                if cpu<50 and memoria >4:
                    self.setEstadoEjecucion()
                    gestor.mover_proceso_ejecucion(proceso)
                    self.visualizarColaEvento(gestor)
                    cola_proceso_listo.desencolar()
                else:
                    self.setEstadoBlock()
                    gestor.mover_proceso_bloqueado(proceso)
            elif self.estado == "Ejecucion" and not gestor.getColaProcesos(3).esta_vacia():
                self.setEstadoTerminado()
                cola_proceso_ejecucion.desencolar()
        except Exception as e:
            print("Error al avanzar estado: ",e)
