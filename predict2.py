import pickle
import json
import random

X1, X2, names, roles = [], [], [], []
models = ['1', '6', 'b3']
averages = {}

with open('./data/fantadata.json', 'r') as fin:
    data = json.load(fin)


for foot in data:
    pl = data[foot]
    if '18' in pl and '19' in pl:
        averages[foot] = {'vote': 0}
        names.append(foot)
        roles.append(pl['19']['role'])
        x = [pl['18']['vote'], pl['18']['fanta'], pl['18']['goals'],
             pl['19']['vote'], pl['19']['fanta'], pl['19']['goals']]
        x2 = [y for x, y in pl['18'].items()] + \
            [y for x, y in pl['19'].items()]
        X1.append(x)
        X2.append(x2)

for fname in models:
    model = pickle.load(open('./best_models/{}.pk'.format(fname), 'rb'))
    if 'b' in fname:
        X = X1
    else:
        X = X2
    Yp = model.predict(X)

    for name, y, r in zip(names, Yp, roles):
        averages[name]['vote'] += y/len(models)
        averages[name]['role'] = r

res2 = []
for k, v in averages.items():
    res2.append((k, v['vote'], v['role']))


def sf(k):
    return k[1]


res2.sort(key=sf, reverse=True)


cc = [(x, y-5, z) for x, y, z in res2 if z == 4][:60]
aa = [(x, y-5, z) for x, y, z in res2 if z == 8][:40]

ctot, atot = 0, 0
for block in cc:
    ctot += block[1]**2
for block in aa:
    atot += block[1]**2

prices = {}
for name, vote, role in cc:
    prices[name] = (100+int(role)*15)*10 * vote**2 / ctot
r = 0
for name, vote, role in aa:
    r += vote**2
    prices[name] = (100+int(role)*15)*10 * (vote**2) / atot

with open('./results/res2.json', 'w') as fout:
    json.dump(prices, fout)
