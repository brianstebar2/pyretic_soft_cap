from mininet.cli import CLI
from mininet.log import lg, info, setLogLevel
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.util import irange, custom, quietRun, dumpNetConnections

from topology import BasicTopo
from mininet_nat import *

def main():
    "Create a soft capped network and give a CLI to it"

    # Create the Mininet topology with a remote controller
    topo = BasicTopo()
    net = Mininet(topo=topo, controller=None)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Set up the NAT to connect it to the internet
    rootnode = connectToInternet(net)

    # Open CLI for NAT'ed small network
    CLI(net)

    # Clean up
    stopNAT(rootnode)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()
