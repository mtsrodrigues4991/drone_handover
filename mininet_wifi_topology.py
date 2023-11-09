
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', range='20')
    ap1 = net.addAccessPoint('ap1', ssid='ap-ssid1', mode='g', channel='1', position='50,50,0', range='30')
    ap2 = net.addAccessPoint('ap2', ssid='ap-ssid2', mode='g', channel='6', position='90,50,0', range='30')
    c0 = net.addController('c0')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(ap1, sta1)
    net.addLink(ap2, sta1)

    print "*** Starting network"
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    print "*** Addressing..."
    sta1.cmd('ifconfig sta1-wlan0 10.0.0.1/8')

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
