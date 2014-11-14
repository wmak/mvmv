from daemon import Daemon
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import socket
import time

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("modified") # mv code here

class mvmv(Daemon):
    def run(self):
        self.observer = Observer()
        self.monitors = []
        self.dirs = []
        self.observer.start()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 4242))
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
        event_handler = MyHandler()
        self.observer.schedule(event_handler, path, recursive=recursive)
        return event_handler

if __name__ == "__main__":
    mv = mvmv("./mvmvd.pid")
    mv.start()
