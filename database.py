import json
from datetime import datetime
import pytz

def create_user(dec, name, user):
    u_create = {'name': name, 'date': get_time(), 'score': 0, 'submit': {}}
    dec[user] = u_create
    write("users.json", dec)
    return u_create

def add_submition(user_id, user_name, exer, lang, tests, complete, score):
    dec = read("users.json")
    try: user = dec[str(user_id)]
    except KeyError: user = create_user(dec, user_name, user_id)
    try: 
        test = user['submit'][exer]
        if score <= test['score']: return False, test
    except KeyError: test = {}
    test['date'] = get_time()
    test['language'] = lang
    test['tests'] = tests
    test['complete'] = complete
    test['score'] = score

    user['submit'][exer] = test
    user['score'] += score
    write("users.json", dec)
    return True, test

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
    tz_FR = pytz.timezone('Europe/Paris')
    time = datetime.now(tz_FR)
    return str(time.strftime(time_format))