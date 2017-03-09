from toolib.tools import CSV
from collections import Counter, defaultdict
import json

authors = defaultdict(lambda: {'color_counts': Counter()})

with CSV(open("author_counts.csv"), header=False) as f:
    for aid, count in f:
        authors[aid]['word_count'] = int(count)

with CSV(open("colors_pos.tsv"), delimiter="\t") as f:
    for line in f:
        d = line._asdict()
        for key in (k for k in d.keys() if k != 'author'):
            authors[line.author]['color_counts'][key] = int(d[key])

with CSV(open("wikiauthors.csv"), header=False) as f:
    for aid, birth, death in f:
        authors[aid]['year_of_birth'] = int(birth)
        authors[aid]['year_of_death'] = int(death)

with CSV(open("author_polarity.csv")) as f:
    for aid, positive, negative in f:
        positive, negative = int(positive), int(negative)
        authors[aid]['pol_pos'] = positive
        authors[aid]['pol_neg'] = negative
        authors[aid]['pol_avg'] = (positive-negative)/(positive+negative)

with CSV(open("movements.csv")) as f:
    for aid, *_, movements, GND, lang in f:
        # empty list for empty string:
        authors[aid]['movements'] = [*filter(bool, movements.split("+"))]
        authors[aid]['GND'] = GND
        authors[aid]['lang'] = lang

for aid in authors:
    name = " ".join(map(lambda x: x.capitalize() if x != "von" else x, filter(str.isalpha, aid.split("-"))))
    # name = name.replace("Bjrn", "Bjørn")
    authors[aid]['name'] = name
    authors[aid]['color_percentage'] = sum(authors[aid]['color_counts'].values()) / authors[aid]['word_count']

with open("data.json", "w") as f:
    json.dump(authors, f)
