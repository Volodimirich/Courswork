from mininet.net import Mininet
import subprocess
import copy
import threading
import random
import sys
import time
from mininet.node import OVSController

stop=threading.Event()

def graphnet(key1, key2, graph: dict) -> None:
    """This function creating matrix of incidence"""
    graph[key1].append(key2)
    graph[key2].append(key1)

def dijkstra_path(start, end, graph: dict):
    """This function founding path from start to end in graph"""
    weight = {}
    tops = set()
    neighbors = list()
    total_top = start
    pos = 0
    for elem in graph:
        if elem == start:
            weight.update({start: [0, []]})
        else:
            weight.update({elem: [len(graph) ** 3, []]})  # Just now without weight
    while len(tops) != len(graph):
        tops.add(total_top)
        for top in graph[total_top]:
            if top not in tops:
                neighbors.append(top)
                if weight[top][0] > weight[total_top][0] + 1:
                    res = copy.deepcopy(weight[total_top])
                    weight.update({top: [weight[total_top][0] + 1, res[1]]})
                    weight[top][1].append(total_top)
        if pos >= len(neighbors):
            break
        total_top = neighbors[pos]
        pos += 1
    return weight[end][1][1:]

#To begin execution of predefined functions
def prescript(type, sem, seting, host):
    if type == "Server":
        print(host.cmd("iperf -s -u -i 10 -t 20"))
    elif type == "Client":
        stop.set()
        print(host.cmd("iperf -c 10.0.0.3 -u -b  10m -t 20"))
    elif type == "S0":
        if (sem):
            stop.wait()
            stop.wait()
            stop.clear()
            stop.wait(seting-time.clock())
            subprocess.run("ovs-ofctl add-flow s0 in_port=2,actions=output:4", shell=True, executable='/bin/bash')
            stop.set()
            print(stop.is_set())

    elif type == "S1":
        if (sem):
            stop.wait()
            stop.clear()
            stop.wait(seting-time.clock())
            stop.clear()
            subprocess.run("ovs-ofctl add-flow s1 in_port=4,actions=output:2",shell=True, executable='/bin/bash')
            stop.set()

if __name__ == "__main__":        
    net = Mininet(controller = OVSController, cleanup = True)
    Control = net.addController()
    graph_tree = {}

    host1 = net.addHost('h1')
    graph_tree.update({host1.name: []})     #Mutate addHost function for this
    host2 = net.addHost('h2')
    graph_tree.update({host2.name: []})     
    host3 = net.addHost('h3')
    graph_tree.update({host3.name: []})     
    host4 = net.addHost('h4')
    graph_tree.update({host4.name: []})
    switch1=net.addSwitch('s0')
    graph_tree.update({switch1.name: []})
    switch2=net.addSwitch('s1')
    graph_tree.update({switch2.name: []})
    net.addLink(host1, switch1, 1, 1)
    graphnet(host1.name, switch1.name, graph_tree)
    net.addLink(host3, switch2, 3, 3)
    graphnet(host3.name, switch2.name, graph_tree)
    net.addLink(host2, switch1, 2, 2)
    graphnet(host2.name, switch1.name, graph_tree)
    net.addLink(host4, switch2, 2, 2)
    graphnet(host4.name, switch2.name, graph_tree)
    net.addLink(switch1, switch2, 4, 4)
    graphnet(switch1.name, switch2.name, graph_tree)
    net.build()      #Build network

    Way1 = set(dijkstra_path('h2', 'h3', graph_tree))  #Used vertexes were found
    Way2 = {'s0'}  #Used vertexes were found
    Way3 = {'s1'}
    sem = True if (Way1 & Way2) or (Way1 & Way3) else False
    # Get two random time
    delay =  [random.triangular(5,20,random.normalvariate(20,6)), random.triangular(5,20,random.normalvariate(20,6))]
    delay.sort()
    print("Delay")
    print(delay)

    net.start()


    thread1 = threading.Thread(target=prescript, args=("Server", sem, None, host3))
    thread2 = threading.Thread(target=prescript, args=("Client", sem, None, host2))
    thread3 = threading.Thread(target=prescript, args=("S1", sem, delay[0], None))
    thread4 = threading.Thread(target=prescript, args=("S0", sem, delay[1]-delay[0], None))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    net.stop()
