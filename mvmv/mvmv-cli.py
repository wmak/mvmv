#!/usr/bin/env python
from os import path
import sys
import sqlite3
import mvmv
import random
import argparse
import re


def get_db_loc():
    dbs = ['a', 'b', 'c']
    return random.choice(dbs)


def get_parser():
    usage_str = "%(prog)s [OPTIONS] [-r] [-w] [-d] DIRECTORY [DIRECTORY ...]"
    parser = argparse.ArgumentParser(usage=usage_str)

    parser.add_argument("-f", "--file", dest="filename", metavar="FILE",
                        type=str, nargs='*', default=[],
                        help="Rename this FILE")

    parser.add_argument("-d", "--dir", dest="dirname", metavar="DIR",
                        type=str, nargs='*', default=[],
                        help="Rename all files in this DIRECTORY")

    # FIXME(pbhandari): doesn't work properly
    parser.add_argument("-e", "--excludes", dest="excludes", metavar="REGEX",
                        type=str, nargs='*', default=[],
                        help="Rename all files in this DIRECTORY")

    parser.add_argument("-r", "-R", "--recursive", action="store_true",
                        dest="recursive", default=False,
                        help="Recursively scan the directories for files.",)

    parser.add_argument("-m", "--max-depth", dest="depth", metavar="DEPTH",
                        default=None, type=int, nargs='?',
                        help="Recursively scan the directories for files.",)

    parser.add_argument("-g", "--gui", action="store_true", dest="start_gui",
                        default=False,
                        help="Start the program as a GUI.")
    parser.add_argument("-w", "--watch", action="store_true", dest="watch",
                        default=False,
                        help="Watch the given directories for new files")

    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                        default=False,
                        help="Be more verbose.")
    parser.add_argument("-q", "--quiet", dest="quiet", action="store_true",
                        default=False,
                        help="Only output errors.")

    parser.add_argument("-y", "--always-yes", dest="always_yes",
                        action="store_true", default=False,
                        help="Assume yes for every prompt")

    parser.add_argument("-u", "--updatedb", dest="remotedb", default=None,
                        metavar="PATH", type=str, nargs='?',
                        help="Update the movies list from the given DBPATH.")

    # TODO(pbhandari): default db path should be sane.
    parser.add_argument("-p", "--dbpath", dest="dbpath", nargs='?',
                         metavar="PATH", type=str, default="movies.db",
                        help="Alternate path for the database of movies.")

    parser.add_argument('args', nargs=argparse.REMAINDER)
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()

    conn = sqlite3.connect(args.dbpath)
    cursor = conn.cursor()
    args.excludes = [re.compile(a) for a in args.excludes]

    # TODO(pbhandari): Code is ugly and stupid
    renames = []
    for query in args.args + args.filename + args.dirname:
        movies = []
        if path.isdir(query):
            movies = mvmv.get_movies_list(path.abspath(query), args.excludes)
        elif mvmv.is_valid_file(query, args.excludes):
            movies = [(path.dirname(path.abspath(query)), path.basename(query))]

        renames += [(m[0], m[1], mvmv.search(m[1], cursor)) for m in movies]

    print(renames)

    conn.close()
