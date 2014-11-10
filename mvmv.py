import codecs
import sqlite3
import re
from fuzzywuzzy import fuzz

def search(query):
    common_words = [
        "The",
        "Them",
        "A",
        "An",
        ]

    blacklist = [
        "BluRay",
        "\d{3,4}p",
        "(HD|DVD)Rip",
        "x\d{3}",
        "XViD",
        ]

    # Setup the sqlite database
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()
    query = query.replace(".", " ")

    # remove all instancer of 'WORD ' for WORD in blacklist
    bl_re = re.compile("(" + "|".join(blacklist) + ")(\s|$)", re.IGNORECASE)
    query = bl_re.sub("", query)

    m = re.search("(\d{4})", query)
    for match in m.groups():
        if match != "1080":
            year = match

    # Find the first relevant word
    word = ""
    for item in query.split(" "):
        if item not in common_words:
            word = item
            break

    c.execute("SELECT * FROM movies WHERE movies MATCH ?",
            ["%s %s" % (word, year)])

    ratio = 0
    best = query
    for item in c:
        current = fuzz.ratio(item[0], query)
        for word in item[0].split():
            if word not in query:
                current -= 10
        if item[0] in query and len(item[0].split()) > 1:
            ratio = 100
            best = item[0]
        elif current > ratio:
            ratio = current
            best = item[0]
    return best

if __name__ == "__main__":
    import sys
    print(search(sys.argv[0]))
