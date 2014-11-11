#!/usr/bin/env python
import sys
import sqlite3
import mvmv

movies_db = "var/movies.db"
queries = sys.argv[1:]

if __name__ == '__main__':
    conn = sqlite3.connect(movies_db)
    cursor = conn.cursor()

    for query in queries:
        print(mvmv.search(query, cursor))

    conn.close()
