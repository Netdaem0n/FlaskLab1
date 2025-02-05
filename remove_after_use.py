import os
from time import sleep
import sys


def remove_file(filename, timetl):
    sleep(timetl)
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File {filename} deleted.")
    else:
        print(f"File {filename} does not exist.")

remove_file(sys.argv[1], int(sys.argv[2]))

