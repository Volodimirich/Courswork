from mininet.net import Mininet
import datetime
import subprocess
import time
import copy

import sys
import threading 
from mininet.node import OVSController

lock = threading.Lock()

#This function creating matrix of incidence
def graphnet(key1,key2,graph:dict) -> None:
    graph[key1].append(key2)
    graph[key2].append(key1)

#This function founding path from start to end in graph
def dijkstra_path(start, end, graph: dict):
    Weight = {}
    Tops = set()
    Neighbors = list()
    TotalTop = start
    pos = 0
    for elem in graph:
        if elem == start:
            Weight.update({start: [0, []]})
        else:
            Weight.update({elem: [len(graph) ** 3, []]})  # Just now without weight
    while len(Tops) != len(graph):
        Tops.add(TotalTop)
        for top in graph[TotalTop]:
            if top not in Tops:
                Neighbors.append(top)
                if Weight[top][0] > Weight[TotalTop][0] + 1:
                    res = copy.deepcopy(Weight[TotalTop])
                    Weight.update({top: [Weight[TotalTop][0] + 1, res[1]]})
                    Weight[top][1].append(TotalTop)
        if (pos >= len(Neighbors)):
            break
        TotalTop = Neighbors[pos]
        pos += 1
    return Weight[end][1][1:]
            

#To begin execution of predefined functions
def prescript(type,sem:bool, host1,host2) -> None:
    #if sem:
        #lock = threading.Lock()
        #lock.acquire()
    if type=="Server":
        print(host2.cmd("iperf -s -u -i 0.2 -t 20"))
    elif type=="Client":
        time.sleep(0.1)
        print(host1.cmd("iperf -c 10.0.0.3 -u -b  10m -t 20"))
    else:
        time.sleep(int(type))
        subprocess.run("ovs-ofctl add-flow s1 in_port=4,actions=output:2",shell=True, executable='/bin/bash')
    #if sem:
        #lock.release()


if __name__ == "__main__":        
    net = Mininet(controller = OVSController,cleanup = True)
    Control = net.addController()
    GraphTree={}

    Host1 = net.addHost('h1')
    GraphTree.update({Host1.name:[]})                   #Mutate addHost function for this
    Host2 = net.addHost('h2')
    GraphTree.update({Host2.name:[]})
    Host3 = net.addHost('h3')
    GraphTree.update({Host3.name:[]})
    Host4 = net.addHost('h4')
    GraphTree.update({Host4.name:[]})     #To do, make it better
    Switch1=net.addSwitch('s0')
    GraphTree.update({Switch1.name:[]}) 
    Switch2=net.addSwitch('s1')
    GraphTree.update({Switch2.name:[]}) 
    net.addLink(Host1,Switch1,1,1)
    graphnet(Host1.name,Switch1.name,GraphTree)
    net.addLink(Host3,Switch2,3,3)
    graphnet(Host3.name,Switch2.name,GraphTree)
    net.addLink(Host2,Switch1,2,2)
    graphnet(Host2.name,Switch1.name,GraphTree)
    net.addLink(Host4,Switch2,2,2)
    graphnet(Host4.name,Switch2.name,GraphTree)
    net.addLink(Switch1,Switch2,4,4)
    graphnet(Switch1.name,Switch2.name,GraphTree)
    net.build()      #Build network

    Way1 = set(dijkstra_path('h2','h3',GraphTree))  #Used vertexes were found
    Way2 = set(dijkstra_path('h1','h4',GraphTree))  #Used vertexes were found
    Semaf = True if Way1 & Way2 else False  #If there is an intersection, enable blocking mode

    # print(Semaf,Way1,Way2,dijkstra_path('h2','h3',GraphTree))

    net.start()
    thread1 = threading.Thread(target=prescript, args=("Server",Semaf,Host2,Host3))
    thread2 = threading.Thread(target=prescript, args=("Client",Semaf,Host2,Host3))
    thread3 = threading.Thread(target=prescript, args=(float(sys.argv[1]),Semaf,Host2,Host3))
    lock = threading.Lock()

    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()

    net.stop()

