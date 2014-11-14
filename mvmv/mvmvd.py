from daemon import Daemon
from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.modified = False

    def on_modified(self, event):
        self.modified = True

class mvmv(Daemon):
    def run(self):
        self.observer = Observer()
        self.monitors = [self.new_monitor(".", True)]
        self.observer.start()
        while True:
            while not all([mon.modified for mon in self.monitors]):
                time.sleep(1)
            for mon in self.monitors:
                mon.modified = False
                print("modified") # Change to the move function

    def new_monitor(self, path, recursive):
        event_handler = MyHandler()
        self.observer.schedule(event_handler, path, recursive=recursive)
        return event_handler

if __name__ == "__main__":
    mv = mvmv("./mvmvd.pid")
    mv.start()
