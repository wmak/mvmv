import codecs
import mimetypes
import os
import re
import sqlite3
from fuzzywuzzy import fuzz

# common words in movies that we don't want to search the database for
common_words = [
            "The",
            "Them",
            "A",
            "An",
            "In",
            ]

# blacklist of common garbage that fills up movie names
blacklist = [
            "BluRay",
            "\d{3,4}p",
            "(HD|DVD|BR)Rip",
            "x\d{3}",
            "XViD(-.*)?",
            "AC3-EVO",
            ]

# compile the blacklist into a regex
bl_re = re.compile("(" + "|".join(blacklist) + ")(\s|$)", re.IGNORECASE)

# Setup the sqlite database
def search(query, cursor):
    # remove all instancer of 'WORD ' for WORD in blacklist
    query = query.replace(".", " ")
    query = bl_re.sub("", query)

    year = re.search("(19|20)\d{2}", query)
    if year:
        year = year.group(0)

    # Find the first relevant word
    word = ""
    for item in query.split(" "):
        if item not in common_words and len(item) > 3:
            word = item.replace("-", " ")
            break

    cursor.execute("SELECT * FROM movies WHERE movies MATCH ?",
                   ["%s %s" % (word, year)])

    ratio = 0
    best = query
    if year:
        best = best.replace(year, "")
    best = best.strip()
    for item in cursor:
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


def is_valid_file(filename, excludes):
    return str(mimetypes.guess_type(filename)[0]).find('video/') == 0 and \
           not any(map(lambda x: bool(x.match(filename)), excludes))


def get_movies_list(dirname, excludes=None):
    if excludes is None:
        excludes = []

    movies = []
    for root, _, files in os.walk(dirname):
        if any(map(lambda x: x.match(root), excludes)):
            continue

        movies += [(root, mov) for mov in files if is_valid_file(mov, excludes)]
    return movies

def movemovie(src, dst, cursor):
    filename, extension = os.path.splitext(src[1])
    os.rename(os.path.join(src[0]. src[1]),
            "%s/%s%s" % (dst, search(filename, cursor),
            extension))

def movemovies(dirname, dst, cursor, excludes=None):
    for movie in get_movies_list(dirname, excludes):
        movemovie(movie, dst, cursor)

if __name__ == "__main__":
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    import sys
    print(search(sys.argv[1], cursor))

    conn.close()
