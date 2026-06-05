from definition.settings import *


class Test_Config_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_fw_x1(self):
        x1_opt = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': "12.12.0.1",
            'dns1': Parameter.X1_DNS_1,
            'dns2': Parameter.X2_DNS_2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        rc = iface_v4_api.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed')

    def test_02_register_fw(self):
        for i in range(10):
            time.sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_restore_remote_fw(self):
        logger.info('=> restore remote FW and enable API')
        remote_conf_path = os.environ['PYTHON_COMMON_HOME'] + '/config/restore_gw_rmt_tel.py'
        cmd1 = f'python3 {remote_conf_path} ' \
            f'-os=1 --testbed={Params.testbed} ' \
            f'-device=RemoteGEN7 -if=x1 -zone=WAN ' \
            f'-ip=12.12.1.201 -restore=1'
        pc1_login.send_command(cmd1)
        logger.info('=> check if remote X3 is reachable')
        res = pc1_login.ping(f'{Parameter.REM_X1_IP}')
        logger.info(f'ping remote firewall x1 result: {res}')
        Assertion.assert_equal(res, True, 'ERR: config remote FW failed')

    def test_04_config_x2(self):
        x2_opt = {
            'if': 'X2',
            'zone': "LAN",
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        rc = iface_v4_api.config_interface(**x2_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x2 failed')

    def test_05_config_x3(self):
        x3_opt = {
            'if': 'X3',
            'zone': "LAN",
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        rc = iface_v4_api.config_interface(**x3_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x2 failed')

    def test_06_config_x2_v6_on_local(self):
        x2_v6_opt = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X2_V6_IP,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = iface_v6_api.config_interface_ipv6(**x2_v6_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x2 v6 static addr failed!!!')

    def test_07_config_x3_v6_on_local(self):
        x3_v6_opt = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_V6_IP,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = iface_v6_api.config_interface_ipv6(**x3_v6_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x2 v6 static addr failed!!!')

    def test_08_config_x3_v6_on_server(self):
        x3_v6_opt = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.REM_X3_V6_IP,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = rem_iface_v6_api.config_interface_ipv6(**x3_v6_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x2 v6 static addr failed!!!')

    def test_09_add_dynamic_dhcpv6_scope_on_server(self):
        dynamic_scope_1 = {
            "name": "for_relay_x2",
            "range": {
                "from": "2001:1:2:3::100",
                "to": "2001:1:2:3::1ff"
            },
            "enable": True,
            "prefix": "2001:1:2:3::",
            "lifetime": {
                "valid": 2,
                "preferred": 1
            },
            "comment": "",
            "domain_name": "test.com",
            "dns": {
                "server":
                    {"static":
                        {
                            "primary": "100::1",
                            "secondary": "::",
                            "tertiary": "::"
                        }
                    }
            },
            "generic_option": {},
            "always_send_option": False
        }
        dynamic_scope_2 = {
            "name": "for_server_x3",
            "range": {
                "from": "2001:1:2:4::100",
                "to": "2001:1:2:4::101"
            },
            "enable": True,
            "prefix": "2001:1:2:4::",
            "lifetime": {
                "valid": 2,
                "preferred": 1
            },
            "comment": "",
            "domain_name": "",
            "dns": {
                "server": {
                    "inherit": True
                }
            },
            "generic_option": {},
            "always_send_option": False
        }
        rc = rem_dhcpv6_api.add_dhcp_server_scope_dynamic(
            **{"dhcp_server": {"ipv6": {"scope": {"dynamic": [dynamic_scope_1, dynamic_scope_2]}}}})
        Assertion.assert_equal(rc, True, 'ERR: add dynamic dhcpv6 scope on server failed!!!')

    def test_10_add_route_to_dut_x2(self):
        network_dict = {
            'object_type': 'network',
            'zone': 'LAN',
            "name": "2001:1:2:3::/64",
            "subnet": "2001:1:2:3::",
            "mask": "64"
        }
        rc = rem_ao_api.config_ipv6_addressobject(**network_dict)

        route_opt = {
            "comment": "",
            "interface": "X3",
            "metric": 12,
            "service": {"any": True},
            "gateway": {"name": "X3 IPv6 Primary Static Address"},
            "source": {"any": True},
            "destination": {"name": "2001:1:2:3::/64"},
            "disable_on_interface_down": True,
            "vpn_precedence": False,
            "probe": "",
            "distance": {"auto": True},
            "tos": "0x00",
            "mask": "0x00",
            "type": "standard"
        }
        rc &= rem_route_api.add_route_policy(**{"route_policies": [{"ipv6": route_opt}]})
        Assertion.assert_equal(rc, True, 'ERR: add route to DUT X2 on server failed!!!')

    def test_11_enable_ip_helper_on_dut(self):
        rc = ip_helper_api.enable_iphelper()
        Assertion.assert_equal(rc, True, 'ERR: enable IP Helper on DUT failed!!')

    def test_12_enable_dhcpv6_relay(self):
        rc = ip_helper_api.edit_protocol(name='DHCPv6', **{'enable': True})
        Assertion.assert_equal(rc, True, 'ERR: enable dhcpv6 relay protocol on DUT failed!!')

    def test_13_create_dhcpv6_relay_policy(self):
        policy_opt = {
            "ip_helper": {
                "policy": [
                    {
                        "egressif": "X3",
                        "protocol": "DHCPv6",
                        "source": {
                            "interface": "X2"
                        },
                        "destination": {
                            "ipv6": "2001:1:2:4::169"
                        },
                        "enable": True,
                        "comment": ""
                    }
                ]
            }
        }
        rc = ip_helper_api.add_policy(**policy_opt)
        Assertion.assert_equal(rc, True, 'ERR: add dhcpv6 relay policy on DUT failed')

    def test_14_config_pkt_moniter(self):
        param = {
            'monitor_filter': {
                'ip_types': 'udp',
                'destination_ports': '546,547'
            }
        }
        res = pkt_api.conf_packmon(**param)
        Assertion.assert_equal(res, True, 'ERR: config packet monitor failed.')
