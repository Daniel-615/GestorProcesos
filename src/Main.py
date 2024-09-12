from Proceso import Proceso
from GestorProceso import GestorProcesos

def agregar_proceso(gestor, cores, n):
    """Función para agregar un nuevo proceso a la cola."""
    
    # Verificar el número total de procesos en todas las colas
    total_procesos = (
        gestor.cola_fifo.contador +
        gestor.cola_rr.contador +
        gestor.cola_sjf.contador +
        gestor.cola_priority.contador
    )
    
    if total_procesos >= cores:
        print(f"Has alcanzado el número máximo de procesos asignados a {cores} cores.")
        return
    
    lista_comandos = Proceso.devolver_comandos()
    print(f"Lista de Comandos:\n{lista_comandos}\n")
    
    comando = input("¿Qué tipo de comando deseas ejecutar?: ").strip()
    prioridad = input("¿Tipo de prioridad? (baja/media/alta): ").strip().lower()
    
    if prioridad not in ["baja", "media", "alta"]:
        print("Error: La prioridad ingresada no es válida.")
        return

    planificacion = input("¿Tipo de Planificación? (FIFO/Robin/SJF/Priority): ").strip().lower()
    if planificacion not in ["fifo", "robin", "sjf", "priority"]:
        print("Error: La planificación ingresada no es válida.")
        return

    # Crear el nuevo proceso con los datos proporcionados
    proceso = Proceso(
        prioridad=prioridad, 
        proceso=f"Proceso {n}", 
        tipo_proceso=comando, 
        gestor=gestor, 
        tipo_planificacion=planificacion
    )
    
    # Agregar el proceso a la cola correspondiente
    gestor.agregar_proceso(proceso)
    print(f"Proceso {n} agregado correctamente a la cola de {planificacion.upper()}.")

def ejecutar_procesos_por_tipo(gestor, cores):
    """Función para ejecutar los procesos agrupados por su tipo de planificación."""
    
    total_procesos = (
        gestor.cola_fifo.contador +
        gestor.cola_rr.contador +
        gestor.cola_sjf.contador +
        gestor.cola_priority.contador
    )

    if total_procesos == 0:
        print("No hay procesos en la cola. Agrega al menos un proceso antes de empezar.")
        return

    # Ejecutar los procesos de acuerdo a su tipo de planificación
    if not gestor.cola_fifo.esta_vacia():
        print("Ejecutando procesos FIFO...")
        gestor.visualizar(1)
        gestor.ejecutar_fifo(cores)
        

    if not gestor.cola_rr.esta_vacia():
        print("Ejecutando procesos Round Robin...")
        gestor.visualizar(2)
        gestor.ejecutar_robin()
        
    if not gestor.cola_sjf.esta_vacia():
        print("Ejecutando procesos SJF...")
        gestor.visualizar(3)
        gestor.ejecutar_sjf()
        
    if not gestor.cola_priority.esta_vacia():
        print("Ejecutando procesos por prioridad...")
        gestor.visualizar(4)
        gestor.ejecutar_priority()

def main():
    gestor = GestorProcesos()
    cores = gestor.consulta_cores()  
    n = 1  
    while True:
        action = input("¿Deseas agregar un nuevo proceso o empezar la ejecución? (agregar/empezar/salir): ").strip().lower()

        if action == "agregar":
            agregar_proceso(gestor, cores, n)
            n += 1  
        elif action == "empezar":
            ejecutar_procesos_por_tipo(gestor, cores)
        elif action == "salir":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor ingresa 'agregar', 'empezar' o 'salir'.")

if __name__ == "__main__":
    main()
