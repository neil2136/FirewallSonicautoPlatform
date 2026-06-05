from definition.initial_param import *
from lib.utils import *


class Test_ipv6_nat_policies_01(Test):
    uuid = "SOSAIOT-TC-56611"
    jira = 'Gen7-21603'
    description = show_testcase_info(Parameter.TESTPLAN, "19", description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info('19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_01_01_config_x1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.wan_ip,
            'mgmt_ping': True,
        }
        out = interface_v6.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 ipv6 failed!")

    def test_01_02_add_addrobj_publicIP(self):
        obj = {
            'object_type': 'host',
            'name': 'Public-IP',
            'zone': 'WAN',
            'ip': Parameter.wan_ip,
        }
        rc = address_obj.config_ipv6_addressobject(**obj)
        Assertion.assert_equal(rc, True, "ERR: Add Public-IP address obj failed!")

    def test_01_03_add_addrobj_privateIP(self):
        obj = {
            'object_type': 'host',
            'name': 'Private-IP',
            'zone': 'WAN',
            'ip': Parameter.lan_host1,
        }
        rc = address_obj.config_ipv6_addressobject(**obj)
        Assertion.assert_equal(rc, True, "ERR: Add Public-IP address obj failed!")

    def test_01_04_add_ipv6_nat_policy(self):
        # source : trans_src -> Private IP; translated_src -> Public IP
        ipv6_nat_json = {
            "nat_policies": [{
                "ipv6": {
                    "name": "TEST1",
                    "reflexive": False,
                    "source_port_remap": True,
                    "comment": "test",
                    "enable": True,
                    "inbound": "X0",
                    "outbound": "X1",
                    "source": {
                        "name": "Private-IP"
                        },
                    "translated_source": {
                        "name": "Public-IP"
                        },
                    "destination": {
                        "any": True
                        },
                    "translated_destination": {
                        "original": True
                        },
                    "service": {
                        "any": True
                        },
                    "translated_service": {
                        "original": True
                        },
                    "ticket": {
                        "tag1": "",
                        "tag2": "",
                        "tag3": ""
                        }
                    }
                }]
            }
        rc = natpolicy_obj.add_nat_policy(**ipv6_nat_json)
        Assertion.assert_equal(rc, True, "ERR: Add ipv6 nat policy failed")

    def test_01_05_check_NATed_srcip_without_privateIP(self):
        rc = check_NATed_source_ip(ip='2001::100')
        Assertion.assert_equal(rc, True, "ERR: The NATed source ip with private ip!")

    def test_01_06_config_another_ipv6_address_on_PC1(self):
        # config another ipv6 addr of pc1.eth1
        rc1 = configure_ipv6_address_of_PC('d', Parameter.lan_host1, Parameter.lan_host1_if)
        rc2 = configure_ipv6_address_of_PC('a', Parameter.lan_host2, Parameter.lan_host1_if)
        Assertion.assert_equal(rc1 + rc2, '', "ERR: Configure ipv6 address on PC1 failed!")

    def test_01_07_check_NATed_src_ip_with_privateIP(self):
        rc = check_NATed_source_ip(ip='2001::110')
        Assertion.assert_equal(rc, False, "ERR: ICMP packet without your source ip")

    def test_01_08_resign_ipv6_address_on_PC1(self):
        # resign ipv6 addr of pc1.eth1
        rc1 = configure_ipv6_address_of_PC('d', Parameter.lan_host2, Parameter.lan_host1_if)
        rc2 = configure_ipv6_address_of_PC('a', Parameter.lan_host1, Parameter.lan_host1_if)
        Assertion.assert_equal(rc1 + rc2, '', "ERR: Configure ipv6 address on PC1 failed!")

    def test_01_09_delete_TEST1_nat_policy(self):
        rc = natpolicy_obj.del_nat_policy_by_name(name='TEST1', version='ipv6')
        Assertion.assert_equal(rc, True, "ERR: Delete TEST1 nat policy failed!")

    def test_01_10_delete_ipv6_addrobjs(self):
        rc1 = address_obj.delete_addressobject('host', object_path='name', object_name_uuid='Public-IP', ip_type='ipv6')
        rc2 = address_obj.delete_addressobject('host', object_path='name', object_name_uuid='Private-IP', ip_type='ipv6')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Delete address objects failed!")

    def test_01_11_unassign_X1_ipv6(self):
        rc = interface_v6.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(rc, True, "ERR: Unassign X1 ipv6 failed!")


class Test_ipv6_nat_policies_02(Test):
    uuid = "SOSAIOT-TC-56612"
    jira = 'Gen7-21603'
    description = show_testcase_info(Parameter.TESTPLAN, "23", description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info('23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_add_addrobjs(self):
        opt1 = {
            'name': 'WAN-IP-Translated',
            'zone': 'WAN',
            'object_type': 'range',
            'begin': '2001:1::20',
            'end': '2001:1::30'
        }
        rc1 = address_obj.config_ipv6_addressobject(**opt1)
        opt2 = {
            'name': 'WAN-IP-Pool',
            'zone': 'WAN',
            'object_type': 'range',
            'begin': Parameter.wan_host1,
            'end': Parameter.wan_host4,
        }
        rc2 = address_obj.config_ipv6_addressobject(**opt2)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Configure address objects failed!")

    def test_02_02_add_ipv6_nat_policy(self):
        # destination: trans_src -> WAN-IP-Translated; trans_dsn -> WAN-IP-Pool
        ipv6_nat_json = {
            "nat_policies": [{
                "ipv6": {
                    "name": "TEST2",
                    "reflexive": False,
                    "comment": "",
                    "enable": True,
                    "inbound": "X0",
                    "outbound": "any",
                    "source": {
                        "any": True
                        },
                    "translated_source": {
                        "original": True
                        },
                    "destination": {
                        "name": "WAN-IP-Translated"
                        },
                    "translated_destination": {
                        "name": "WAN-IP-Pool"
                        },
                    "service": {
                        "any": True
                        },
                    "translated_service": {
                        "original": True
                        },
                    "ticket": {
                        "tag1": "",
                        "tag2": "",
                        "tag3": ""
                        }
                    }
                }]
            }
        rc = natpolicy_obj.add_nat_policy(**ipv6_nat_json)
        Assertion.assert_equal(rc, True, "ERR: Add ipv6 nat policy failed")

    def test_02_03_add_ipv6_addrs_on_pc2(self):
        # add some ipv6 addresses for wan pc -> PC2 : 2001:1::101~103 (add all ip addrs in WAN-IP-Pool)
        rc1 = configure_ipv6_address_of_PC('a', Parameter.wan_host2, Parameter.wan_host1_if, PC='PC2')
        rc2 = configure_ipv6_address_of_PC('a', Parameter.wan_host3, Parameter.wan_host1_if, PC='PC2')
        rc3 = configure_ipv6_address_of_PC('a', Parameter.wan_host4, Parameter.wan_host1_if, PC='PC2')
        sleep(2)
        pc2_ssh.send_command('exit')
        Assertion.assert_equal(rc1 + rc2 + rc3, '', "ERR: Configure some ipv6 addresses on PC2 failed!")

    def test_02_04_check_NATed_dsnip_without_transIP(self):
        # ping ipv6 address in range : 2001:1::20~30 , and the WAN-IP-Pool in range : 2001:1::100~103
        rc = check_NATed_destination_ip(Parameter.translated_ips, Parameter.wan_ip_pool)
        Assertion.assert_equal(rc, True, "ERR: Check NATed destination ip failed!")

    def test_02_05_clear_added_ipv6_addrs_on_PC2(self):
        # delete some ipv6 addresses for wan pc -> PC2 : 2001:1::101~103
        rc1 = configure_ipv6_address_of_PC('d', Parameter.wan_host2, Parameter.wan_host1_if, PC='PC2')
        rc2 = configure_ipv6_address_of_PC('d', Parameter.wan_host3, Parameter.wan_host1_if, PC='PC2')
        rc3 = configure_ipv6_address_of_PC('d', Parameter.wan_host4, Parameter.wan_host1_if, PC='PC2')
        sleep(2)
        pc2_ssh.send_command('exit')
        Assertion.assert_equal(rc1 + rc2 + rc3, '', "ERR: Configure some ipv6 addresses on PC2 failed!")

    def test_02_06_delete_TEST2_nat_policy(self):
        rc = natpolicy_obj.del_nat_policy_by_name(name='TEST2', version='ipv6')
        Assertion.assert_equal(rc, True, "ERR: Delete TEST2 nat policy failed!")

    def test_02_07_delete_added_ipv6_addrobj(self):
        rc1 = address_obj.delete_addressobject('range', object_path='name', object_name_uuid='WAN-IP-Translated', ip_type='ipv6')
        rc2 = address_obj.delete_addressobject('range', object_path='name', object_name_uuid='WAN-IP-Pool', ip_type='ipv6')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Delete address objects failed!")


class Test_ipv6_nat_policies_03(Test):
    uuid = "SOSAIOT-TC-56615"
    jira = 'Gen7-21603'
    description = show_testcase_info(Parameter.TESTPLAN, "44", description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info('44')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_config_x1_ipv6(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IP,
            'mgmt_ping': True,
        }
        out = interface_v6.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 ipv6 failed!")

    def test_03_02_config_x2(self):
        x2_v4_opt = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_v4_IP,
            'mask': '255.255.255.0',
        }
        rc1 = interface_v4.config_interface(**x2_v4_opt)
        x2_v6_opt = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': Parameter.X2_IP,
            'mgmt_ping': True
        }
        rc2 = interface_v6.config_interface_ipv6(**x2_v6_opt)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Configure X2 failed!")

    def test_03_03_config_x3(self):
        x3_v4_opt = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_v4_IP,
            'mask': '255.255.255.0',
        }
        rc1 = interface_v4.config_interface(**x3_v4_opt)
        x3_v6_opt = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': Parameter.X3_IP,
            'mgmt_ping': True
        }
        rc2 = interface_v6.config_interface_ipv6(**x3_v6_opt)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Configure X3 failed!")

    def test_03_04_add_ipv6_nat_policies(self):
        # add translated src -> X0 to X1 LAN to WAN
        wan_ipv6_nat_json = {
            "nat_policies": [{
                "ipv6": {
                    "name": "WAN-IPv6-NAT-Policy",
                    "reflexive": False,
                    "source_port_remap": True,
                    "comment": "",
                    "enable": True,
                    "inbound": "X0",
                    "outbound": "X1",
                    "source": {
                        "any": True
                        },
                    "translated_source": {
                        "name": "X1 IPv6 Primary Static Address"
                        },
                    "destination": {
                        "any": True
                        },
                    "translated_destination": {
                        "original": True
                        },
                    "service": {
                        "any": True
                        },
                    "translated_service": {
                        "original": True
                        },
                    "ticket": {
                        "tag1": "",
                        "tag2": "",
                        "tag3": ""
                        }
                }
            }]
        }
        # add translated src -> X2 to X3 DMZ to WAN
        dmz_ipv6_nat_json = {
            "nat_policies": [{
                "ipv6": {
                    "name": "DMZ-IPv6-NAT-Policy",
                    "reflexive": False,
                    "source_port_remap": True,
                    "comment": "",
                    "enable": True,
                    "inbound": "X2",
                    "outbound": "X3",
                    "source": {
                        "any": True
                    },
                    "translated_source": {
                        "name": "X3 IPv6 Primary Static Address"
                    },
                    "destination": {
                        "any": True
                    },
                    "translated_destination": {
                        "original": True
                    },
                    "service": {
                        "any": True
                    },
                    "translated_service": {
                        "original": True
                    },
                    "ticket": {
                        "tag1": "",
                        "tag2": "",
                        "tag3": ""
                    }
                }
            }]
        }
        rc = natpolicy_obj.add_nat_policy(**wan_ipv6_nat_json)
        rc &= natpolicy_obj.add_nat_policy(**dmz_ipv6_nat_json)
        Assertion.assert_equal(rc, True, "ERR: Add ipv6 nat policies failed!")

    def test_03_05_export_firewall_settings(self):
        rc = setting.export_setting_exp()
        Assertion.assert_equal(rc, True, "ERR: Export preferences failed!")

    def test_03_06_restore_firewall(self):
        # mode = 2 -> restore-factory at current version, ssh_flag = True (set after booting up)
        rc = setting.boot_fw(mode=2)
        Assertion.assert_equal(rc, True, "ERR: restore dut failed")

    def test_03_07_enable_api_on_firewall(self):
        # enable api (make sure enable ssh)
        api_dict = {
            'sonicos-api': True,
            'basic': True,
        }
        result = admin.sonicos_api(**api_dict)
        Assertion.assert_equal(result, True, "Upload firmware failed!")

    def test_03_08_import_firewall_settings(self):
        rc = setting.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(rc, True, "ERR: Import preferences failed!")

    def test_03_09_check_wan_ipv6_nat_policy(self):
        rc = check_NATed_source_ip(ip=Parameter.X1_IP)
        Assertion.assert_equal(rc, False, "ERR: The NATed source ip without X1 ip!")

    def test_03_10_config_ipv6_route_on_pc(self):
        # PC1
        localhost.send_command("ip -6 r d default via {} dev {} metric 100".format(Parameter.X0_IP, Parameter.lan_host1_if))
        rc1 = localhost.send_command("ip -6 r a default via {} dev {} metric 100".format(Parameter.X2_IP, Parameter.dmz_host1_if))
        # PC2
        pc2_ssh.send_command("ip -6 r d default via {} dev {} metric 100".format(Parameter.X1_IP, Parameter.wan_host1_if))
        rc2 = pc2_ssh.send_command("ip -6 r a default via {} dev {} metric 100".format(Parameter.X3_IP, Parameter.x3_host_if))
        Assertion.assert_equal(rc1+rc2, '', "ERR: Configure ipv6 route on pc failed!")

    def test_03_11_check_dmz_ipv6_nat_policy(self):
        rc = check_NATed_source_ip(ip=Parameter.X3_IP, eth='eth3', ping_ip=Parameter.x3_host)
        Assertion.assert_equal(rc, False, "ERR: The NATed source ip without X3 ip!")

    def test_03_12_delete_added_nat_policies(self):
        rc = natpolicy_obj.del_nat_policy_by_name(name='WAN-IPv6-NAT-Policy', version='ipv6')
        rc2 = natpolicy_obj.del_nat_policy_by_name(name='DMZ-IPv6-NAT-Policy', version='ipv6')
        Assertion.assert_equal(rc & rc2, True, "ERR: Delete WAN-IPv6-NAT-Policy nat policy failed!")

    def test_03_13_resign_ipv6_address_on_pc(self):
        #  PC1
        rc1 = localhost.send_command("ip -6 r d default via {} dev {} metric 100".format(Parameter.X2_IP, Parameter.dmz_host1_if))
        #  PC2
        rc2 = pc2_ssh.send_command("ip -6 r d default via {} dev {} metric 100".format(Parameter.X3_IP, Parameter.x3_host_if))
        Assertion.assert_equal(rc1+rc2, '', 'ERR: Resign ipv6 route on pc failed!')












