import discord
import os
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True 

# Inicializar el cliente de Discord con los intents
client = discord.Client(intents=intents)

# Obtener las variables de entorno
TOKEN = os.getenv('DISCORD_TOKEN') 
DIRECTORIO_IMAGENES = os.getenv('REPORTS_PATH_IMG')  

# Variable global para almacenar el ID del usuario
USER_ID = None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    global USER_ID
    
    # Ignorar los mensajes del propio bot
    if message.author == client.user:
        return

    # Guardar el USER_ID del usuario que envía el mensaje
    if USER_ID is None:
        USER_ID = message.author.id  # Obtener el ID del usuario
        print(f'Usuario identificado: {USER_ID}')

    # Comando para enviar imágenes por mensaje directo
    if isinstance(message.channel, discord.DMChannel) and message.content.startswith('!enviar_imagen'):
        try:
            user = await client.fetch_user(USER_ID)  # Cambiar a fetch_user
            if user:
                archivos = os.listdir(DIRECTORIO_IMAGENES)
                if archivos:
                    for archivo in archivos:
                        file_path = os.path.join(DIRECTORIO_IMAGENES, archivo)
                        await user.send(file=discord.File(file_path))
                        os.remove(file_path) 
                    #await message.channel.send('Imágenes enviadas correctamente.')
                else:
                    await message.channel.send('No hay imágenes para enviar.')
            else:
                await message.channel.send('Usuario no encontrado.')
        except Exception as e:
            await message.channel.send(f'Error al enviar imágenes: {str(e)}')
    
    # Comando para interactuar en canales regulares
    elif message.content.startswith('!enviar_imagen'):
        await message.channel.send("Este comando solo funciona por mensajes directos.")

client.run(TOKEN)
