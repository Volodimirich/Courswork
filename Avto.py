import subprocess
import sys


time = float(21)
delay = float(sys.argv[1])
limit = float(sys.argv[2])
while time > limit:
    subprocess.run(f"echo Tested delayed time is - {time} >> Result.txt\n",shell=True)
    subprocess.run(f"python3 Test.py {time} >> Result.txt", shell=True)
    subprocess.run("mn -c", shell=True)
    time -= delay
