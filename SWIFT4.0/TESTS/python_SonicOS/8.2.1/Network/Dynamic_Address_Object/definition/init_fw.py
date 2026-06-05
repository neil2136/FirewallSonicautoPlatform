from definition.settings import *


class TestInitConfig(Test):
    uuid = 'NonTC'
    def test_01_config_interface(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': X1_IP,
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_get_PC1_eth0_mac(self):
        ret = False
        '''
            [root@VTB531-PC2 ~]# ifconfig eth0|grep HWaddr|awk '{print $5}'
                 FA:16:3E:3C:69:6A
            [root@VTB531-PC2 ~]# ifconfig eth0|grep HWaddr
                 eth0      Link encap:Ethernet  HWaddr FA:16:3E:3C:69:6A
        '''
        Parameter.PC1_ETH0_MAC = os.popen("ifconfig eth0|grep HWaddr|awk '{print $5}'").read()
        Parameter.PC1_ETH0_MAC = Parameter.PC1_ETH0_MAC.replace('\n', '')
        logger.info(Parameter.PC1_ETH0_MAC)
        b = Parameter.PC1_ETH0_MAC.split(':')
        Parameter.PC1_ETH0_MAC = ''.join(b)
        logger.info(Parameter.PC1_ETH0_MAC)
        if len(Parameter.PC1_ETH0_MAC) == 12:
            ret = True
        Assertion.assert_equal(ret, True, "ERR: Get PC1 eth0 mac failed")
