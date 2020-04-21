from subprocess import run, PIPE
import os

language = {'.py': 'Python', '.java': 'Java', '.c': 'C'}

async def compute(pathFile, filename, extension, msg, author):

    if not os.path.isdir(filename.split('.')[:-1]):
        await msg.edit(content=f":x: **Aucun exercice du nom de `{filename.split('.')[:-1]}` n'existe !**")
        return

    bashCommand = ''
    if extension == '.zip':
        bashCommand = f"unzip -o {filename} -d {filename[:-4]}" # -o Overwrite / -d Destination
        run(bashCommand, check=False, stdout=PIPE, cwd=pathFile, shell=True)
        print(f"Succesfully extracted {filename}")
        filename = filename[:-4]
        file = checkFile(f"{pathFile}/{filename}", "Main")
        if file is None:
            await msg.edit(content=f"[`{filename}.zip`]\n:x: **Le fichier `Main` n'a pas été trouvé !**")
            return
        pathFile += '/'+filename
        extension = '.'+file.split('.')[-1]
        filename = 'Main' + extension        

    if extension == '.py': bashCommand = f"python3 -S {filename}"
    if extension == '.java':
        bashCommand = "javac *.java"
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        if p.stderr != "":
            await msg.edit(content=f"`{filename}` [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            return
        bashCommand = "java Main"

    if extension == '.c':
        try: os.remove(f"{pathFile}/{filename[:-2]}")
        except FileNotFoundError: pass

        bashCommand = f"gcc {filename} -o {filename[:-2]} -std=c11 -O2 -lm"
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        
        newFile = checkFile(pathFile, filename[:-2])
        if newFile is None:
            await msg.edit(content=f"`{filename}` [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            return
        filename = filename[:-2]
        bashCommand = f"./{filename}"

    if bashCommand == '': return

    testAmount = int(open(f"{msg.channel.name}/data.txt", "r").read())
    await msg.edit(content=f"`{filename}` [{language[extension]}]\n:clock1: Exécution du programme en cours...")

    for i in range(1, testAmount+1):

        inp = open(f"{msg.channel.name}/in_{i}.txt", "r").read()
        process = run(bashCommand, input=inp, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
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
    

def checkFile(pathFile, name):
    for file in os.listdir(pathFile):
        if file.split('.')[0] == name: return file
    return None