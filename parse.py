import codecs
import sqlite3
import re

# Setup the sqlite database
print("starting")
conn = sqlite3.connect("movies.db")
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS movies")
print("creating table")
c.execute("CREATE VIRTUAL TABLE movies USING fts4(name, year)")

# Open the movies list
f = codecs.open("movies.list", encoding="utf-8", errors="ignore")
lines = f.readlines()[15:-1] # skip the header

print("Starting insertion into datbase")
# Read and insert movies into the database
for line in lines:
    m = re.search("\"(.*?)\" \((.*?)\)", line)
    try:
        name = m.group(1)
        year = m.group(2)
    except Exception as e:
        try:
            m = re.search("(.*?) \((.*?)\)", line)
            name = m.group(1)
            year = m.group(2)
        except Exception as e:
            print("okay wow failed on both regex:\n%s" % line)
    c.execute("INSERT INTO movies VALUES (?, ?)", (name, year))

# Commit and close the database
conn.commit()
conn.close()
