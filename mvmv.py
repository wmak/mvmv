import codecs
import sqlite3
import re
from fuzzywuzzy import fuzz

# common words in movies that we don't want to search the database for
common_words = [
            "The",
            "Them",
            "A",
            "An",
            ]

# blacklist of common garbage that fills up movie names
blacklist = [
            "BluRay",
            "\d{3,4}p",
            "(HD|DVD)Rip",
            "x\d{3}",
            "XViD(-.*)?",
            ]

# compile the blacklist into a regex
bl_re = re.compile("(" + "|".join(blacklist) + ")(\s|$)", re.IGNORECASE)

conn = sqlite3.connect("movies.db")
c = conn.cursor()

# Setup the sqlite database
def search(query):
    # remove all instancer of 'WORD ' for WORD in blacklist
    query = query.replace(".", " ")
    query = bl_re.sub("", query)

    year = re.search("(19|20)\d{2}", query).group(0)

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
    conn.close
