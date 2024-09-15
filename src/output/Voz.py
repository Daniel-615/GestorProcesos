import pyttsx3
class Voz():
    def __init__(self):
        self.engine=pyttsx3.init()
    def hablar(self,mensaje):
        """Este método sirve para pronunciar los mensajes adquiridos."""
        self.engine.setProperty('rate',150) #velocidad de la voz normal
        self.engine.say(" "+mensaje)
        self.engine.runAndWait()