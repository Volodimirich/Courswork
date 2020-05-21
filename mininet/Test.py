from mininet.net import Mininet
from mininet.util import createLink

net = Mininet()

Control = net.addController()

Host1 = net.addHost('h1')
Host2 = net.addHost('h2')
Host3 = net.addHost('h3')
Host4 = net.addHost('h4')

    
MainSwitch=net.addSwitch('s0')

net.addLink(Host1,MainSwitch)
net.addLink(Host2,MainSwitch)
net.addLink(Host3,MainSwitch)
net.addLink(Host4,MainSwitch)

Host1.setIp('192.168.1.1',24)
Host2.setIp('192.168.1.2',24)
Host3.setIp('192.168.1.3',24)
Host4.setIp('192.168.1.4',24)

print('!')
net.start()
print(net.hosts)
for host in net.hosts:
    print('!')
net.pingAll()
net.stop()
