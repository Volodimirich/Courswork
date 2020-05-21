from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.node import OVSController

Linear = LinearTopo(k=4)
net = Mininet(topo=Linear,controller = OVSController)

net.start()
net.pingAll()
net.stop()
