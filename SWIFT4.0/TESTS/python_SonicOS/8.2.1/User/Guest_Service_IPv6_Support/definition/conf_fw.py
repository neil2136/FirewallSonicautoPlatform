from definition.initial_parameter import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"

    def test_00_00_config_x0_interface(self):
        X0_IPv6_Interface = {
            'name': 'X0',
            'mode': 'static',
            'zone':'LAN',
            "ip": Parameter.X0_IPv6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc = interface_ipv6.config_interface_ipv6(**X0_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv4 failed")

    def test_00_01_config_x1_interface(self):
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
            'mgmt_https': False,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = interface_ipv4.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")
    
    @repeat_method(10)
    def test_00_02_register_fw(self):
        # add X1 route for PC1 at first
        logger.info('register fw..')
        rc = licenseObj.register('online')
        Assertion.assert_equal(rc, True, 'ERR: Register fw failed')

    def test_00_03_config_x1_interface(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            # 'gateway': Parameter.X1_GW,
            # 'dns1': Parameter.X1_DNS_1,
            # 'dns2': Parameter.X1_DNS_2,
            'mgmt_https': False,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = interface_ipv4.config_interface(**x1)
        X1_IPv6_Interface = {
            'name': 'X1',
            'mode': 'static',
            'zone':'WAN',
            "ip": Parameter.X1_IPv6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc &= interface_ipv6.config_interface_ipv6(**X1_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_00_04_config_x2_interface(self):
        #setup X2 which connect to linux http server
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            # 'gateway': Parameter.X1_GW,
            # 'dns1': Parameter.X1_DNS_1,
            # 'dns2': Parameter.X1_DNS_2,
            'mgmt_https': False,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = interface_ipv4.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")
        X2_IPv6_Interface = {
            'name': 'X2',
            'mode': 'static',
            'zone':'WAN',
            "ip": Parameter.X2_IPv6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc &= interface_ipv6.config_interface_ipv6(**X2_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_00_05_add_guest_user(self):
        guest_user = {
            'action': 'add',
            'accountname': 'guest',
            'password': 'password',
            # 'activate_on_login': True,
            # 'enable_guest_service_privilege': True,
            # 'login_uniqueness': False,
            #'account_lifetime': False,
            #'acco_lifetime': 2,
            #'acco_lifetype': 'days',
            # 'prune_on_expiry': True,
            # 'comment': 'Newadd',
            # 'quota_cycle': 'day',
            # 'session_lifetime': True,
            # 'sess_lifetime': 1,
            # 'sess_lifetype': 'days',
        }
        rc = guest_obj.user_guest_account(**guest_user)
        Assertion.assert_equal(rc, True, "ERR: create guest user failed")

    def test_00_06_add_customer_zone(self):
        customer_zone = {
            "zones": [
                {
                    "name": "customer",
                    "security_type": "trusted"
                }
            ]
        }
        rc = zone_obj.add_zone_object(**customer_zone)
        Assertion.assert_equal(rc, True, "ERR: add customer zone failed")

    def test_00_07_add_dhcpv6_dynamic_scope(self):
        dhcp_server_ipv6_scope = {
            "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "scope_ipv6",
                                "enable": True,
                                "prefix": "2003:db93::",
                                "range": {
                                    "from": "2003:db93::200",
                                    "to": "2003:db93::205"
                                }
                            }
                        ]
                    }
                }
            }
        }

        rc = dhcp_server_obj.add_dhcp_server_scope_dynamic(**dhcp_server_ipv6_scope)
        Assertion.assert_equal(rc, True, "ERR: failed to add dhcpv6 dynamic scope")

    def test_00_08_Add_default_Route_for_PC1(self):
        cmd = 'route -A inet6 del default gw ' + Parameter.LAN_PC_IPv6_GW
        localhost.send_command(cmd)
        cmd = 'route -A inet6 add default gw ' + Parameter.X0_IPv6
        localhost.send_command(cmd)
        out = localhost.send_command("ip -6 route show")
        Assertion.assert_regular(out, r'default via 2001:db0', "ERR: add route for lanpc pc1 failed")

    def test_00_09_Add_default_Route_for_PC2(self):
        cmd = 'route -A inet6 del default gw ' + Parameter.LINUX_SERVER_IPv6_GW
        http_server.send_command(cmd)
        cmd = 'route -A inet6 add default gw ' + Parameter.X2_IPv6
        http_server.send_command(cmd)
        out = http_server.send_command("ip -6 route show")
        Assertion.assert_regular(out, 'default via 2001:db1', "ERR: add route for linux server failed")

    def test_00_10_Add_default_Route_for_PC3(self):
        Customer_PC = Host(Params.testbed+'-PC3')
        cmd = 'route -A inet6 del default gw ' + Parameter.static_PC_IPv6_GW
        Customer_PC.send_command(cmd)
        cmd = 'route -A inet6 add default gw ' + Parameter.X3_IPv6
        Customer_PC.send_command(cmd)
        out = Customer_PC.send_command("ip -6 route show")
        Assertion.assert_regular(out,'default via 2001:1100', "ERR: Config X1 IPv4 failed")


