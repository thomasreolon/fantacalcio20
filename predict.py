import pickle
import json

FILEN = ['1-0.53', '1-0.75']
results = {}

# load dataset
with open('./data/footballers.json') as fin:
    data = json.load(fin)

X, names = [], []
for foot in data:
    names.append(foot)
    items1 = data[foot]['2'].items()
    items2 = data[foot]['3'].items()
    X.append([y for x, y in items1]+[y for x, y in items2])


# for each model
for f in FILEN:
    model = pickle.load(open('./models/{}.pk'.format(f), 'rb'))
    Yp = model.predict(X)

    # results
    for n, v in zip(names, Yp):
        if n not in results:
            results[n] = 0
        results[n] += v

for k, v in results.items():
    print(k, "->", v/len(FILEN))
