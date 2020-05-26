import subprocess
import sys

if __name__ == "__main__":
    for i in range (int(sys.argv[1])):
        subprocess.run(f"python3 Locks.py >> Result.txt", shell=True)
        subprocess.run("mn -c", shell=True)
