import json
from datetime import datetime
import pytz

def create_user(dec, name, user):
    u_create = {'name': name, 'date': get_time(), 'score': {'general': 0}, 'submit': {}}
    dec[user] = u_create
    write("users.json", dec)
    return u_create

def add_submition(user_id, user_name, exer, lang, tests, complete, score):
    dec = read("users.json")
    try: user = dec[str(user_id)]
    except KeyError: user = create_user(dec, user_name, user_id)
    try: ex = user['submit'][exer]
    except KeyError: ex = {"best_score": 0, "complete": False}
    try: sub = ex[lang]
    except KeyError: sub = {}
    ret = ""
    try:
        if score <= sub['score']: ret = f"Tu as déjà réussi cet exercice en `{'` ,`'.join([name.capitalize() for name, data in ex.items() if name not in ['best_score', 'complete'] and bool(data['complete'])])}` !"
    except KeyError: pass
    
    if ret == "":
        try:
            user['score'][lang] -= sub['score']
            user['score'][lang] += score
        except KeyError: user['score'][lang] = score

        sub['time'] = get_time()
        sub['tests'] = tests
        sub['complete'] = complete
        sub['score'] = score

        if not bool(ex['complete']) and complete: ex['complete'] = complete

        ex[lang] = sub
        if score > ex['best_score']:
            user['score']['general'] -= ex['best_score']
            user['score']['general'] += score
            ex['best_score'] = score
            ret = f"C'est ton meilleur score sur cet exercice ({score} pts) !"
        else: ret = f"C'est ton meilleur score en `{lang.capitalize()}` ({score} pts) !"
        user['submit'][exer] = ex

    write("users.json", dec)
    return ret


def create_submition():
    pass


def read(path):
    with open(path, 'r') as mf:
        dec = json.load(mf)
    mf.close()
    return dec

def write(path, data):
    with open(path, 'w') as mf:
        json.dump(data, mf, indent=4)
    mf.close()

def get_time(time_format='%x %X'):
    # tz_FR = pytz.timezone('Europe/Paris')
    # tz_FR = None
    tz_FR = pytz.timezone('Etc/GMT-0')
    time = datetime.now(tz_FR)
    return str(time.strftime(time_format))