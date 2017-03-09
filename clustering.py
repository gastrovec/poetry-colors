import json
import code
import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans
from collections import defaultdict, Counter

number_of_clusters = 4

with open("data.json") as f:
    j = json.load(f)

all_colors = ['black', 'white', 'grey', 'brown', 'red', 'blue', 'yellow', 'green', 'orange', 'violet', 'gold', 'silver']

def div(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return 0

ls, authors = [], []
for author in j:
    if j[author]['lang'] != 'de': continue
    if j[author]['word_count'] >= 10000: continue
    total = sum(j[author]['color_counts'].values())
    ls.append([div(j[author]['color_counts'].get(color, 0), total) for color in all_colors])
    authors.append(author)

X = np.array(ls)

# k = KMeans(number_of_clusters)
k = AgglomerativeClustering(number_of_clusters)

k.fit(X)

clusters = defaultdict(list)

for aid, cid in zip(authors, k.labels_):
    clusters[cid].append(aid)

# for key in clusters:
#     clusters[key] = sum(clusters[key]) / len(clusters[key])

code.interact(local=locals())
