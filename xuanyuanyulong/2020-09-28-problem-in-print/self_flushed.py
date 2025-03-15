import threading
import time


def print_sharp():
    while True:
        time.sleep(0.5)
        print("#", end="", flush=True)


t1 = threading.Thread(target=print_sharp)
t1.setDaemon(True)
t1.start()

time.sleep(5)
