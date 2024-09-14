import discord
import os
from dotenv import load_dotenv
load_dotenv()

class Bot():
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents)

        # Configura el evento on_ready
        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user}')
            await self.send_pdfs()  
    
    async def send_pdfs(self):
        """Envía archivos PDF almacenados en el directorio especificado a un usuario de Discord."""
        DIRECTORIO_PDFS = os.getenv('REPORTS_PATH_PDF') 
        USER_ID = int(os.getenv('USER_ID'))

        try:
            user = await self.client.fetch_user(USER_ID)  
            
            if user:
                archivos = os.listdir(DIRECTORIO_PDFS)
                if archivos:
                    for archivo in archivos:
                        if archivo.endswith('.pdf'):
                            file_path = os.path.join(DIRECTORIO_PDFS, archivo)
                            await user.send(file=discord.File(file_path))
                            os.remove(file_path)
                    print('PDFs enviados correctamente.')
                else:
                    print('No hay archivos PDF para enviar.')
            else:
                print('Usuario no encontrado.')
        except discord.NotFound:
            print('Usuario no encontrado.')
        except Exception as e:
            print(f'Error al enviar PDFs: {str(e)}')

    def start(self):
        TOKEN = os.getenv('DISCORD_TOKEN')
        self.client.run(TOKEN)
