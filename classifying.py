import json
import code
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from collections import defaultdict, Counter

with open("data.json") as f:
    j = json.load(f)

all_colors = ['black', 'white', 'grey', 'brown', 'red', 'blue', 'yellow', 'green', 'orange', 'violet', 'gold', 'silver']
good_colors = ['black', 'white', 'red', 'blue', 'yellow', 'green',]
all_movements = ['Barock', 'Historismus', 'Rokoko', 'Empfindsamkeit', 'Moderne', 'Heimatdichtung', 'Realismus', 'Nationalismus', 'Aufklärung', 'Renaissance', 'Avantgarde', 'Biedermaier', 'Expressionismus', 'Exilliteratur', 'Junges_Deutschland', 'Vormärz', 'Romantik', 'Klassik', 'Biedermeier', 'Naturalismus', 'Sturm_und_Drang', 'Neue_Sachlichkeit', 'Humanismus', 'Weimarer_Republik', 'Mittelalter']
good_movements = ['Realismus', 'Moderne', 'Romantik', 'Aufklärung', 'Expressionismus', 'Vormärz'] #, 'Heimatdichtung', 'Naturalismus', 'Biedermeier', 'Klassik']

def div(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return 0

def movement_label(ls):
    ls = [*filter(lambda x: x in good_movements, ls)]
    if not ls:
        return None, 0  # no movement
    else:
        #return ls[0], all_movements.index(ls[0]) + 1
        return ls[0], good_movements.index(ls[0]) + 1


x_ls, authors = [], []
y_ls, movements = [], []
for author in j:
    if j[author]['lang'] != 'de': continue
    if j[author]['word_count'] < 1000: continue
    total = sum(j[author]['color_counts'].get(color, 0) for color in all_colors)
    movement, movement_id = movement_label(j[author]['movements'])
    if movement_id == 0: continue  # be fair, don't judge unknowns
    x_ls.append([div(j[author]['color_counts'].get(color, 0), total) for color in all_colors])
    y_ls.append(movement_id)
    authors.append(author)
    movements.append(movement)

X = np.array(x_ls)
Y = np.array(y_ls)

print(len(X), len(Y))

# code.interact(local=locals())

log, nb, svm, rf, dumm = [], [], [], [], []

for iteration in range(1000):
    print("Iteration", iteration)
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.10)

    classifier = LogisticRegression()
    classifier.fit(x_train, y_train)
    # print("logistic:", cross_val_score(classifier, X, Y, cv=10))
    log.append(classifier.score(x_test, y_test))

    classifier = GaussianNB()
    classifier.fit(x_train, y_train)
    # print("NaiveBaes:", cross_val_score(classifier, X, Y, cv=10))
    nb.append(classifier.score(x_test, y_test))

    classifier = SVC()
    classifier.fit(x_train, y_train)
    # print("NaiveBaes:", cross_val_score(classifier, X, Y, cv=10))
    svm.append(classifier.score(x_test, y_test))

    classifier = RandomForestClassifier()
    classifier.fit(x_train, y_train)
    # print("NaiveBaes:", cross_val_score(classifier, X, Y, cv=10))
    rf.append(classifier.score(x_test, y_test))

    dummy = DummyClassifier()
    dummy.fit(x_train, y_train)
    # print("Dummy:", cross_val_score(classifier, X, Y, cv=10))
    dumm.append(dummy.score(x_test, y_test))

print("logistic r average:", sum(log)/len(log))
print("Naive Baes average:", sum(nb)/len(nb))
print("SVMachines average:", sum(svm)/len(svm))
print("RandomFrst average:", sum(rf)/len(rf))
print("Dummy dumm average:", sum(dumm)/len(dumm))

# code.interact(local=locals())
