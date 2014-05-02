from mininet.topo import Topo
from mininet.net import Mininet
# from mininet.link import TCLink
# from mininet.util import custom

class BasicTopo(Topo):
    "Very basic Mininet topology with a single host and switch"

    def __init__(self, **params):
      
        # Initialize topology
        Topo.__init__(self, **params)

        # Host configuration
        hostConfig = {'cpu': 0.5}

        # Hosts and switches
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', **hostConfig)

        # Wire the host to the switch
        self.addLink(h1, s1)
