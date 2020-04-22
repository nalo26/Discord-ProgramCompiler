import discord
from discord.ext import commands
import os

from compiler import compute
import database
from datetime import datetime
from shutil import rmtree

client = commands.Bot(command_prefix = "!")

ADMIN = [250989853158801419, 520334699046895617]

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
@client.command(aliases=['createTest'])
async def create(ctx, *argv):
    if not is_admin(ctx.message.author.id): return
    if not is_dm(ctx.channel): return
    title = ""
    description = ""
    inputs = ""
    output = ""
    difficulty = 1
    hidden = False
    for i, arg in enumerate(argv):
        if len(argv)-1 >= i+1 and '-' not in argv[i+1]:
            if arg in ['-t', '--title']: title = argv[i+1]
            if arg in ['-D', '--description']: description = argv[i+1]
            if arg in ['-i', '--input']: inputs = argv[i+1]
            if arg in ['-o', '--output']: output = argv[i+1]
            if arg in ['-d', '--difficulty']: difficulty = int(argv[i+1])
            if arg in ['-h', '--hidden']: hidden = bool(argv[i+1].lower() == 'true')

    try:
        database.read("exercices.json")[title]
        await ctx.send(f":x: **Un défi du nom de `{title}` existe déjà ! **")
    except KeyError: await ctx.send(embed=create_ex(title, difficulty, description, inputs, output, hidden))

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
    for i, arg in enumerate(argv):
        if len(argv)-1 >= i+1 and '-' not in argv[i+1]:
            if arg in ['-t', '--title']: title = argv[i+1]
            if arg in ['-D', '--description']: description = argv[i+1]
            if arg in ['-i', '--input']: inputs = argv[i+1]
            if arg in ['-o', '--output']: output = argv[i+1]
            if arg in ['-d', '--difficulty']: difficulty = int(argv[i+1])
            if arg in ['-h', '--hidden']: hidden = bool(argv[i+1].lower() == 'true')

    try:
        database.read("exercices.json")[title]
        await ctx.send(embed=edit_ex(title, difficulty, description, inputs, output, hidden))
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
        add_test(title, inputs.replace("\\n", "\n"), outputs.replace("\\n", "\n"))
        await ctx.send(f":white_check_mark: **Test pour le défi `{title}` créé avec succès !**")
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
@client.command(aliases=["exercices", "list", "liste", "listes", "detail"])
async def exercice(ctx, name=""):
    dec = database.read("exercices.json")
    if name == "": # loop all exercice
        await ctx.send(embed=show_all_ex())
    else: # specific exercice
        try: ex = dec[name]
        except KeyError:
            await ctx.send(f":x: **Aucun exercice du nom de `{name}` n'a été trouvé !**")
            return
        await ctx.send(embed=show_ex(name, ex))

@client.command(aliases=['profil', 'me'])
async def profile(ctx):
    dec = database.read("users.json")
    u_disc = ctx.message.author
    try: user = dec[str(u_disc.id)]
    except KeyError: user = database.create_user(dec, u_disc.id)
    await ctx.send(embed=show_user(u_disc, user))

@client.command(aliases=['classement', 'top'])
async def leaderboard(ctx):
    dec = database.read("users.json")
    res = {}
    for u in dec.values():
        res[u['name']] = u['score']
    res = sorted(res.items(), key = lambda kv:(kv[1], kv[0]))
    
    embed = discord.Embed(title=":trophy: Classement général")
    desc = ""
    for i, (name, score) in enumerate(res):
        desc += f"{i+1} : {name} ({score}pts)\n"
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

    try: os.mkdir(f"{exercice}/{author}")
    except FileExistsError: pass
    print("=====================================================================")
    print(f"'{filename}' by {message.author.name}#{message.author.discriminator}")
    path = f"{exercice}/{author}"
    await file.save(f"{path}/{filename}")
    print(f"File '{filename}' saved to '{path}/{filename}'")

    msg = await client.get_user(author).send(f"Téléchargement du programme {filename}...")
    
    try: username = client.get_guild(688355824934060032).get_member(author).nick
    except Exception: username = client.get_user(author).display_name
    await compute(path, filename, extension, exercice, msg, author, username)

def is_admin(u_id):
    return u_id in ADMIN
def is_dm(channel):
    return isinstance(channel, discord.DMChannel)

def create_ex(title, difficulty, desc, inputs, output, hidden):
    os.mkdir(title)
    dec = database.read("exercices.json")
    data = {'difficulty': difficulty, 'date': database.get_time(), 'description': desc, 'inputs': inputs, 'output': output, 'hidden': hidden, 'test_amount': 0, 'executed_test': 0}
    dec[title] = data
    database.write("exercices.json", dec)
    return show_ex(title, data)

def edit_ex(title, difficulty, desc, inputs, output, hidden):
    dec = database.read("exercices.json")
    ex = dec[title]
    if difficulty != -1: ex['difficulty'] = difficulty
    if desc != "": ex['description'] = desc
    if inputs != "": ex['inputs'] = inputs
    if output != "": ex['output'] = output
    if hidden is not None: ex['hidden'] = hidden
    database.write("exercices.json", dec)
    return show_ex(title, ex)

def delete_ex(title):
    rmtree(title, ignore_errors=True)
    dec = database.read("exercices.json")
    del dec[title]
    database.write("exercices.json", dec)
    
def show_ex(title, data):
    embed = discord.Embed(title=f"{title} ({data['difficulty']}:star:)")
    embed.description = data['description'] if data['description'] != "" else "*Non défini*"
    embed.add_field(name="Entrées :", value=data['inputs'] if data['inputs'] != "" else "*Non défini*")
    embed.add_field(name="Sortie :", value=data['output'] if data['output'] != "" else "*Non défini*")

    embed.set_footer(text='Créé le')
    embed.timestamp = datetime.strptime(data['date'], '%x %X')
    return embed

def show_all_ex():
    dec = database.read("exercices.json")
    embed = discord.Embed(title=f"Liste des défis ({len(dec)})")
    desc = ""
    for title, ex in dec.items():
        desc += f"▸ {title} ({ex['difficulty']}:star:)\n"
    embed.description = desc if desc != "" else "Aucun défi n'a été trouvé !"
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
    embed.description = f":bar_chart: Score total : **{user['score']}**\n"
    exercices = ""
    for title, ex in user['submit'].items():
        exercices += f"▸ {title} ({dec[title]['difficulty']}:star:)"
        exercices += " :white_check_mark:\n" if bool(ex['complete']) else " :x:\n"
    if exercices == "": exercices = "Aucune participation n'a été trouvée !"

    embed.add_field(name=f"Épreuves ({len(user['submit'])}/{len(dec)})", value=exercices)
    embed.set_footer(text='Créé le')
    embed.timestamp = datetime.strptime(user['date'], '%x %X')
    return embed


client.run("NzAxNDEwMjk1MzE0MzgyODc4.XqAF_A.c2wa8C88DpD1Wi3WWIfn_oiR1ac")