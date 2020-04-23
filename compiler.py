from subprocess import run, PIPE
import os

import database

language = {'.py': 'Python', '.java': 'Java', '.class': 'Java', '.c': 'C'}
listLang = ["python", "java", "c"]

async def compute(pathFile, filename, extension, exer_name, msg, author, username):

    exercice = database.read("exercices.json")[exer_name]

    try: lang = language[extension]
    except KeyError:
        await msg.edit(content=f":x: **`{extension}` n'est pas une extension valide !**")
        return
    if exercice['language'] != "all" and lang.lower() != exercice['language']:
        await msg.edit(content=f":x: **Cet exercice est seulement disponible en `{exercice['language'].capitalize()}` !**")
        return

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
            await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            return
        bashCommand = f"java {filename[:-5]}"

    if extension == '.c':
        try: os.remove(f"{pathFile}/{filename[:-2]}_c")
        except FileNotFoundError: pass

        bashCommand = f"gcc {filename} -o {filename[:-2]}_c -std=c11 -O2 -lm"
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        
        newFile = checkFile(pathFile, filename[:-2])
        if newFile is None:
            await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            return
        filename = filename[:-2]
        bashCommand = f"./{filename}_c"

    dec = database.read("exercices.json")
    ex_data = dec[exer_name]
    testAmount = ex_data['test_amount']
    difficulty = ex_data['difficulty']
    ishidden = bool(ex_data['hidden'])
    ex_data['executed_test'] += 1
    database.write("exercices.json", dec)
    
    print(f"Running {filename}..", end='')
    await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}]\n:clock1: Exécution du programme en cours...")

    exercice_done = 0
    for i in range(1, testAmount+1):

        inp = open(f"{exer_name}/in_{i}.txt", "r").read()
        process = run(bashCommand, input=inp, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        output = process.stdout
        error  = process.stderr
        if output == '': output = ' '
        # if error  == '': error  = ' '

        neededOut = open(f"{exer_name}/out_{i}.txt", "r").read()
        
        if error != '': # on error
            if not ishidden: await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme a rencontré une erreur.**\nSortie standard attendue :```{neededOut[:-1]}```\nSortie standard du programme :```{output}```\nSortie d'erreur du programme :```{error}```")
            else: await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme a rencontré une erreur.**\n*Sortie attendue masquée pour ce défi*\nSortie standard du programme :```{output}```\nSortie d'erreur du programme :```{error}```")
            print('. Failed!')
            is_top, submition = database.add_submition(author, username, exer_name, language[extension], exercice_done, False, 0)
            if not is_top and submition['complete']: await msg.edit(content=f"{msg.content}\nTu as déjà réussi cet exercice le `{submition['date'].split(' ')[0]}` en `{submition['language']}` !")
            return

        if output != neededOut: # not good output
            if not ishidden: await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme s'est exécuté correctement, mais :**\nSortie standard attendue :```{neededOut[:-1]}```\nSortie standard du programme :```{output}```")
            else: await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme s'est exécuté correctement, mais :**\n*Sortie attendue masquée pour ce défi*\nSortie standard du programme :```{output}```")
            print('. Failed!')
            is_top, submition = database.add_submition(author, username, exer_name, language[extension], exercice_done, False, 0)
            if not is_top and submition['complete']: await msg.edit(content=f"{msg.content}\nTu as déjà réussi cet exercice le `{submition['date'].split(' ')[0]}` en `{submition['language']}` !")
            return
            
        await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :white_check_mark: **Test passé !**")
        exercice_done += 1
    
    await msg.edit(content=f"{msg.content}\n\n:trophy: Bravo, tu as réussi cet exercice !")
    print('. Done!')

    is_top, submition = database.add_submition(author, username, exer_name, language[extension], exercice_done, True, exercice_done*difficulty)
    if is_top: await msg.edit(content=f"{msg.content}\nC'est ton meilleur score, tu gagnes {exercice_done*difficulty} point(s) !")
    else: await msg.edit(content=f"{msg.content}\nTu as déjà réussi cet exercice le `{submition['date'].split(' ')[0]}` en `{submition['language']}` !")
    

def checkFile(pathFile, name):
    for file in os.listdir(pathFile):
        splited = file.split('.')
        if '.'.join(splited[:-1]) == name and splited[-1] != 'class': return file
    return None