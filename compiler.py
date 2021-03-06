from subprocess import run, PIPE
import os
from shutil import rmtree

import database

language = {'.py': 'Python', '.java': 'Java', '.class': 'Java', '.c': 'C', '.cpp': 'C++', '.cs': 'C#', '.js': 'NodeJS', '.rs': 'Rust', '.fs': 'F#'}
listLang = ["python", "java", "c", "cpp", "c#", "nodejs", "rust", "f#"]

async def compute(pathFile, filename, extension, exer_name, msg, author, username, isReal=True):

    exercice = database.read("exercices.json")[exer_name]

    if not bool(exercice['enable']) and isReal:
        await msg.edit(content=f":x: **Cet exercice n'est pas/plus disponible !**")
        return

    bashCommand = ''
    if extension == '.zip':
        rmtree(f"{pathFile}/{filename[:-4]}", ignore_errors=True)
        bashCommand = f"unzip -o {filename} -d {filename[:-4]}" # -o Overwrite / -d Destination
        run(bashCommand, check=False, stdout=PIPE, cwd=pathFile, shell=True)
        print(f"Succesfully extracted {filename}")
        filename = filename[:-4]
        file = checkFile(f"{pathFile}/{filename}", filename)
        if file is None:
            await msg.edit(content=f"[`{filename}.zip`]\n:x: **Le fichier `{filename}` à exécuter n'a pas été trouvé !**")
            print("Executing file not found")
            return
        pathFile += '/'+filename
        extension = '.'+file.split('.')[-1]
        filename += extension

    try: lang = language[extension]
    except KeyError:
        await msg.edit(content=f":x: **`{extension}` n'est pas une extension valide !**")
        return
    if exercice['language'] != "all" and lang.lower() != exercice['language']:
        await msg.edit(content=f":x: **Cet exercice est seulement disponible en `{exercice['language'].capitalize()}` !**")
        return

    if extension == '.py': bashCommand = f"python3 -S {filename}"
    if extension == '.js': bashCommand = f"node {filename}"
    if extension == '.java':
        bashCommand = "javac *.java"
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        if p.stderr != "":
            await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            print("Compilation Error")
            return
        # run(f"chmod +x {filename[:-5]}.class", check=False, cwd=pathFile, shell=True)
        bashCommand = f"java {filename[:-5]}"

    if extension == '.c':
        try: os.remove(f"{pathFile}/{filename[:-2]}_c")
        except FileNotFoundError: pass

        bashCommand = f"gcc {filename} -o {filename[:-2]}_c -I."
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        
        filename = filename[:-2]
        newFile = checkFile(pathFile, f"{filename}_c")
        if newFile is None:
            await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            print("Compilation Error")
            return
        bashCommand = f"./{filename}_c"

    if extension == ".cpp":
        try: os.remove(f"{pathFile}/{filename[:-4]}_cpp")
        except FileNotFoundError: pass

        bashCommand = f"g++ {filename} -o {filename[:-4]}_cpp -std=c++17 -O2 -I."
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        
        filename = filename[:-4]
        newFile = checkFile(pathFile, f"{filename}_cpp")
        if newFile is None:
            await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            print("Compilation Error")
            return
        bashCommand = f"./{filename}_cpp"

    if extension == ".cs":
        try: os.remove(f"{pathFile}/{filename[:-3]}.exe")
        except FileNotFoundError: pass

        bashCommand = f"mcs -optimize+ {filename}"
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        
        filename = filename[:-3]
        newFile = checkFile(pathFile, f"{filename}.exe")
        if newFile is None:
            await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            print("Compilation Error")
            return
        bashCommand = f"mono {filename}.exe"
    
    if extension == ".rs":
        try: os.remove(f"{pathFile}/{filename[:-3]}_rs")
        except FileNotFoundError: pass

        bashCommand = f"rustc -o {filename[:-3]}_rs -W warnings -O {filename}"
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        
        filename = filename[:-3]
        newFile = checkFile(pathFile, f"{filename}_rs")
        if newFile is None:
            await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            print("Compilation Error")
            return
        bashCommand = f"./{filename}_rs"

    if extension == ".fs":
        try: os.remove(f"{pathFile}/{filename[:-3]}_fs")
        except FileNotFoundError: pass

        bashCommand = f"fsharpc -o {filename[:-3]}_fs {filename}"
        p = run(bashCommand, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8", cwd=pathFile, shell=True)
        
        filename = filename[:-3]
        newFile = checkFile(pathFile, f"{filename}_fs")
        if newFile is None:
            await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}]\n:x: **Erreur de compilation !** ```{p.stderr}```")
            print("Compilation Error")
            return
        bashCommand = f"./{filename}_fs"

    dec = database.read("exercices.json")
    ex_data = dec[exer_name]
    testAmount = ex_data['test_amount']
    difficulty = ex_data['difficulty']
    ishidden = bool(ex_data['hidden'])
    timeout = ex_data['timeout']
    ex_data['executed_test'] += 1
    database.write("exercices.json", dec)

    pwd = open("PWD", 'r').read()
    
    print(f"Running {filename}..", end='')
    await msg.edit(content=f"`{exer_name}` ({exercice['difficulty']}:star:) [{language[extension]}] {'***__UNRANKED__***' if not isReal else ''}\n:clock1: Exécution du programme en cours...")
    run(f"echo {pwd} | sudo -S -u programcompiler cat empty", check=False, shell=True) # connecting

    exercice_done = 0
    for i in range(1, testAmount+1):

        inp = open(f"{exer_name}/in_{i}.txt", "r").read()
        try:
            process = run(f'echo "{inp}" | sudo -u programcompiler timeout -v {timeout} {bashCommand}', stdout=PIPE, stderr=PIPE, check=False, cwd=pathFile, shell=True, universal_newlines=True)                
            output = process.stdout
            error  = process.stderr
            if output == '': output = ' '
        except UnicodeDecodeError as e: error = str(e)
        neededOut = open(f"{exer_name}/out_{i}.txt", "r").read()
        
        if error != '': # on error
            if error.startswith("timeout:"): await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : Votre programme a mis trop de temps à répondre !**")
            else:
                if not ishidden: await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme a rencontré une erreur.**\nSortie standard attendue :```{neededOut[:-1]}```\nSortie standard du programme :```{output}```\nSortie d'erreur du programme :```{error}```")
                else: await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme a rencontré une erreur.**\n*Sortie attendue masquée pour ce défi*\nSortie standard du programme :```{output}```\nSortie d'erreur du programme :```{error}```")
            print('. Failed!')
            if isReal: await msg.edit(content=f"{msg.content}\n{database.add_submition(author, username, exer_name, language[extension].lower(), exercice_done, False, exercice_done*difficulty)}")
            return

        if output != neededOut: # not good output
            if not ishidden: await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme s'est exécuté correctement, mais :**\nSortie standard attendue :```{neededOut[:-1]}```\nSortie standard du programme :```{output}```")
            else: await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :x: **Test échoué : votre programme s'est exécuté correctement, mais :**\n*Sortie attendue masquée pour ce défi*\nSortie standard du programme :```{output}```")
            print('. Failed!')
            if isReal: await msg.edit(content=f"{msg.content}\n{database.add_submition(author, username, exer_name, language[extension].lower(), exercice_done, False, exercice_done*difficulty)}")
            return
            
        await msg.edit(content=f"{msg.content}\n`{i}/{testAmount}` :white_check_mark: **Test passé !**")
        exercice_done += 1
    
    await msg.edit(content=f"{msg.content}\n\n:trophy: Bravo, tu as réussi cet exercice !")
    print('. Done!')

    if isReal: await msg.edit(content=f"{msg.content}\n{database.add_submition(author, username, exer_name, language[extension].lower(), exercice_done, True, exercice_done*difficulty)}")
    

def checkFile(pathFile, name):
    for file in os.listdir(pathFile):
        splited = file.split('.')
        if '.'.join(splited[:-1]) == name and splited[-1] != 'class': return file
        if file == name: return file
    return None