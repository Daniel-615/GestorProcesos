import psutil

class Recursos:
    def __init__(self):
        pass

    def obtener_uso_cpu(self):
        uso_cpu = psutil.cpu_percent(interval=1)
        return uso_cpu

    def obtener_info_cpu(self):
        num_nucleos_logicos = psutil.cpu_count(logical=True)
        num_nucleos_fisicos = psutil.cpu_count(logical=False)
        return num_nucleos_logicos, num_nucleos_fisicos

    def obtener_info_memoria(self):
        memoria = psutil.virtual_memory()
        total_memoria = memoria.total / (1024 ** 3)
        memoria_disponible = memoria.available / (1024 ** 3)
        memoria_en_uso = memoria.used / (1024 ** 3)
        uso_memoria = memoria.percent
        return memoria_disponible
