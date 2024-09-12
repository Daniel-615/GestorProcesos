import concurrent.futures
class RoundRobin:
    def __init__(self, c_p, c_p_b, gestor, quantum=2):
        self.cola_procesos = c_p
        self.cola_procesos_bloqueados = c_p_b
        self.quantum = quantum
        self.gestor = gestor

    def ejecutar_procesos(self):
        """Por medio de hilos, invoca a la clase Evento para obtener los estados dependiendo 
        del nivel de recursos solicitado, y gestiona la ejecución con Quantum."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.gestor.getCores()) as executor:
            futuros = []
            procesos_completados = []
            while not self.cola_procesos.esta_vacia() or not self.cola_procesos_bloqueados.esta_vacia():
                proceso = (self.cola_procesos_bloqueados.desencolar() 
                           if not self.cola_procesos_bloqueados.esta_vacia() 
                           else self.cola_procesos.desencolar())

                if proceso:
                    evento = proceso.getEvento()

                    # Intentar desbloquear el proceso si está bloqueado
                    if evento.getEstado() == "Bloqueado":
                        if evento.intentar_desbloquear():
                            print(f"Proceso {proceso.getProceso()} desbloqueado y movido a Listo.")
                            self.cola_procesos.encolar(proceso)
                            continue

                    if evento.getEstado() == "Nuevo":
                        self._manejar_proceso_nuevo(proceso, evento, executor, futuros)
                    elif evento.getEstado() == "Listo":
                        self._manejar_proceso_listo(proceso, evento, executor, futuros)
                    elif evento.getEstado() == "Ejecucion":
                        self._manejar_proceso_ejecucion(proceso, evento, executor, futuros)

            self._completar_futuros(futuros, procesos_completados)

        return procesos_completados

    def _manejar_proceso_nuevo(self, proceso, evento, executor, futuros):
        """Maneja el proceso en estado 'Nuevo', moviéndolo a través de los estados correspondientes."""
        self.gestor.mover_proceso_nuevo(proceso)
        evento.avanzarEstado(proceso)

        if evento.getEstado() == "Listo":
            self._manejar_proceso_listo(proceso, evento, executor, futuros)

    def _manejar_proceso_listo(self, proceso, evento, executor, futuros):
        """Maneja el proceso en estado 'Listo', ejecutándolo según el Quantum."""
        if proceso.rafaga_cpu > self.quantum:
            print(f"Ejecutando {proceso.getProceso()} por {self.quantum} segundos.")
            proceso.ejecutar_comando()
            proceso.rafaga_cpu -= self.quantum
            if proceso.rafaga_cpu>0:    
                self.cola_procesos.encolar(proceso)
                print(f"Proceso {proceso.getProceso()} reencolado con {proceso.rafaga_cpu:.2f} segundos restantes.")

        else:
            print(f"Ejecutando {proceso.getProceso()} por {proceso.rafaga_cpu:.2f} segundos.")
            proceso.ejecutar_comando()
            proceso.rafaga_cpu = 0
            evento.avanzarEstado(proceso)
            print(f"Proceso {proceso.getProceso()} ha terminado.")
        
        evento.avanzarEstado(proceso)

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
