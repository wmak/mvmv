import sys
import codecs
import re
import sqlite3

def create_table(movie_list, movie_db):
    # Setup the sqlite database
    print("starting")
    conn = sqlite3.connect(movie_db)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS movies")
    print("creating table")
    c.execute("CREATE VIRTUAL TABLE movies USING fts4(name, year)")

    # Open the movies list
    f = codecs.open(movie_list, encoding="utf-8", errors="replace")
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

if __name__ == "__main__":
    create_table(sys.argv[0], sys.argv[1])
