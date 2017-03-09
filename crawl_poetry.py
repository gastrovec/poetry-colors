import re
import os
import sys
import json
import requests
from time import sleep
from bs4 import BeautifulSoup as Soup
from collections import defaultdict, Counter

def limit(iterable, number=10):
    """Yield the top n elements of an iterable, like 'head' on unix.

    From github.com/L3viathan/toolib
    """
    for x, _ in zip(iterable, range(number)):
        yield x

try:
    with open("links.txt") as f:
        #words = defaultdict(Counter)
        for url in f:
            print("Downloading", url, end="", file=sys.stderr)
            r = requests.get(url.strip())
            if r.status_code != 200:
                print("Error with this one.", file=sys.stderr)
                continue
            sp = Soup(r.text)
            text = sp.find("div", {"id": "gutenb"}).text
            author = sp.find("div", {"class": "gbbreadcrumb"}).find_all("a")[1]["href"]
            author = author.split("/")[-1].strip()
            #words[author].update(map(lambda x: x.group().lower(), re.finditer("[a-zA-ZäüöÄÖÜ'ß]+", text)))
            folder = "poems/" + author
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(folder + "/" + '_'.join(url.split("/")[-2:]).strip(), 'w') as f:
                f.write(text)
            sleep(0.02)
except Exception as e:
    print("Error.", e, file=sys.stderr)
finally:
    '''with open("words.json", "w") as g:
        print("Dumping JSON file...", file=sys.stderr)
        json.dump(words, g)
    '''
    print("All done.", file=sys.stderr)
