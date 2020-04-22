import discord
from discord.ext import commands
import os

from compiler import compute

client = commands.Bot(command_prefix = "pc!")

@client.event
async def on_ready():
    print("Connected as")
    print(f"{client.user.name}#{client.user.discriminator}")
    print(client.user.id)
    print('--------------------')
    await client.change_presence(activity=discord.Game(name="Compiling some file"))

@client.event
async def on_message(message):
    if message.author.id == client.user.id: return
    if not isinstance(message.channel, discord.DMChannel): return # only private message
    if len(message.attachments) == 0: return

    file = message.attachments[0]
    filename = file.filename
    extension = '.'+filename.split('.')[-1] if len(filename.split('.')) > 1 else ''
    if extension == '': return

    author = message.author.id
    exercice = ".".join(filename.split('.')[:-1])

    if exercice in ['.git', '__pycache__', 'users'] or not os.path.isdir(exercice):
        await client.get_user(author).send(f":x: **Aucun exercice du nom de `{exercice}` n'existe !**")
        return

    try: os.mkdir(f"{exercice}/{author}")
    except FileExistsError: pass
    print("=====================================================================")
    print(f"'{filename}' by {message.author.name}#{message.author.discriminator}")
    path = f"{exercice}/{author}"
    await file.save(f"{path}/{filename}")
    print(f"File '{filename}' saved to '{path}/{filename}'")

    msg = await client.get_user(author).send(f"Téléchargement du programme {filename}...")
    
    await compute(path, filename, extension, exercice, msg, author)
    

client.run("NzAxNDEwMjk1MzE0MzgyODc4.Xp6gMg.pugzaUO-z1fCQDKm3CIMQkGg71M")