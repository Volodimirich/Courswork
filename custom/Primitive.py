from mininet.topo import Topo

#Creating primitve topology
#   H1       H3
#     \    /
#       Sw
#     /    \
#   H2       H4
class PrimitiveTopo(Topo):

    def __init__(self):
        Topo.__init__(self)

        Host1=self.addHost('h1')
        Host2=self.addHost('h2')
        Host3=self.addHost('h3')
        Host4=self.addHost('h4')
        MainSwitch=self.addSwitch('s1')

        self.addLink(Host1,MainSwitch)
        self.addLink(Host2,MainSwitch)
        self.addLink(Host3,MainSwitch)
        self.addLink(Host4,MainSwitch)

topos = { 'Primitive': ( lambda: PrimitiveTopo() ) }
