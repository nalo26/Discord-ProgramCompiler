import discord
from discord.ext import commands
import os

import compiler

client = commands.Bot(command_prefix = "pc!")

SUBMIT_CHANNEL = [701830495629213738] # id of code submition channels

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
    if message.channel.id not in SUBMIT_CHANNEL: return
    if len(message.attachments) == 0: return

    file = message.attachments[0]
    filename = file.filename
    extension = '.'+filename.split('.')[-1] if len(filename.split('.')) > 1 else ''
    if extension == '': return
    try: os.mkdir(f"{message.channel.name}/{message.author.id}")
    except FileExistsError: pass
    print(f"'{filename}' by {message.author.name}#{message.author.discriminator} in {message.channel.name}")
    path = f"{message.channel.name}/{message.author.id}"
    await file.save(f"{path}/{filename}")
    print(f"file '{filename}' saved to '{path}/{filename}'")

    author = message.author.id
    
    await message.delete()
    msg = await client.get_user(author).send(f"Téléchargement du programme {filename}...")
    
    await compiler.compute(path, filename, extension, msg, author)
    

client.run("TOKEN")