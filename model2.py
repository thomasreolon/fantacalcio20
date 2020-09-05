import json
import random
import pickle
from sklearn import svm, tree, neighbors
from sklearn.linear_model import LinearRegression

X, Y, Xt, Yt = [], [], [], []
ONLY_BIG = True

# models
models = [
    svm.SVR(max_iter=2000),
    LinearRegression(),
    neighbors.KNeighborsRegressor(2, weights='uniform')
]

# loss functions


def f1(a, b): return abs((a-b)*(b-5))
def f3(a, b): return abs(a-b)


print("(err*distance5)    (diff avg)")


def loss(Yt, Yp, f):
    totErr, times = 0, 0
    for y1, y2 in zip(Yt, Yp):
        if not ONLY_BIG or y2 > 6.3:
            totErr += f(y1, y2)
        else:
            times += 1

    return totErr / (len(Yt)-times)


# load dataset
with open('./data/fantadata.json', 'r') as fin:
    data = json.load(fin)

for i in range(15, 20):
    for foot in data:
        pl = data[foot]
        if str(i) in pl and str(i+1) in pl and str(i+2) in pl:
            if pl[str(i+2)]['fanta'] < 6.6:
                continue

            x = [pl[str(i)]['vote'], pl[str(i)]['fanta'], pl[str(i)]['goals'], pl[str(
                i+1)]['vote'], pl[str(i+1)]['fanta'], pl[str(i+1)]['goals']]
            # x = [y for x, y in pl[str(i)].items()] + \
            #[y for x, y in pl[str(i+1)].items()]
            if random.random() < 0.9:
                X.append(x)
                Y.append(pl[str(i+2)]['fanta'])
            else:
                Xt.append(x)
                Yt.append(pl[str(i+2)]['fanta'])
print("--------->{}/{}".format(len(X), len(Xt)))

# train & predict
err = []
for i, model in enumerate(models):
    model = model.fit(X, Y)
    Yp = model.predict(Xt)

    error = (loss(Yt, Yp, f1),  loss(Yt, Yp, f3))
    models[i] = model
    err.append(error)

    print("{} --> {}".format(i, error))


# save best model
print("which do you want to save? (0-1-2)")
idx = None
while(idx == None):
    try:
        idx = int(input())
    except:
        pass

if idx >= 0 and idx < len(models):
    errs = "-".join([str(x)[:3] for x in err[idx]])
    pickle.dump(models[idx],
                open('./models/b{}-{}.pk'.format(idx, errs), 'wb'))
