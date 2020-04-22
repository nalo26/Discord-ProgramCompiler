import json
from datetime import datetime
import pytz

def create_user(dec, user):
    u_create = {'id': user, 'score': 0, 'submit': []}
    dec.append(u_create)
    write(dec)
    return u_create

def add_submition(user_id, exer, lang, tests, complete, score):
    dec = read()
    user = get_user(dec, user_id)
    if user == -1: user = create_user(dec, user_id)
    test = get_test(user, exer.lower())
    if test == -1:
        test = {'exercice': exer.lower(), 'language': lang, 'date': get_time(), 'complete_test': tests, 'complete': complete, 'score': score}
        user['submit'].append(test)
        user['score'] += score
        write(dec)
        return True, test
    if score <= test['score']: return False, test
    # test['exercice'] = exer
    test['language'] = lang
    test['date'] = get_time()
    test['complete_test'] = tests
    test['complete'] = complete
    user['score'] -= test['score']
    user['score'] += score
    test['score'] = score
    write(dec)
    return True, test
    
def get_test(user, exer_name):
    for ex in user['submit']:
        if ex['exercice'] == exer_name: return ex
    return -1

def get_user(dec, u_id):
    for user in dec:
        if user['id'] == u_id: return user
    return -1

def get_exo(user, ex_id):
    for exer in user['submit']:
        if exer['id'] == ex_id: return exer
    return -1

def read():
    with open('users.json', 'r') as mf:
        dec = json.load(mf)
    mf.close()
    return dec

def write(data):
    with open('users.json', 'w') as mf:
        json.dump(data, mf, indent=4)
    mf.close()

def get_time(time_format='%x %X'):
    tz_FR = pytz.timezone('Europe/Paris')
    time = datetime.now(tz_FR)
    return str(time.strftime(time_format))