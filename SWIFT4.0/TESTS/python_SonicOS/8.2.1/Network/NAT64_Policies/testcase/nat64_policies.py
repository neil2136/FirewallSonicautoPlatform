from definition.init_param import *


class Test_nat64_policies_01(Test):
    uuid = '1510936'
    description = show_testcase_info(Parameter.TESTPLAN, "2", description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info('2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_01_01_add_nat64_policy(self):
        nat64_json = {
            "nat_policies": [
                {"nat64": {
                    "comment": "test",
                    "enable": True,
                    "inbound": "any",
                    "name": "TEST1",
                    "outbound": "any",
                    "pref64": {"name": "Well-Known Pref64"},
                    "service": {"icmp_udp_tcp": True},
                    "source": {"any": True},
                    "ticket": {"tag1": "", "tag2": "", "tag3": ""},
                    "translated_destination": {"embedded_ipv4_address": True},
                    "translated_service": {"original": True},
                    "translated_source": {"name": "X1 IP"}
                    }
                }
            ]
        }
        rc = nat64_opt.add_nat64_policy(**nat64_json)
        Assertion.assert_equal(rc, True, 'ERR: Add NAT64 policy failed!')

    def test_01_02_delete_nat64_policy(self):
        rc = nat64_opt.del_nat_policy(name='TEST1', version='nat64')
        Assertion.assert_equal(rc, True, 'ERR: Delete NAT64 policy failed!')


class Test_nat64_policies_02(Test):
    uuid = '1510943'
    description = show_testcase_info(Parameter.TESTPLAN, "50", description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info('50')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_02_01_add_DMZ_addrObj(self):
        addr_opt = {
            'name': 'DMZ Obj',
            'zone': 'DMZ',
            'object_type': 'network',
            'subnet': '64:9999::',
            'mask': '96',
        }
        rc = address_obj.config_ipv6_addressobject(**addr_opt)
        Assertion.assert_equal(rc, True, 'ERR: Add DMZ address object failed!')

    def test_02_02_add_nat64_policy(self):
        nat64_json = {
            "nat_policies": [
                {"nat64": {
                    "comment": "test",
                    "enable": True,
                    "inbound": "any",
                    "name": "DMZ NAT64",
                    "outbound": "any",
                    "pref64": {"name": "DMZ Obj"},
                    "service": {"icmp_udp_tcp": True},
                    "source": {"any": True},
                    "ticket": {"tag1": "", "tag2": "", "tag3": ""},
                    "translated_destination": {"embedded_ipv4_address": True},
                    "translated_service": {"original": True},
                    "translated_source": {"name": "X2 IP"}
                }
                }
            ]
        }
        rc = nat64_opt.add_nat64_policy(**nat64_json)
        Assertion.assert_equal(rc, True, 'ERR: Add NAT64 policy failed!')

    def test_02_03_add_accessrull_WAN_to_WAN(self):
        aar_opt = {
            "access_rules": [
                {"ipv6": {
                    "action": "allow",
                    "botnet_filter": False,
                    "comment": "",
                    "connection_limit": {"destination": {}, "source": {}},
                    "destination": {"address": {"any": True}},
                    "dpi": True,
                    "dpi_ssl": {"client": True, "server": True},
                    "enable": True,
                    "flow_reporting": False,
                    "fragments": True,
                    "from": "WAN",
                    "geo_ip_filter": {"enable": False},
                    "h323": False,
                    "logging": True,
                    "management": False,
                    "max_connections": 100,
                    "name": "WANtoWAN",
                    "packet_monitoring": False,
                    "priority": {"auto": True},
                    "quality_of_service": {"class_of_service": {}, "dscp": {"preserve": True}},
                    "reflexive": False,
                    "service": {"any": True},
                    "sip": False,
                    "source": {"address": {"any": True}, "port": {"any": True}},
                    "tcp": {"timeout": 15, "urgent": False},
                    "to": "WAN",
                    "udp": {"timeout": 30},
                    "users": {"excluded": {"none": True}, "included": {"all": True}}
                }}
            ]
        }
        rc = accessrule_opt.add_ipv6_accessrule(**aar_opt)
        Assertion.assert_equal(rc, True, 'ERR: Add WAN to WAN ipv6 accessrule failed!')

    def test_02_04_allow_accessrule_WAN_to_DMZ(self):
        aar_opt = {
            'option': 'modify',
            'name': 'Default Access Rule',
            'from': 'WAN',
            'to': 'DMZ',
            'action': 'allow',
        }
        rc = accessrule_opt.config_ipv6_access_rule(**aar_opt)
        Assertion.assert_equal(rc, True, 'ERR: Allow WAN to DMZ accessrule failed!')

    def test_02_05_test_ping_success(self):
        cmd = 'ping6 {} -c 4'.format(Parameter.X1_IPV6)
        rc = pc2_ssh.send_command(cmd)
        Assertion.assert_not_regular(rc, r'100% packet loss', 'ERR: Faild to ping server from client!')

    
class Test_nat64_policies_03(Test):
    uuid = '1510944'
    description = show_testcase_info(Parameter.TESTPLAN, "51", description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info('51')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!")

    def test_03_01_add_nat64_policy(self):
        nat64_json = {
            "nat_policies": [
                {"nat64": {
                    "comment": "test",
                    "enable": True,
                    "inbound": "any",
                    "name": "X1 NAT64",
                    "outbound": "any",
                    "pref64": {"name": "Well-Known Pref64"},
                    "service": {"icmp_udp_tcp": True},
                    "source": {"any": True},
                    "ticket": {"tag1": "", "tag2": "", "tag3": ""},
                    "translated_destination": {"embedded_ipv4_address": True},
                    "translated_service": {"original": True},
                    "translated_source": {"name": "X1 IP"}
                }
                }
            ]
        }
        rc = nat64_opt.add_nat64_policy(**nat64_json)
        Assertion.assert_equal(rc, True, 'ERR: Add NAT64 policy failed!')

    def test_03_02_test_ping_success(self):
        cmd = 'ping6 {} -c 4'.format(Parameter.X1_IPV6)
        rc = pc2_ssh.send_command(cmd)
        Assertion.assert_not_regular(rc, r'100% packet loss', 'ERR: Faild to ping X1 ipv6')