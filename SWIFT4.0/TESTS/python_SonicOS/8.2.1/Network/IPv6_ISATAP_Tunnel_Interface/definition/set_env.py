from definition.init_param import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_02_config_interface_x1_ipv6(self):
        logger.info('config interface x1 ipv6...')
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPv6,
            'mgmt_ping': True,
            'gateway':pc3_ipv6_ip,
        }
        rc = interface_ipv6_obj.config_interface_ipv6( **x1_opt )
        Assertion.assert_equal(rc, True, "ERR: config interface x1 ipv6 Failed!")
 
    def test_03_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.0.0',
          
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

        @repeat_method(10)
    def test_04_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


