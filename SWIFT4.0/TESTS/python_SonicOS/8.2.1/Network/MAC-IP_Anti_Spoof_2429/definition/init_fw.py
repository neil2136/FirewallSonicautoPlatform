from definition.settings import *


class TestInitConfig(Test):
    uuid = 'NonTC'

    def test_00_Config_X1_and_Register(self):
        x1_gw = '111.111.111.1'
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': '255.255.255.0',
            'gateway': x1_gw,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
        }
        rc = interface_obj.config_interface(**x1_static)
        rc &= lc_obj.register(mode='online')
        Assertion.assert_equal(rc, True, "=====> ERR: Configure X1 failed!")

    def test_01_Config_X2(self):
        logger.info("config x2 interface... ")
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_02_Config_X3(self):
        logger.info("config x3 interface... ")
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': X3_IP,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_03_get_PC2_eth0_mac(self):
        ret = False
        Parameter.PC2_ETH0_MAC = PC2_login.send_command("ifconfig eth0|grep HWaddr|awk '{print $5}'")
        Parameter.PC2_ETH0_MAC = Parameter.PC2_ETH0_MAC.replace('\n', '')
        #match = re.search("b'(.*)'", Parameter.PC2_ETH0_MAC)
        #if match:
        #    Parameter.PC2_ETH0_MAC = match.group(1).replace('\n', '')
        #    logger.info(Parameter.PC2_ETH0_MAC)
        b = Parameter.PC2_ETH0_MAC.split(':')
        Parameter.PC2_ETH0_MAC = ''.join(b)
        logger.info(Parameter.PC2_ETH0_MAC)
        if len(Parameter.PC2_ETH0_MAC) == 12:
            ret = True
        Assertion.assert_equal(ret, True, "ERR: Get PC2 eth0 mac failed")