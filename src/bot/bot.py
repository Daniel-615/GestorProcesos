import discord
import os
from dotenv import load_dotenv
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') 
DIRECTORIO_IMAGENES = os.getenv('REPORTS_PATH_IMG')  
USER_ID = int(os.getenv('USER_ID')) 

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.startswith('!enviar_imagen'):
        user = client.get_user(USER_ID)
        if user:
            archivos = os.listdir(DIRECTORIO_IMAGENES)
            if archivos:
                for archivo in archivos:
                    file_path = os.path.join(DIRECTORIO_IMAGENES, archivo)
                    await user.send(file=discord.File(file_path))
                    os.remove(file_path) 
            else:
                await message.channel.send('No hay imágenes para enviar.')
        else:
            await message.channel.send('Usuario no encontrado.')

client.run(TOKEN)
