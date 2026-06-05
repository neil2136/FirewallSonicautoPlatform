from definition.settings import *

from lib.modules.CLI.system import LicenseCli
fw_cli = Firewall("192.168.168.168", user='admin', password='password', supported_config_mode='cli-ssh')
license_obj = LicenseCli(fw_cli)


class TestInitConfig(Test):
    uuid = 'NonTC'
   
    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': MASK,
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x1_static)
        rc &= license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
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

    def test_03_Config_X3(self):
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
