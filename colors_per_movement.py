import sys
import json
import code
from collections import defaultdict, Counter
from itertools import chain

with open("data.json") as f:
    d = json.load(f)

good_movements = ['Realismus', 'Moderne', 'Romantik', 'Aufklärung', 'Expressionismus', 'Vormärz'] #, 'Heimatdichtung', 'Naturalismus', 'Biedermeier', 'Klassik']

movements = defaultdict(Counter)
totals = Counter()

movement_counts = Counter()

for aid in d:
    if d[aid]['lang'] != 'de': continue
    for movement in d[aid]['movements']:
        if movement not in good_movements: continue
        movement_counts[movement] += 1
        for color in d[aid]['color_counts']:
            if color in ('violet', 'orange'): continue
            movements[movement][color] += d[aid]['color_counts'][color]
            totals[movement] += d[aid]['color_counts'][color]

colors = list(set(chain.from_iterable(movements[e].keys() for e in movements)))

# code.interact(local=locals())

print("movement,color,freq")
for movement in movements:
    if movement_counts[movement] < 10: continue  # debug
    for color in colors:
        print(movement, color, movements[movement][color] / totals[movement], sep=",")
