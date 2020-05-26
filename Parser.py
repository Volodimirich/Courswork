import sys

if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    NextOut=False
    Counter =0
    for line in f:
        if line == "Delay\n":
            NextOut=True
        elif line == "[ ID] Interval       Transfer     Bandwidth        Jitter   Lost/Total Datagrams\n":
            Counter=4
        elif NextOut:
            print(line,end='');
            NextOut=False
        elif Counter!=0:
            Counter-=1
            print(line,end='');
        else:
            NextOut=False
