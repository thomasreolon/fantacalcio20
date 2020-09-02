import pickle
import json
import random

X1, X2, names = [], [], []
models = ['1', '6', 'b3']
averages = {}

fout = open('./results2.txt', 'w')

with open('./data/fantadata.json', 'r') as fin:
    data = json.load(fin)


for foot in data:
    pl = data[foot]
    if '18' in pl and '19' in pl:
        averages[foot] = 0
        names.append(foot)
        x = [pl['18']['vote'], pl['18']['fanta'], pl['18']['goals'],
             pl['19']['vote'], pl['19']['fanta'], pl['19']['goals']]
        x2 = [y for x, y in pl['18'].items()] + \
            [y for x, y in pl['19'].items()]
        X1.append(x)
        X2.append(x2)

for fname in models:
    fout.write(
        "\n\033[91m-----------------------------------------------\033[0m")
    model = pickle.load(open('./best_models/{}.pk'.format(fname), 'rb'))
    if 'b' in fname:
        X = X1
    else:
        X = X2
    Yp = model.predict(X)

    for name, y in zip(names, Yp):
        averages[name] += y
        fout.write("\n{} -> {}".format(name, y))

fout.write(
    "\n\033[91m--------------------avgs---------------------------\033[0m")
for name, y in averages.items():
    fout.write("\n{} -> {}".format(name, y/len(models)))
    averages[name] = y/len(models)

fout.write(
    "\n\033[91m---------------------------------------------------\033[0m")
for name, y in averages.items():
    diff = y-6.1
    y += diff*abs(diff)

    fout.write("\n{} -> {}".format(name, y))
