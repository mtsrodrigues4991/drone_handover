from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP, OVSKernelSwitch, Controller
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():
    # Cria a rede Mininet
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink, accessPoint=OVSKernelAP)

    # Adiciona controlador
    c0 = net.addController('c0')

    # Cria os nós do AP (antenas)
    ap1 = net.addAccessPoint('ap1', ssid="ssid_ap1", mode="g", channel="1")
    ap2 = net.addAccessPoint('ap2', ssid="ssid_ap2", mode="g", channel="6")

    # Cria um nó móvel (drone)
    sta1 = net.addStation('sta1', ip="192.168.0.1/24")

    # Conecta o AP1 e AP2 ao controlador
    net.addLink(ap1, c0)
    net.addLink(ap2, c0)

    # Conecta o drone ao AP1
    net.addLink(sta1, ap1)

    # Inicializa a rede
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    # Define os controladores dos rádios (usando o controlador Ryu)
    ap1.cmd("dpctl unix:/tmp/ap1 mgmt openflow.sta1")
    ap2.cmd("dpctl unix:/tmp/ap2 mgmt openflow.sta1")

    # Inicializa o controlador Ryu
    ap1.cmd("ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest --ofp-tcp-listen-port 6634")
    ap2.cmd("ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest --ofp-tcp-listen-port 6635")

    # Inicializa o CLI
    setLogLevel('info')
    net.start()

    # Agora você pode interagir com a topologia no CLI do Mininet

    # Execute o Mininet CLI
    CLI(net)

    # Quando terminar, pare a rede
    net.stop()

if __name__ == '__main__':
    topology()
