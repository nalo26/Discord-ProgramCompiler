import discord
from discord.ext import commands
import os

from compiler import compute
import database
from datetime import datetime
from shutil import rmtree

client = commands.Bot(command_prefix = "!")

ADMIN = [250989853158801419, 520334699046895617]
listLang = ["python", "java", "c", "nodejs"]

@client.event
async def on_ready():
    print("Connected as")
    print(f"{client.user.name}#{client.user.discriminator}")
    print(client.user.id)
    print('--------------------')
    await client.change_presence(activity=discord.Game(name="Compiling some file"))

# ================== #
# | ADMIN COMMANDS | #
# ================== #
@client.command(aliases=['createTest', 'createExercise'])
async def create(ctx, *argv):
    if not is_admin(ctx.message.author.id): return
    if not is_dm(ctx.channel): return
    title = ""
    description = ""
    inputs = ""
    output = ""
    difficulty = 1
    hidden = False
    language = "all"
    timeout = 10
    enable = True
    for i, arg in enumerate(argv):
        if len(argv)-1 >= i+1 and '-' not in argv[i+1]:
            if arg in ['-t', '--title']: title = argv[i+1]
            if arg in ['-D', '--description']: description = argv[i+1]
            if arg in ['-i', '--input']: inputs = argv[i+1]
            if arg in ['-o', '--output']: output = argv[i+1]
            if arg in ['-d', '--difficulty']: difficulty = int(argv[i+1])
            if arg in ['-h', '--hidden']: hidden = bool(argv[i+1].lower() == 'true')
            if arg in ['-l', '--language']: language = argv[i+1]
            if arg in ['-T', '--timeout']: timeout = int(argv[i+1])
            if arg in ['-e', '--enable']: enable = bool(argv[i+1].lower() == 'true')

    if language != "all" and language.lower() not in listLang:
        await ctx.send(f":x: **Le langage `{language}` n'est pas (encore) supporté !**")
        return
    try:
        database.read("exercices.json")[title]
        await ctx.send(f":x: **Un défi du nom de `{title}` existe déjà ! **")
    except KeyError:
        await ctx.send(embed=create_ex(title, difficulty, description, inputs, output, hidden, language.lower(), timeout, enable))
        print(f"Exercise '{title}' ({difficulty}) [{language}] created by {ctx.message.author.name}")

@client.command()
async def edit(ctx, *argv):
    if not is_admin(ctx.message.author.id): return
    if not is_dm(ctx.channel): return
    title = ""
    description = ""
    inputs = ""
    output = ""
    difficulty = -1
    hidden = None
    language = "all"
    timeout = -1
    enable = None
    for i, arg in enumerate(argv):
        if len(argv)-1 >= i+1 and '-' not in argv[i+1]:
            if arg in ['-t', '--title']: title = argv[i+1]
            if arg in ['-D', '--description']: description = argv[i+1]
            if arg in ['-i', '--input']: inputs = argv[i+1]
            if arg in ['-o', '--output']: output = argv[i+1]
            if arg in ['-d', '--difficulty']: difficulty = int(argv[i+1])
            if arg in ['-h', '--hidden']: hidden = bool(argv[i+1].lower() == 'true')
            if arg in ['-l', '--language']: language = argv[i+1]
            if arg in ['-T', '--timeout']: timeout = int(argv[i+1])
            if arg in ['-e', '--enable']: enable = bool(argv[i+1].lower() == 'true')

    if language != "all" and language.lower() not in listLang:
        await ctx.send(f":x: **Le langage `{language}` n'est pas (encore) supporté !**")
        return
    try:
        database.read("exercices.json")[title]
        await ctx.send(embed=edit_ex(title, difficulty, description, inputs, output, hidden, language.lower(), timeout, enable))
        print(f"Exercise '{title}' ({difficulty}) [{language}] edited by {ctx.message.author.name}")
    except KeyError: await ctx.send(f":x: **Aucun exercice du nom de `{title}` n'a été trouvé !**")

@client.command(aliases=['del', 'delete'])
async def remove(ctx, title):
    dec = database.read("exercices.json")
    try: dec[title]
    except KeyError:
        await ctx.send(f":x: **Aucun exercice du nom de `{title}` n'a été trouvé !**")
        return
    delete_ex(title)
    await ctx.send(f":white_check_mark: **Défi `{title}` supprimé avec succès !**")
    print(f"Exercise '{title}' deleted by {ctx.message.author.name}")

@client.command(aliases=['addTest'])
async def add(ctx, *argv):
    if not is_admin(ctx.message.author.id): return
    if not is_dm(ctx.channel): return
    title = ""
    inputs = ""
    outputs = ""
    for i, arg in enumerate(argv):
        if len(argv)-1 >= i+1:
            if arg in ['-t', '--title']: title = argv[i+1]
            if arg in ['-i', '--input', '--inputs']: inputs = argv[i+1]
            if arg in ['-o', '--output', '--outputs']: outputs = argv[i+1]

    dec = database.read("exercices.json")
    if title != "" and inputs != "" and outputs != "":
        try: dec[title]
        except KeyError:
            await ctx.send(f":x: **Aucun exercice du nom de `{title}` n'a été trouvé !**")
            return
        add_test(title, inputs.replace('/n', '\n').replace("\\n", "\n"), outputs.replace('/n', '\n').replace("\\n", "\n"))
        await ctx.send(f":white_check_mark: **Test pour le défi `{title}` créé avec succès !**")
        print(f"Test added for '{title}' by {ctx.message.author.name}")
    else:
        if title == "":
            await ctx.send(":x: **Veuillez préciser le __titre__ du défi !** (`-t`)")
            return
        if inputs == "" and outputs == "":
            await ctx.send(":x: **Veuillez préciser un __input__ et un __output__ à ce test !** (`-i` et `-o`)")
            return
        if inputs == "": await ctx.send(":x: **Veuillez préciser un __input__ à ce test !** (`-i`)")
        if outputs == "": await ctx.send(":x: **Veuillez préciser un __output__ à ce test !** (`-o`)")
    


# ================= #
# | USER COMMANDS | #
# ================= #
@client.command(aliases=["list", "listes"])
async def liste(ctx, lang="all"):
    if lang != "all" and lang.lower() not in listLang:
        await ctx.send(f":x: **Le langage `{lang}` n'est pas (encore) supporté !**")
        return
    await ctx.send(embed=show_all_ex(lang.lower()))

@client.command(aliases=["exercice", "exercise", "details"])
async def detail(ctx, title=""):
    dec = database.read("exercices.json")
    try: ex = dec[title]
    except KeyError:
        await ctx.send(f":x: **Aucun exercice du nom de `{title}` n'a été trouvé !**")
        return
    await ctx.send(embed=show_ex(title, ex))

@client.command(aliases=['profil', 'me'])
async def profile(ctx):
    dec = database.read("users.json")
    u_disc = ctx.message.author
    try: user = dec[str(u_disc.id)]
    except KeyError:
        try: username = client.get_guild(688355824934060032).get_member(u_disc.id).nick
        except Exception: username = client.get_user(u_disc.id).display_name
        user = database.create_user(dec, username, u_disc.id)
    await ctx.send(embed=show_user(u_disc, user))

@client.command(aliases=['classement', 'top'])
async def leaderboard(ctx, lang="all"):
    if lang != "all" and lang.lower() not in listLang:
        await ctx.send(f":x: **Le langage `{lang}` n'est pas (encore) supporté !**")
        return
    dec = database.read("users.json")
    res = {}
    for u in dec.values():
        if lang.lower() == "all": res[u['name']] = u['score']['general']
        else:
            try: res[u['name']] = u['score'][lang.lower()]
            except KeyError: pass
    res = sorted(res.items(), key = lambda kv:(kv[1], kv[0]))
    res.reverse()
    
    if lang.lower() == "all": embed = discord.Embed(title=":trophy: Classement général")
    else: embed = discord.Embed(title=f":trophy: Classement général {lang.capitalize()}")
    desc = ""
    for i, (name, score) in enumerate(res):
        desc += f"{i+1} : {name} ({score}pts)\n"
    if desc == "": desc = "*Aucune participation n'a été trouvée !*"
    embed.description = desc

    await ctx.send(embed=embed)


@client.event
async def on_message(message):

    await client.process_commands(message)

    if message.author.id == client.user.id: return
    if not is_dm(message.channel): return # only private message
    if len(message.attachments) == 0: return

    file = message.attachments[0]
    filename = file.filename
    extension = '.'+filename.split('.')[-1] if len(filename.split('.')) > 1 else ''
    if extension == '': return

    author = message.author.id
    exercice = ".".join(filename.split('.')[:-1])

    dec = database.read("exercices.json")
    try: dec[exercice]
    except KeyError:
        await client.get_user(author).send(f":x: **Aucun exercice du nom de `{exercice}` n'a été trouvé !**")
        return

    print("=====================================================================")
    try: os.mkdir(f"{exercice}/{author}")
    except FileExistsError: pass
    try: username = client.get_guild(688355824934060032).get_member(author).nick
    except Exception: username = client.get_user(author).display_name

    print(f"'{filename}' by {username}")
    path = f"{exercice}/{author}"
    await file.save(f"{path}/{filename}")
    print(f"File '{filename}' saved to '{path}/{filename}'")

    msg = await client.get_user(author).send(f"Téléchargement du programme {filename}...")
    
    await compute(path, filename, extension, exercice, msg, author, username)

def is_admin(u_id):
    return u_id in ADMIN
def is_dm(channel):
    return isinstance(channel, discord.DMChannel)

def create_ex(title, difficulty, desc, inputs, output, hidden, language, timeout, enable):
    os.mkdir(title)
    dec = database.read("exercices.json")
    data = {'difficulty': difficulty, 'date': database.get_time(), 'description': desc, 'inputs': inputs, 'output': output, 'hidden': hidden, 'language': language, 'timeout': timeout, 'enable': enable, 'test_amount': 0, 'executed_test': 0}
    dec[title] = data
    database.write("exercices.json", dec)
    return show_ex(title, data)

def edit_ex(title, difficulty, desc, inputs, output, hidden, language, timeout, enable):
    dec = database.read("exercices.json")
    ex = dec[title]
    if difficulty != -1: ex['difficulty'] = difficulty
    if desc != "": ex['description'] = desc
    if inputs != "": ex['inputs'] = inputs
    if output != "": ex['output'] = output
    if hidden is not None: ex['hidden'] = hidden
    if language is not None: ex['language'] = language
    if timeout != -1: ex['timeout'] = timeout
    if enable is not None: ex['enable'] = enable
    database.write("exercices.json", dec)
    return show_ex(title, ex)

def delete_ex(title):
    rmtree(title, ignore_errors=True)
    dec = database.read("exercices.json")
    del dec[title]
    database.write("exercices.json", dec)
    dec = database.read("users.json")
    for user in dec.values():
        try:
            user['score']['general'] -= user['submit'][title]['best_score']
            for sub, data in user['submit'][title].items():
                if sub not in ["best_score", "complete"]: user['score'][sub] -= data['score']
            del user['submit'][title]
        except KeyError: pass
    database.write("users.json", dec)
    
def show_ex(title, data):
    embed = discord.Embed(title=f"{title} ({data['difficulty']}:star:)")
    embed.description = data['description'] if data['description'] != "" else "*Non défini*"
    embed.add_field(name="Langage :", value=data['language'].capitalize() if data['language'] != "all" else "*Tous*")
    embed.add_field(name="Disponibilité :", value=":white_check_mark: Ouvert" if bool(data['enable']) else ":x: Fermé")
    embed.add_field(name="Entrée :", value=data['inputs'] if data['inputs'] != "" else "*Non défini*", inline=False)
    embed.add_field(name="Sortie :", value=data['output'] if data['output'] != "" else "*Non défini*", inline=False)

    embed.set_footer(text='Créé le')
    embed.timestamp = datetime.strptime(data['date'], '%x %X')
    return embed

def show_all_ex(lang):
    dec = database.read("exercices.json")
    if lang == "all":
        embed = discord.Embed(title=f"Liste de tous les défis ({len(dec)})")
        desc = ""
        for title, ex in dec.items():
            desc += "\n~~" if not bool(ex['enable']) else "\n"
            if ex['language'] == "all": desc += f"▸ {title} ({ex['difficulty']}:star:)"
            else: desc += f"▸ {title} [**{ex['language'].capitalize()}**] ({ex['difficulty']}:star:)"
            if not bool(ex['enable']): desc += "~~"
    else:
        good_lang = {}
        for title, ex in dec.items():
            if ex['language'] == lang: good_lang[title] = ex
        embed = discord.Embed(title=f"Liste des défis {lang.capitalize()} ({len(good_lang)})")
        desc = ""
        for title, ex in good_lang.items():
            desc += "\n~~" if not bool(ex['enable']) else "\n"
            desc += f"▸ {title} [**{ex['language'].capitalize()}**] ({ex['difficulty']}:star:)"
            if not bool(ex['enable']): desc += "~~"
    embed.description = desc if desc != "" else "*Aucun défi n'a été trouvé !*"
    return embed

def add_test(title, inp, out):
    dec = database.read("exercices.json")
    ex = dec[title]
    ex['test_amount'] += 1
    ind = ex['test_amount']

    with open(f"{title}/in_{ind}.txt", 'w') as mf:
        mf.write(inp)
    mf.close()
    with open(f"{title}/out_{ind}.txt", 'w') as mf:
        mf.write(out+"\n")
    mf.close()

    database.write("exercices.json", dec)

def show_user(u_disc, user):
    dec = database.read("exercices.json")
    embed = discord.Embed(title=f"Profile de {user['name']}")
    embed.set_thumbnail(url=str(u_disc.avatar_url))
    desc = f":bar_chart: __Score total : **{user['score']['general']}pts**__\n"
    for l in listLang:
        try: desc += f"▸ **{l.capitalize()}** : {user['score'][l]}pts\n"
        except KeyError: desc += f"▸ **{l.capitalize()}** : 0pts\n"
    embed.description = desc
    exercices = ""
    for title, ex in user['submit'].items():
        exercices += f"▸ {title} ({dec[title]['difficulty']}:star:) **{user['submit'][title]['best_score']}pts**"
        exercices += " :white_check_mark:\n" if bool(ex['complete']) else " :x:\n"
    if exercices == "": exercices = "*Aucune participation n'a été trouvée !*"

    embed.add_field(name=f"Épreuves ({len(user['submit'])}/{len(dec)})", value=exercices)
    embed.set_footer(text='Créé le')
    embed.timestamp = datetime.strptime(user['date'], '%x %X')
    return embed


client.run(open("TOKEN", 'r').read())