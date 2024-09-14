import json
class Json(): 
    def __init__(self):
        self.mostrar_colas=False
        self.mostrar_colas_dc=False
    def getDc(self):
        return self.mostrar_colas_dc
    def getColas(self):
        return self.mostrar_colas
    def setDc(self,valor):
        self.mostrar_colas_dc=valor
    def setColas(self,valor):
        self.mostrar_colas=valor
    def cargar_configuracion(self):
        nombre_archivo = 'config.json'
        
        try:
            with open(nombre_archivo, 'r') as archivo:
                datos = json.load(archivo)
                self.mostrar_colas = datos.get('mostrar_colas', False)
                self.mostrar_colas_dc = datos.get('mandar_colas_dc', False)
        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no se encontró.")
        except json.JSONDecodeError:
            print(f"Error al decodificar el archivo JSON.")
        except Exception as e:
            print(f"Error al cargar la configuración: {e}")

    def crear_json_configuracion(self):
        datos = {
            "mostrar_colas": True,
            "mandar_colas_dc": True
        }

        nombre_archivo = 'config.json'

        try:
            with open(nombre_archivo, 'w') as archivo:
                json.dump(datos, archivo, indent=4)  
            print(f"Archivo {nombre_archivo} creado con éxito.")
        except Exception as e:
            print(f"Error al crear el archivo JSON: {e}")