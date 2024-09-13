import concurrent.futures
import heapq  

class PriorityScheduling:
    def __init__(self, c_p, c_p_b, gestor):
        self.cola_procesos = c_p
        self.cola_procesos_bloqueados = c_p_b
        self.gestor = gestor

    def ejecutar_procesos(self):
        """Por medio de hilos, invoca a la clase Evento para obtener los estados dependiendo 
        del nivel de recursos solicitado, y gestiona la ejecución basándose en prioridades.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.gestor.getCores()) as executor:
            futuros = []
            procesos_completados = []
            cola_prioridad = []

            while not self.cola_procesos.esta_vacia() or not self.cola_procesos_bloqueados.esta_vacia() or cola_prioridad:
               
                self._intentar_desbloquear_procesos()

                # Agregar procesos de la cola de procesos a la cola de prioridad
                while not self.cola_procesos.esta_vacia():
                    proceso = self.cola_procesos.desencolar()
                    if proceso.prioridad =="alta":
                        heapq.heappush(cola_prioridad,(1,proceso))
                    if proceso.prioridad=="media":
                        heapq.heappush(cola_prioridad,(2,proceso))
                    if proceso.prioridad=="baja":
                        heapq.heappush(cola_prioridad,(3,proceso))  

                # Desencolar el proceso con la prioridad más alta (heapq devuelve el de menor valor)
                if cola_prioridad:
                    _, proceso = heapq.heappop(cola_prioridad)
                    evento = proceso.getEvento()

                    if evento.getEstado() == "Nuevo":
                        self._manejar_proceso_nuevo(proceso, evento, executor, futuros)
                    elif evento.getEstado() == "Listo":
                        self._manejar_proceso_listo(proceso, evento, executor, futuros)
                    elif evento.getEstado() == "Ejecucion":
                        self._manejar_proceso_ejecucion(proceso, evento, executor, futuros)

            self._completar_futuros(futuros, procesos_completados)

        return procesos_completados

    def _intentar_desbloquear_procesos(self):
        """Intenta desbloquear todos los procesos en la cola de bloqueados."""
        procesos_a_reinsertar = []

        while not self.cola_procesos_bloqueados.esta_vacia():
            proceso = self.cola_procesos_bloqueados.desencolar()
            evento = proceso.getEvento()

            if evento.intentar_desbloquear():
                procesos_a_reinsertar.append(proceso)
            else:
                self.cola_procesos_bloqueados.encolar(proceso)

        for proceso in procesos_a_reinsertar:
            self.cola_procesos.encolar(proceso)

    def _manejar_proceso_nuevo(self, proceso, evento, executor, futuros):
        """Maneja el proceso en estado 'Nuevo', moviéndolo a través de los estados correspondientes."""
        self.gestor.mover_proceso_nuevo(proceso)
        evento.avanzarEstado(proceso)

        if evento.getEstado() == "Listo":
            self._manejar_proceso_listo(proceso, evento, executor, futuros)

    def _manejar_proceso_listo(self, proceso, evento, executor, futuros):
        """Maneja el proceso en estado 'Listo', ejecutándolo basado en su prioridad."""
        print(f"Ejecutando proceso {proceso.getProceso()} con prioridad {proceso.prioridad}.")
        proceso.ejecutar_comando()
        evento.avanzarEstado(proceso)

        if evento.getEstado() == "Terminado":
            print(f"Proceso {proceso.getProceso()} ha terminado.")
        else:
            futuros.append((executor.submit(proceso.ejecutar), proceso))

    def _manejar_proceso_ejecucion(self, proceso, evento, executor, futuros):
        """Maneja el proceso en estado 'Ejecución', ejecutando comandos y avanzando estados."""
        proceso.ejecutar_comando()
        evento.avanzarEstado(proceso)
        print(f"Proceso {proceso.getProceso()} está en ejecución.")

        if proceso.ha_fallado():
            print(f"Proceso {proceso.getProceso()} ha fallado y se moverá a bloqueados.")
            self.gestor.mover_proceso_bloqueado(proceso)
            self.cola_procesos_bloqueados.encolar(proceso)  
        elif evento.getEstado() == "Terminado":
            print(f"Proceso {proceso.getProceso()} ha terminado.")
        else:
            futuros.append((executor.submit(proceso.ejecutar), proceso))

    def _completar_futuros(self, futuros, procesos_completados):
        """Asegura que todos los procesos en los futuros hayan sido completados."""
        for futuro, proceso in futuros:
            futuro.result() 
            evento = proceso.getEvento()

            if evento.getEstado() == "Ejecucion":
                evento.avanzarEstado(proceso)

            procesos_completados.append(proceso)
            print(f"Proceso completado: {proceso.getProceso()}")
