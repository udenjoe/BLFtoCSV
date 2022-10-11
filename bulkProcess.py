import sys
import glob
import os

directory_name = ""
files = []
try:
    directory_name=sys.argv[1]
    config = sys.argv[2]
    print(directory_name)
    files = glob.glob(directory_name + "/*.blf")
    print(files)
    for file in files:
        os.system("python3 blftocsv.py " + file + " " + config)
except Exception as e: print(e)