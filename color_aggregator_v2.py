import re
import json
from glob import iglob
from collections import Counter, defaultdict
from polyglot.text import Text

colors = {
        'blue': r'\bbl[aä]u(e[rmsn]?)?\b',
        'red': r'\br[oö]t(e[rsmn]?)?\b',
        'yellow': r'\bgelb(e[rmsn]?)?\b',
        'green': r'\bgrün(e[rsmn]?)?\b',
        'orange': r'\borange(ne[rsmn]?)?\b',
        'violet': r'\bviolett(e[rsnm]?)?\b',
        'black': r'\bschw[aä]rz(e[rmsn]?)?\b',
        'white': r'\bweiß(e[rsnm]?)?\b',
        'grey': r'\bgr[aä]u(e[rsnm]?)?\b',
        'brown': r'\bbr[aä]un(e[rsnm]?)?\b',
        'silver': r'\bsilber(n(e[rsnm]?)?)?\b',
        'gold': r'\bg[oü]ld(en(e[rsnm]?)?)?\b',
        }

authors = defaultdict(Counter)
sentiments = defaultdict(Counter)

for author_folder in iglob("poems/*"):
    author = author_folder.split("/")[-1]
    for poem_file in iglob(author_folder + "/*"):
        with open(poem_file) as f:
            for line in f:
                t = Text(line, hint_language_code="de")
                for word, tag in t.pos_tags:
                    if tag in ("ADJ", "ADV", "PROPN"):
                        for color, pattern in colors.items():
                            if re.match(pattern, word):
                                authors[author][color] += 1
                for word in t.words:
                    pol = word.polarity
                    if pol == -1:
                        sentiments[author]['negative'] += 1
                    elif pol == 1:
                        sentiments[author]['positive'] += 1


with open("colors_pos.tsv", "w") as f:
    ordered_colors = (
            'black',
            'white',
            'grey',
            'red',
            'green',
            'blue',
            'yellow',
            'orange',
            'violet',
            'brown',
            'silver',
            'gold',
            )
    f.write('author\t')
    f.write('\t'.join(ordered_colors))
    f.write("\n")
    for author in authors:
        f.write(author)
        f.write("\t")
        f.write("\t".join(str(authors[author][color]) for color in ordered_colors))
        f.write("\n")

with open("author_polarity.csv", "w") as f:
    f.write("author,positive,negative\n")
    for aid in sentiments:
        f.write("{},{},{}\n".format(aid, sentiments[aid]['positive'], sentiments[aid]['negative']))
