import pickle
import json
import random

Xt, Yt, names = [], [], []
test_names = {'dybala', 'higuain', 'immobile', 'zielinski',
              'pjanic', 'duncan', 'freuler', 'spinazzola', 'lukaku r.', }

with open('./data/fantadata.json', 'r') as fin:
    data = json.load(fin)

# get dataset (for testing)
for i in range(15, 20):
    for foot in data:
        pl = data[foot]
        if str(i) in pl and str(i+1) in pl and str(i+2) in pl:
            if pl[str(i+2)]['fanta'] < 6.2:
                continue
            names.append(foot)
            x = [pl[str(i)]['vote'], pl[str(i)]['fanta'], pl[str(i)]['goals'], pl[str(
                i+1)]['vote'], pl[str(i+1)]['fanta'], pl[str(i+1)]['goals']]
            # x = [y for x, y in pl[str(i)].items()] + \
            #[y for x, y in pl[str(i+1)].items()]
            Xt.append(x)
            Yt.append(pl[str(i+2)]['fanta'])


# shows the prediction
for i in range(1, 6):
    model = pickle.load(open('./models/b{}.pk'.format(i), 'rb'))
    Yp = model.predict(Xt)
    err, t = 0, 0
    for y, yy in zip(Yt, Yp):
        if yy > 6:
            err += abs(y-yy)
            t += 1
    print("\033[91m ----> model:{} -> err:{} \033[0m".format(i, err/t))
    for x, y, y2, name in zip(Xt, Yt, Yp, names):
        if name in test_names:
            print(name, y2-y, "   |", x)
