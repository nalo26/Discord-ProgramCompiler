import discord
from discord.ext import commands
from subprocess import run, PIPE
import shlex

async def compute(file, extension, msg):
    bashCommand = ''
    if extension == '.py': bashCommand = f"python3 -S {file}"
    if extension == '.java': bashCommand = f"java {file}"
    if extension == '.c': bashCommand = f"gcc {file} -o {file[:-2]} -std=c11 -O2 -lm"

    if bashCommand == '': return

    testAmount = int(open(f"{msg.channel.name}/data.txt", "r").read())
    await msg.edit("Exécution du programme en cours...")
    for i in range(1, testAmount+1):
        inp = open(f"{msg.channel.name}/in_{i}.txt", "r").read()

        if extension == '.c': # compiled THEN execute
            run(shlex.split(f"{bashCommand}"), check=False)
            process = run(shlex.split(f"./{file[:-2]}"), input=inp, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8")
        else:
            process = run(shlex.split(f"{bashCommand}"), input=inp, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8")
        output = process.stdout
        error  = process.stderr
        if output == '': output = ' '

        neededOut = open(f"{msg.channel.name}/out_{i}.txt", "r").read()
        
        if error != '': # on error
            await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme a rencontré une erreur.**\nSortie standard attendue :```{neededOut[:-1]}```\nSortie standard du programme :```{output}```\nSortie d'erreur du programme :```{error}```")
            break

        if output != neededOut: # not good output
            await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme s'est exécuté correctement, mais :**\nSortie standard attendue :```{neededOut[:-1]}```\nSortie standard du programme :```{output}```")
            break    
            
        await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :white_check_mark: **Test passé !**")
    