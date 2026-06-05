from definition.init_param import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = 'setup router and http ftp server'
    goto_teardown = True

     
    def test_01_config_interface_x1(self):
        logger.info('config interface x1...')
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    @repeat_method(3)
    def test_02_register_fw(self):
        logger.info('config interface to dhcp...')
        rc = licenseObj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
