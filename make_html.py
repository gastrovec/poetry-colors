from toolib.tools import CSV

header = """<html>
    <head>
<style>
* {
    margin:0;
    padding: 0;
    border: 0;
}
.outer {
    line-height: 4px;
    width:920px;
    display: flex;
    margin-left: auto;
    margin-right: auto;
    transition: width 1s;
    animation-name: pageLoad;
    animation-iteration-count: 1;
    animation-duration:1s;
    animation-timing-function: ease-out;
    }
@keyframes pageLoad {
0% {
    width:920px;
    }
20% {
    width:100%;
    }
100% {
    width:920px;
    }
}

.authorname {
    display:none;
    font-family: sans-serif;
    }
.outer:hover {
    line-height: 25px;
    width: 100%;
    transition: width 0.2s;
    }
.outer:hover .authorname {
    display: inline;
    margin:5px;
    position: fixed;
    top: 0px;
    left: 0px;
    background: rgb(2,43,54);
    color: rgb(253,246,228);
    font-weight: bold;
    padding: 10px;
}

body {
background: rgb(253,246,228);
}

</style>
</head>
<body>"""

footer = """</body>
</html>"""

start_color = 1

solarized = {"yellow": "rgb(181, 136, 29)", "red": "rgb(219,53,54)", "blue": "rgb(38,115,170)", "green": "rgb(129,147,25)", "purple": "rgb(99,106,177)", "pink": "rgb(209,58,130)", "golden": "#FFC500", "black": "rgb(2,43,54)", "gray": "rgb(148,162,162)"}

color_scheme = {"purple": "#380470", "yellow": "#FFEE00", "golden":"#FFC500", "blue":"#2419B2", "pink":"#B40097", "red":"#A60000", "gray":"#FF0000", "green":"#003619", "brown":"#4C2C00", "silver":"#596363"}

color_scheme = solarized

def to_name(authorname):
    return " ".join(map(lambda x: x.capitalize() if x != "von" else x, filter(str.isalpha, authorname.split("-"))))

with open("wikiauthors.csv") as f:
    dates = {}
    for line in f:
        aid, born, died = line.strip().split(",")
        dates[aid] = (int(born), int(died))

with CSV(open("colors_pos.tsv"), delimiter="\t") as f, open("out_pos.html", "w") as html:
    html.write(header)
    for line in sorted(f, key=lambda x: dates[x.author][1]):
        colors = tuple(map(float,line[start_color:]))
        s = sum([colors[0]] + list(colors[2:]))
        if s==0:
            continue
        if s < 10:
            continue  # only enough contributions
        html.write("""<div class="outer">""")
        for colname, value in zip(line._fields[start_color:], colors):
            html.write("""<div class="inner" style="display: inline-block; background-color:{}; width: {}%;">&nbsp;</div>""".format(
                color_scheme.get(colname, colname),
                100*value/s,
                ))
        html.write("""<span class="authorname">{} (*{} &dagger;{})</span>""".format(to_name(line.author), *dates[line.author]))
        html.write("""</div>""")
