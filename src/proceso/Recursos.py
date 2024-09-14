import psutil

class Recursos:
    def __init__(self):
        pass

    def obtener_uso_cpu(self):
        uso_cpu = psutil.cpu_percent(interval=1)
        #print(f"Uso de CPU: {uso_cpu}%")
        return uso_cpu

    def obtener_info_cpu(self):
        num_nucleos_logicos = psutil.cpu_count(logical=True)
        num_nucleos_fisicos = psutil.cpu_count(logical=False)
        #print(f"Núcleos lógicos: {num_nucleos_logicos}, Núcleos físicos: {num_nucleos_fisicos}")
        return num_nucleos_logicos, num_nucleos_fisicos

    def obtener_info_memoria(self):
        memoria = psutil.virtual_memory()
        total_memoria = memoria.total / (1024 ** 3)
        memoria_disponible = memoria.available / (1024 ** 3)
        memoria_en_uso = memoria.used / (1024 ** 3)
        uso_memoria = memoria.percent
        #print(f"Memoria Total: {total_memoria:.2f} GB")
        #print(f"Memoria Disponible: {memoria_disponible:.2f} GB")
        #print(f"Memoria en Uso: {memoria_en_uso:.2f} GB ({uso_memoria}%)")
        return memoria_disponible

    def obtener_info_disco(self):
        disco = psutil.disk_usage('/')
        total_disco = disco.total / (1024 ** 3)
        espacio_usado = disco.used / (1024 ** 3)
        espacio_libre = disco.free / (1024 ** 3)
        uso_disco = disco.percent
        print(f"Espacio en Disco Total: {total_disco:.2f} GB")
        print(f"Espacio Usado: {espacio_usado:.2f} GB ({uso_disco}%)")
        print(f"Espacio Libre: {espacio_libre:.2f} GB")
        return total_disco, espacio_usado, espacio_libre, uso_disco

    def obtener_info_procesos(self):
        num_procesos = len(psutil.pids())
        print(f"Número de procesos activos: {num_procesos}")
        procesos = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            print(proc.info)
            procesos.append(proc.info)
        return num_procesos, procesos

    def obtener_info_red(self):
        estadisticas_red = psutil.net_io_counters()
        bytes_enviados = estadisticas_red.bytes_sent / (1024 ** 2)
        bytes_recibidos = estadisticas_red.bytes_recv / (1024 ** 2)
        print(f"Bytes enviados: {bytes_enviados:.2f} MB")
        print(f"Bytes recibidos: {bytes_recibidos:.2f} MB")
        return bytes_enviados, bytes_recibidos

