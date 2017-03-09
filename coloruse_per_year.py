import sys
import json
import code
from collections import defaultdict, Counter
from itertools import chain

with open("data.json") as f:
    d = json.load(f)

years = Counter()
totals = Counter()

for aid in d:
    if d[aid]['word_count'] < 5000: continue  # debug
    if d[aid]['lang'] != 'de': continue
    year = d[aid]['year_of_birth'] + 21
    for color in d[aid]['color_counts']:
        years[year] += d[aid]['color_counts'][color]
        totals[year] += d[aid]['word_count']

# code.interact(local=locals())

print("year,percentage")
for year in sorted(years):
    # print(year, ",", sep="", end="")
    # print(",".join(str(years[year][color] / totals[year]) for color in colors))
    if year <1700: continue  # debug
    print(year, years[year] / totals[year], sep=",")
