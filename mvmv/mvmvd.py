from daemon import Daemon
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import mvmv
import os
import socket
import sqlite3
import time

class MvmvHandler(FileSystemEventHandler):
    def __init__(self, dest, cursor):
        self.lock = False
        self.dest = dest
        self.cursor = cursor

    def on_modified(self, event):
        if event.is_directory:
            if not self.lock:
                self.lock = True
                print("moving...")
                mvmv.movemovies(event.src_path, self.dest, self.cursor)
                self.lock = False

class mvmvd(Daemon):
    def __init__(self, pidfile, port=4242, destination="", dirs=None):
        # Run the original Daemon code
        Daemon.__init__(self, pidfile)

        # Create and start the observer
        self.observer = Observer()
        self.observer.start()

        # Connect to the movies database
        conn = sqlite3.connect("movies.db")
        self.cursor = conn.cursor()

        # Initialize the variables
        self.dirs = []
        self.monitors = []
        self.dest = destination
        self.port = port

        # watch any directories passed in
        if dirs:
            for path in dirs:
                if path.directory not in self.dirs:
                    self.monitors.append(self.new_monitor(path.directory,
                        path.recursive))
                    self.dirs.append(path.directory)

    def run(self):
        # Listen on port 4242 for any new directories to watch
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", self.port))
        s.listen(5)

        #main execution loop
        while True:
            conn, addr = s.accept()
            data = conn.recv(1024)
            if data:
                opt = data.split(" ")
                message = ""
                if opt[0] == "watch":
                    if opt[-1] not in self.dirs:
                        self.monitors.append(self.new_monitor(opt[-1],
                            "-r" in opt))
                        self.dirs.append(opt[-1])
                        message = "added monitor %s" % opt[-1]
                    else:
                        message = "directory already being monitored"
                conn.sendall(message)
                conn.close()

    def new_monitor(self, path, recursive):
        event_handler = MvmvHandler(self.dest, self.cursor)
        self.observer.schedule(event_handler, path, recursive=recursive)
        return event_handler

if __name__ == "__main__":
    mv = mvmvd("./mvmvd.pid")
    mv.run()
