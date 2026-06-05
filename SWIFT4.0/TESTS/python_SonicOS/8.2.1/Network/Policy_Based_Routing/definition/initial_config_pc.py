from definition.initial_parameter import *


class TestConfigPC(Test):
    uuid = 'NonTC'
    def test_00_01_set_pc1_route_ipv4(self):
        logger.info('Seting route on PC1 via gw {}'.format(Parameter.FIREWALL))
        rc = os.system('route add -net 10.0.0.0 netmask 255.0.0.0 gw 172.18.1.1')
        rc = os.system('ip -4 r del default')
        rc = os.system('ip -4 r add default via ' + Parameter.FIREWALL)
        rc = os.system('route add -net 172.17.1.0 netmask 255.255.255.0 gw ' + Parameter.FIREWALL)
        rc = os.system('route add -net 172.20.1.0 netmask 255.255.255.0 gw ' + Parameter.FIREWALL)
        rc = os.system('route del -net 192.168.168.0 netmask ' + Parameter.MASK)
        rc = os.system('route add -net 192.168.168.168 netmask 255.255.255.255 gw ' + PC1_ETH1_IP)
        rc = os.system('ifconfig eth2 down')
        result = os.popen('ip -4 r').read()
        logger.info(result)
        Assertion.assert_regular(result, 'default via 192.168.168.168', "ERR: Set route IPv4 on PC1 failed")

    def test_00_02_set_pc3_route_ipv4(self):
        logger.info('Seting route on PC3 via gw {}'.format(Parameter.FIREWALL))
        PC3_login.send_command( "route add -net 10.0.0.0 netmask 255.0.0.0 gw 172.18.1.1")
        PC3_login.send_command( "ip -4 r del default")
        PC3_login.send_command( "ip -4 r add default via " + Parameter.FIREWALL )
        PC3_login.send_command( "route add -net 10.0.0.0 netmask 255.0.0.0 gw 172.18.1.1")
        PC3_login.send_command( "route add -net 172.20.1.0 netmask 255.255.255.0 gw " + Parameter.FIREWALL)
        PC3_login.send_command( "route add -net 172.30.1.0 netmask 255.255.255.0 gw " + Parameter.FIREWALL)
        result = os.popen('ip -4 r').read()
        logger.info(result)
        Assertion.assert_regular(result, 'default via 192.168.168.168', "ERR: Set route IPv4 on PC4 failed")