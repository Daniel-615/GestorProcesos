import concurrent.futures
class SJF:
    def __init__(self, c_p, c_p_b, gestor):
        self.cola_procesos = c_p
        self.cola_procesos_bloqueados = c_p_b
        self.gestor = gestor

    def ejecutar_procesos(self):
        """Por medio de hilos, invoca a la clase Evento para obtener los estados dependiendo 
        del nivel de recursos solicitado, y gestiona la ejecución según SJF."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.gestor.getCores()) as executor:
            procesos_completados = []
            while not self.cola_procesos.esta_vacia() or not self.cola_procesos_bloqueados.esta_vacia():
                # Intentar desbloquear procesos antes de procesar la siguiente cola
                self._intentar_desbloquear_procesos()

                # Ordenar los procesos por el tiempo de ráfaga más corto
                self.cola_procesos.ordenar_por_rafaga()

                # Procesar los procesos en cola
                while not self.cola_procesos.esta_vacia():
                    proceso = self.cola_procesos.desencolar()
                    evento = proceso.getEvento()

                    if evento.getEstado() == "Nuevo":
                        self._manejar_proceso_nuevo(proceso, evento, executor)
                    elif evento.getEstado() == "Listo":
                        self._manejar_proceso_listo(proceso, evento, executor)
                    elif evento.getEstado() == "Ejecucion":
                        self._manejar_proceso_ejecucion(proceso, evento, executor)

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

    def _manejar_proceso_nuevo(self, proceso, evento, executor):
        """Maneja el proceso en estado 'Nuevo', moviéndolo a través de los estados correspondientes."""
        self.gestor.mover_proceso_nuevo(proceso)
        evento.avanzarEstado(proceso)

        if evento.getEstado() == "Listo":
            self._manejar_proceso_listo(proceso, evento, executor)

    def _manejar_proceso_listo(self, proceso, evento, executor):
        """Maneja el proceso en estado 'Listo'."""
        print(f"Ejecutando {proceso.getProceso()} con ráfaga de {proceso.rafaga_cpu:.2f} segundos.")
        proceso.ejecutar_comando()
        proceso.rafaga_cpu = 0
        evento.avanzarEstado(proceso)
        print(f"Proceso {proceso.getProceso()} ha terminado.")
        
        if evento.getEstado() == "Terminado":
            print(f"Proceso {proceso.getProceso()} completado y terminado.")

    def _manejar_proceso_ejecucion(self, proceso, evento, executor):
        """Maneja el proceso en estado 'Ejecución', ejecutando comandos y avanzando estados."""
        proceso.ejecutar_comando()
        evento.avanzarEstado(proceso)
        print(f"Proceso {proceso.getProceso()} está en ejecución.")

        if proceso.ha_fallado():
            print(f"Proceso {proceso.getProceso()} ha fallado y se moverá a bloqueados.")
            self.gestor.mover_proceso_bloqueado(proceso)
        elif evento.getEstado() == "Terminado":
            print(f"Proceso {proceso.getProceso()} ha terminado.")
