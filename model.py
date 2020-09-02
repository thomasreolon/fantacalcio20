import json
import random
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle


I = 0
ONLY_BIG = True

with open('./data/footballers.json') as fin:
    data = json.load(fin)

# dataset
X, Y, Xt, Yt = [], [], [], []
for foot in data:
    items1 = data[foot]['1'].items()
    items2 = data[foot]['2'].items()
    items1 = [y for x, y in items1]
    items2 = [y for x, y in items2]

    if items1[4] == 0 or items2[4] == 0:  # drop if vote = 10
        continue
    if random.random() > 0.97:  # already done testing
        X.append(items1+items2)
        Y.append(data[foot]['3']['fanta'])
    else:
        Xt.append(items1+items2)
        Yt.append(data[foot]['3']['fanta'])


# train
if I == 0:
    pred_fanta = MLPRegressor(hidden_layer_sizes=(4), max_iter=2000)
    pred_fanta.fit(X, Y)
    Yp = pred_fanta.predict(Xt)
elif I == 1:
    pred_fanta = LinearRegression().fit(X, Y)
    Yp = pred_fanta.predict(Xt)

if ONLY_BIG:
    todel = []
    Yp = [x for x in Yp]
    for i in range(len(Yt)):
        if Yt[i] < 6.5:
            todel.append(i)
    for x in reversed(todel):
        del Yt[x]
        del Yp[x]


# test
totErr = 0
for y1, y2 in zip(Yt, Yp):
    totErr += abs(y1-y2)
totErr /= len(Yt)

# out
out = ["{}->{} ({})".format(x, y, y2)
       for x, y, y2 in zip(Xt, Yt, Yp)]
print(
    """
dataset={}|{} ---> {}
\t{}
    """.format(len(X), len(Xt), totErr, "\n\t".join(out[:5]))
)


print("save?(y|N)")
if input().lower() == 'y':
    pickle.dump(pred_fanta, open(
        './models/{}-{}.pk'.format(I, str(totErr)[:4]), 'wb'))
