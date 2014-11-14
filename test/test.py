import csv
import mvmv
import sqlite3
import time

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

count = 0
length = 0
start = time.time()

with open("test.csv", "rb") as csvfile:
    testfile = csv.reader(csvfile)
    for row in testfile:
        length += 1
        result = mvmv.search(row[0], cursor)
        if result != row[1][1:]:
            count += 1
            print("source: %s" % row[0])
            print("actual: %s" % row[1][1:])
            print("result: %s\n" % result)

print("AvgT: %f" % ((time.time() - start)/float(length)))
print("Fails: %d" % count)
print("Pass: %d%%" % (100*float(length - count)/float(length)))

conn.close()
