from subprocess import run, PIPE
import os
import json

import database

language = {'.py': 'Python', '.java': 'Java', '.class': 'Java', '.c': 'C'}

async def compute(pathFile, filename, extension, exercice, msg, author):

    bashCommand = ''
    if extension == '.zip':
        bashCommand = f"unzip -o {filename} -d {filename[:-4]}" # -o Overwrite / -d Destination
        run(bashCommand, check=False, stdout=PIPE, cwd=pathFile, shell=True)
        print(f"Succesfully extracted {filename}")
        filename = filename[:-4]
        file = checkFile(f"{pathFile}/{filename}", filename)
        if file is None:
            await msg.edit(content=f"[`{filename}.zip`]\n:x: **Le fichier `{filename}` à exécuter n'a pas été trouvé !**")
            return
        pathFile += '/'+filename
        extension = '.'+file.split('.')[-1]
        filename += extension

    if extension == '.py': bashCommand = f"python3 -S {filename}"
    if extension == '.java':
        bashCommand = "javac *.java"
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        if p.stderr != "":
            await msg.edit(content=f"`{filename}` [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            return
        bashCommand = f"java {filename[:-5]}"

    if extension == '.c':
        try: os.remove(f"{pathFile}/{filename[:-2]}_c")
        except FileNotFoundError: pass

        bashCommand = f"gcc {filename} -o {filename[:-2]}_c -std=c11 -O2 -lm"
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        
        newFile = checkFile(pathFile, filename[:-2])
        if newFile is None:
            await msg.edit(content=f"`{filename}` [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            return
        filename = filename[:-2]
        bashCommand = f"./{filename}_c"

    if bashCommand == '': return

    with open(f"{exercice}/data.json", "r") as mf:
        dec = json.load(mf)
    mf.close()
    testAmount = dec['test_amount']
    difficulty = dec['difficulty']
    
    print(f"Running {filename}..", end='')
    await msg.edit(content=f"`{filename}` [{language[extension]}]\n:clock1: Exécution du programme en cours...")

    exercice_done = 0
    for i in range(1, testAmount+1):

        inp = open(f"{exercice}/in_{i}.txt", "r").read()
        process = run(bashCommand, input=inp, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        output = process.stdout
        error  = process.stderr
        if output == '': output = ' '

        neededOut = open(f"{exercice}/out_{i}.txt", "r").read()
        
        if error != '': # on error
            await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme a rencontré une erreur.**\nSortie standard attendue :```{neededOut[:-1]}```\nSortie standard du programme :```{output}```\nSortie d'erreur du programme :```{error}```")
            print('. Failed!')
            return

        if output != neededOut: # not good output
            await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme s'est exécuté correctement, mais :**\nSortie standard attendue :```{neededOut[:-1]}```\nSortie standard du programme :```{output}```")
            print('. Failed!')
            return
            
        await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :white_check_mark: **Test passé !**")
        exercice_done += 1
    
    await msg.edit(content=f"{msg.content}\n\n:trophy: Bravo, tu as réussi cet exercice !")
    print('. Done!')

    is_top, submition = database.add_submition(author, exercice, language[extension], exercice_done, exercice_done==testAmount, exercice_done*difficulty)
    if is_top: await msg.edit(content=f"{msg.content}\nC'est ton meilleur score, tu gagnes {exercice_done*difficulty} point(s) !")
    else: await msg.edit(content=f"{msg.content}\nTu as déjà réussi cet exercice le `{submition['date'].split(' ')[0]}` en `{submition['language']}` !")
    

def checkFile(pathFile, name):
    for file in os.listdir(pathFile):
        splited = file.split('.')
        if '.'.join(splited[:-1]) == name and splited[-1] != 'class': return file
    return None