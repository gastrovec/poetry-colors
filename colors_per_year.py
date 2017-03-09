import sys
import json
import code
from collections import defaultdict, Counter
from itertools import chain

with open("data.json") as f:
    d = json.load(f)

years = defaultdict(Counter)
totals = Counter()

for aid in d:
    if d[aid]['lang'] != 'de': continue
    if d[aid]['word_count'] < 5000: continue  # debug
    year = d[aid]['year_of_birth'] + 21
    for color in d[aid]['color_counts']:
        # if color == 'silver': continue  # debug
        # if color == 'gold': continue  # debug
        if color == 'orange': continue  # debug
        if color == 'violet': continue  # debug
        years[year][color] += d[aid]['color_counts'][color]
        totals[year] += d[aid]['color_counts'][color]

colors = list(set(chain.from_iterable(years[y].keys() for y in years)))

# code.interact(local=locals())

print("year,color,freq")
for year in sorted(years):
    # print(year, ",", sep="", end="")
    # print(",".join(str(years[year][color] / totals[year]) for color in colors))
    if year <1700: continue  # debug
    for color in colors:
        print(year, color, years[year][color] / totals[year], sep=",")
