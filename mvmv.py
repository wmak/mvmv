import codecs
import sqlite3
import re
import sys
from fuzzywuzzy import fuzz

def search(query):
    blacklist = [
        "BluRay",
        "x264",
        "1080p",
        ]


    # Setup the sqlite database
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()
    query = sys.argv[1].replace(".", " ")
    for item in blacklist:
        query = query.replace(item, "")

    m = re.search("(\d{4})", query)
    for match in m.groups():
        if match != "1080":
            return match

    c.execute("SELECT * FROM movies WHERE year=?", [year])

    ratio = 0
    best = ""
    for item in c:
        current = fuzz.ratio(item[0], query)
        if current > ratio:
            ratio = current
            best = item[0]
    return best
