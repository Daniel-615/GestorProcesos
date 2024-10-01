import logging

class Log():
    def __init__(self):
        self.logger = logging.getLogger(__name__) 

        if not self.logger.handlers:  
            self.logger.setLevel(logging.INFO) 

          
            file_handler = logging.FileHandler("gestor_procesos.log")
            file_handler.setLevel(logging.INFO) 

           
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

           
            self.logger.addHandler(file_handler)


    def log_info(self, message):
        """Método para loggear mensajes de información"""
        self.logger.info(message)
    
    def log_error(self, message):
        """Método para loggear mensajes de error"""
        self.logger.error(message)
    def log_warning(self,message):
        """Método para loggear mensajes de precaución"""
        self.logger.warning(message)
