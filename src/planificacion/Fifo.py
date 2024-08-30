import concurrent.futures

class Fifo:
    def __init__(self, c_p, c_p_b, max_cores, gestor):
        self.cola_procesos = c_p
        self.cola_procesos_bloqueados = c_p_b
        self.max_cores = max_cores
        self.gestor = gestor

    def ejecutar_procesos(self):
        """Por medio de hilos, invoca a la clase Evento para obtener los estados dependiendo 
        del nivel de recursos solicitado.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_cores) as executor:
            futuros = []
            procesos_completados = []

            while not self.cola_procesos.esta_vacia() or not self.cola_procesos_bloqueados.esta_vacia():
                proceso = (self.cola_procesos_bloqueados.desencolar() 
                           if not self.cola_procesos_bloqueados.esta_vacia() 
                           else self.cola_procesos.desencolar())

                if proceso:
                    evento = proceso.getEvento()

                    if evento.getEstado() == "Nuevo":
                        self._manejar_proceso_nuevo(proceso, evento, executor, futuros)

            self._completar_futuros(futuros, procesos_completados)

        return procesos_completados

    def _manejar_proceso_nuevo(self, proceso, evento, executor, futuros):
        """Maneja el proceso en estado 'Nuevo', moviéndolo a través de los estados correspondientes."""
        self.gestor.mover_proceso_nuevo(proceso)
        evento.avanzarEstado(proceso)

        if evento.getEstado() == "Listo":
            futuro = executor.submit(proceso.ejecutar)
            evento.avanzarEstado(proceso)
            futuros.append((futuro, proceso))

            if evento.getEstado() == "Ejecucion":
                proceso.ejecutar_comando()
                evento.avanzarEstado(proceso)
                print(f"Proceso {proceso.getProceso()} está en ejecución.")

                if evento.getEstado() == "Terminado":
                    print(f"Proceso {proceso.getProceso()} terminado.")

    def _completar_futuros(self, futuros, procesos_completados):
        """Asegura que todos los procesos en los futuros hayan sido completados."""
        for futuro, proceso in futuros:
            futuro.result() 
            evento = proceso.getEvento()

            if evento.getEstado() == "En ejecucion":
                evento.avanzarEstado(proceso)

            procesos_completados.append(proceso)
            print(f"Proceso completado: {proceso.getProceso()}")
