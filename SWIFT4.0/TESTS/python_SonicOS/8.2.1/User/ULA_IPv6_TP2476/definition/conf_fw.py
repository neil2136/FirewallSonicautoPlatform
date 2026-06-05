from definition.settings import *


class TestConfigFw(Test):
    uuid = 'NonTC'

    def test_00_00_config_x0_interface(self):
        X0_IPv6_Interface = {
            'name': 'X0',
            'mode': 'static',
            'zone':'LAN',
            "ip": Parameter.X0_IPV6,
            "prefix_length": 64,
            'mgmt_https': True,
            'user_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc = interface_ipv6.config_interface_ipv6(**X0_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv6 failed")


    def test_00_01_config_x1_interface(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'dns3': Parameter.X1_DNS3,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = interface_ipv4.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")
        X1_IPv6_Interface = {
            'name': 'X1',
            'mode': 'static',
            'zone':'WAN',
            "ip": Parameter.X1_IPV6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': False,
            'mgmt_ssh': False,
            'mgmt_snmp': False,
        }
        rc = interface_ipv6.config_interface_ipv6(**X1_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv6 failed")
    
    def test_00_02_config_x2_interface(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_ipv4.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")
        x2_IPv6_Interface = {
            'name': 'X2',
            'mode': 'static',
            'zone':'DMZ',
            "ip": Parameter.X2_IPV6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': False,
            'user_https': True,
        }
        rc = interface_ipv6.config_interface_ipv6(**x2_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv6 failed")
    
    def test_00_03_add_customized_zone(self):
        cuz_dict = {
            "zones": [
                {
                "name": "cuz_zone",
                "security_type": "public",
                }
            ]
        }
        add_zone = zone_api.add_zone_object(**cuz_dict)
        Assertion.assert_equal(add_zone,True,"Err: Failed to add zone.")
    
    def test_00_04_config_x3_interface(self):
        logger.info("config x3 interface... ")
        x3 = {
            'if': 'X3',
            'zone': 'cuz_zone',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_ipv4.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")
        x3_IPv6_Interface = {
            'name': 'X3',
            'mode': 'static',
            'zone':'cuz_zone',
            "ip": Parameter.X3_IPV6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': False,
            'user_https': True,
        }
        rc = interface_ipv6.config_interface_ipv6(**x3_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 failed")

    @repeat_method(3)
    def test_00_05_Register(self):
        time.sleep(10)
        rc = license.register('online')
        Assertion.assert_equal(rc, True, "ERR: Register failed")
        

