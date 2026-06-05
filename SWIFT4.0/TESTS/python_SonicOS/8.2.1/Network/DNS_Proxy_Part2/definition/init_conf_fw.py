from definition.settings import *

class TestInit_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True
    description = 'initialize firewall'

    def test_00_config_x0(self):
        logger.info("config x0 ipv6 interface ... ")
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interface_v6_api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(rc1, True, "ERR: Config X0 to static failed")

    def test_01_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interface_api.config_interface(**x1_static)
        rc2 = interface_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X1 to static failed")

    @repeat_method(2)
    def test_02_Register_fw(self):
        time.sleep(20)
        rc = license_cli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_interface_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'gateway': Parameter.X2_GW,
            'dns1': Parameter.X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X2_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interface_api.config_interface(**x2_static)
        rc2 = interface_v6_api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 to static failed")

    def test_04_config_interface_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x3_v6_dict = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': Parameter.X3_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interface_api.config_interface(**x3_static)
        rc2 = interface_v6_api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X3 to static failed")

    def test_05_disable_dns_proxy_cache(self):
        disCache = {
            'dns_cache': False,
            'enforce_all_dns_requests': False
        }
        rc = dns_proxy_api.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: Disable DNS Proxy Cache failed")

