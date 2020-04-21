import discord
from discord.ext import commands

import compiler

client = commands.Bot(command_prefix = "pc!")

# SUBMIT_CHANNEL = 701417692711878678
SUBMIT_CHANNEL = 701830495629213738

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
    if message.channel.id != SUBMIT_CHANNEL: return
    if len(message.attachments) == 0: return

    file = message.attachments[0]
    filename = file.filename
    extension = '.'+filename.split('.')[-1] if len(filename.split('.')) > 1 else ''
    if extension == '': return

    print(f"'{filename}' by {message.author.name}#{message.author.discriminator} in {message.channel.name}")
    newFile = f"{message.channel.name}_{message.author.id}{extension}"
    await file.save(newFile)
    print(f"file {filename} saved to {newFile}")

    msg = await message.channel.send("Téléchargement du programme...")

    compiler.compute(newFile, extension, msg)
    


client.run("NzAxNDEwMjk1MzE0MzgyODc4.Xp1VgQ.F1NtuWKWubKVrBL2eqjpujF9qww")