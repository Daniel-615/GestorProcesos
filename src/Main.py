from proceso.Proceso import Proceso
from GestorProceso import GestorProcesos
from proceso.Json import Json
from bot.Bot import Bot  
from output.Reportes import Reportes
def iniciarBot():
    bot=Bot()
    bot.start()
def infLog(gestor,message):
    log=gestor.getLog()
    log.log_info(message)
def errLog(gestor,message):
    log=gestor.getLog()
    log.log_error(message)
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
    
    try:
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
    except Exception as e:
        message=f"Error al agregar el proceso: {e}"
        errLog(gestor,message)

    # Agregar el proceso a la cola correspondiente
    gestor.agregar_proceso(proceso)
    message=f"Proceso {n} agregado correctamente a la cola de {planificacion.upper()}."
    infLog(gestor,message)

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
        try:
            message="Ejecutando procesos FIFO..."
            infLog(gestor,message)
            gestor.visualizar(1)
            gestor.ejecutar_fifo(cores)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(e)
            
        

    if not gestor.cola_rr.esta_vacia():
        try:
            message="Ejecutando procesos Round Robin..."
            infLog(gestor,message)
            gestor.visualizar(2)
            gestor.ejecutar_robin()
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(e)
        
    if not gestor.cola_sjf.esta_vacia():
        try:
            message="Ejecutando procesos SJF..."
            infLog(gestor,message)
            gestor.visualizar(3)
            gestor.ejecutar_sjf()
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(e)
        
    if not gestor.cola_priority.esta_vacia():
        try:
            message="Ejecutando procesos por prioridad..."
            infLog(gestor,message)
            gestor.visualizar(4)
            gestor.ejecutar_priority()
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(e)
    if gestor.cola_priority.esta_vacia() and gestor.cola_sjf.esta_vacia() and gestor.cola_fifo.esta_vacia() and gestor.cola_rr.esta_vacia():
        try:
            reportes=Reportes()
            nombre_pdf_imagenes = "graficos"
            reportes.convertir_imagenes_a_pdf(nombre_pdf_imagenes,gestor)
            
            message=f"{nombre_pdf_imagenes} convertidos a pdf."
            infLog(gestor,message)
        except Exception as e:
            print(f"Error {e}")
            raise ValueError(e)
    
def main():
    gestor = GestorProcesos()
    json_config=Json()
    cores = gestor.consulta_cores()  
    n = 1  
    answer_colas=input("Deseas Mostrar las Colas por cada Evento (SI/NO)?").strip().lower()
    answer_dc=input("Deseas que se te envíe los reportes por medio de Discord? (SI/NO):").strip().lower()
    if answer_colas=="SI":
        json_config.setColas(True)
    if answer_dc=="SI":
        json_config.setDc(True)
    json_config.crear_json_configuracion()
    while True:
        action = input("¿Deseas agregar un nuevo proceso o empezar la ejecución? (agregar/empezar/salir/bot): ").strip().lower()

        if action == "agregar":
            agregar_proceso(gestor, cores, n)
            n += 1  
        elif action == "empezar":
            ejecutar_procesos_por_tipo(gestor, cores)
        elif action == "bot":
            json_config.cargar_configuracion()
            enviar_reportes=json_config.getDc()
            if enviar_reportes:
                print("Mandando reportes por medio del bot..")
                try:
                    iniciarBot()
                except Exception as e:
                    print(f"Error al iniciar el bot: {e}")
            else:
                print("La configuración indica que no se deben enviar reportes por Discord.")
        elif action == "salir":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor ingresa 'agregar', 'empezar' o 'salir'.")
if __name__ == "__main__":
    main()