from mininet.net import Mininet
import subprocess
import time
import copy
import threading 
from mininet.node import OVSController



def graphnet(key1, key2, graph: dict) -> None:
    """This function creating matrix of incidence"""
    graph[key1].append(key2)
    graph[key2].append(key1)

def update_topo(graph: dict, labels: dict, value) -> None:
    """This function update topo information"""
    graph.update({value: []})
    labels.update({value: 0})

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
def prescript(type, sem, host):
    if type == "Server":
        print(host.cmd("iperf -s -u -i 0.2 -t 20"))
    elif type == "Client":
        print(host.cmd("iperf -c 10.0.0.3 -u -b  10m -t 20"))
    else:
        if sem:
            print("delayed time is - ", type)
            threading.Event().wait(type)
            subprocess.run("ovs-ofctl add-flow s1 in_port=4,actions=output:2",shell=True, executable='/bin/bash')

def timeset(way, labels, time_exp):
    time_total = time.clock()
    delay_max, delay_time = 0, 0
    for top in way:
        delay_time = labels[top] - time_total
        delay_max = delay_time if delay_time > delay_max else delay_max
    if delay_max == 0:
        for top in way:
            labels[top] = time_total + time_exp
    return delay_max

if __name__ == "__main__":        
    net = Mininet(controller = OVSController, cleanup = True)
    Control = net.addController()
    graph_tree = {}
    time_labels = {}

    host1 = net.addHost('h1')
    update_topo(graph_tree, time_labels, host1.name)                #Mutate addHost function for this
    host2 = net.addHost('h2')
    update_topo(graph_tree, time_labels, host2.name)
    host3 = net.addHost('h3')
    update_topo(graph_tree, time_labels, host3.name)
    host4 = net.addHost('h4')
    update_topo(graph_tree, time_labels, host4.name)
    switch1=net.addSwitch('s0')
    update_topo(graph_tree, time_labels, switch1.name)
    switch2=net.addSwitch('s1')
    update_topo(graph_tree, time_labels, switch2.name)
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
    Way2 = {'s1'}  #Used vertexes were found



    net.start()

    time.clock()
    delay_way1 = timeset(Way1, time_labels, 20) #TODO make some predictions about time
    delay_way2 = timeset(Way2, time_labels, 1)
    sem = True if (delay_way1 + delay_way2) != 0 else False

    print(delay_way2)

    thread1 = threading.Thread(target=prescript, args=("Server", sem, host3))
    thread2 = threading.Thread(target=prescript, args=("Client", sem, host2))
    thread3 = threading.Thread(target=prescript, args=(delay_way2, sem, None))

    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()

    net.stop()