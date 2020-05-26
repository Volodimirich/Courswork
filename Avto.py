import subprocess
import sys


for i in range (60):
    subprocess.run(f"python3 Locks.py >> Result.txt", shell=True)
    subprocess.run("mn -c", shell=True)
