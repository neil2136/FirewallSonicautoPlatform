import json
from definition.settings import *
from definition.utils import *


# Expect: verify DMZ to WAN One-to-One policy for outbound traffic
class TestDMZNAT_TC34(Test):
    uuid = "SOSAIOT-TC-55938"
    description = show_testcase_info(TESTPLAN, '34', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_policy(self):
        base_dict = copy.deepcopy(nat_base_dict)
        base_dict.update(edit_dict_tc34)
        nat_dict = {"nat_policies": [{"ipv4": base_dict}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        logger.info(f'add nat policy result: {addres}')
        resp = natpolicyapi.get_nat_policy(name=edit_dict_tc34['name'])
        Assertion.assert_regular(json.dumps(
            resp), '"name": "test_for_case_34"', 'ERR: add nat policy failed')

    def test_02_config_packet_monitor(self):
        confres = packetapi.monitor_default()
        logger.info(f'monitor packets to default result: {confres}')
        monitor_conf_dict = {
            'monitor_filter': {
                'ether_types': 'ip',
                'ip_types': 'icmp'
            }
        }
        res = packetapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(res, True, 'ERR: Config packet monitor failed')

    def test_03_verify_traffic(self):
        res = False
        clearres = packetapi.clear_packets()
        logger.info(f'clear packtes result: {clearres}')
        startres = packetapi.start_capture()
        logger.info(f'start capture packtes result: {startres}')
        pingres = pc3_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1', num=10)
        time.sleep(10)
        stopres = packetapi.stop_capture()
        logger.info(f'stop capture packtes result: {stopres}')
        if pingres:
            resp = packetapi.export_captured_packets()
            res, output = icmp_packet_check(
                resp, Parameter.X1_IP, PC2_ETH1_IP, 'X1')
            logger.info(output)
        Assertion.assert_equal(
            res, True, 'ERR: test one to one outbound dmz to wan nat policy failed')

    def test_04_del_nat_policy(self):
        res = natpolicyapi.del_nat_policy_by_name(name=edit_dict_tc34['name'])
        Assertion.assert_equal(res, True, 'ERR: remove config failed')


# Expect: Verify WAN to DMZ One-to-One policy for inbound traffic
class TestDMZNAT_TC35(Test):
    uuid = "SOSAIOT-TC-55939"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_policy(self):
        base_dict = copy.deepcopy(nat_base_dict)
        base_dict.update(edit_dict_tc35)
        nat_dict = {"nat_policies": [{"ipv4": base_dict}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        logger.info(f'add nat policy result: {addres}')
        resp = natpolicyapi.get_nat_policy(name=edit_dict_tc35['name'])
        Assertion.assert_regular(json.dumps(
            resp), '"name": "test_for_case_35"', 'ERR: add nat policy failed')

    def test_02_add_wan_to_dmz_acl(self):
        acl_dict = {
            "name": "wan_to_dmz_acl",
            'from': "WAN",
            "to": "DMZ",
            "action": "allow",
            "source_addr": {"any": True},
            "dst_addr": {"any": True},
            "service": {"group": "Ping"}
        }
        res = aclapi.add_ipv4_access_rule(**acl_dict)
        Assertion.assert_equal(
            res, True, "ERR: add wan to dmz acl ping service failed")

    def test_03_verify_traffic(self):
        res = False
        clearres = packetapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetapi.start_capture()
        logger.info(f'start capture result: {startres}')
        pingres = pc2_login.ping_from_eth(
            ip=Parameter.X1_NAT_IP, eth='eth1', num=20)
        time.sleep(10)
        stopres = packetapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        if pingres:
            resp = packetapi.export_captured_packets()
            logger.info(resp)
            res, output = icmp_packet_check(
                resp, PC2_ETH1_IP, PC3_ETH1_IP, 'X4')
            logger.info(output)
        Assertion.assert_equal(res, True, "ERR: verify traffic failed")

    def test_04_del_nat_policy(self):
        res = natpolicyapi.del_nat_policy_by_name(name=edit_dict_tc35['name'])
        Assertion.assert_equal(res, True, 'ERR: remove config failed')


# Expect: Verify WAN to multiple DMZs Many-to-Many policy for inbound traffic
class TestDMZNAT_TC37(Test):
    uuid = "SOSAIOT-TC-55940"
    description = show_testcase_info(TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_dmzpc_group(self):
        ag_dict = {
            "address_groups": [{
                "ipv4": {
                    "address_object": {
                        "ipv4": [{"name": "dmz_pc1"}, {"name": "dmz_pc2"}]
                    },
                    "name": 'dmz_pc_group'
                }
            }]
        }
        res = agapi.add_addressgroup(**ag_dict)
        Assertion.assert_equal(res, True, 'ERR: create dmz pc group failed')

    def test_02_create_wan_group(self):
        ag_dict = {
            "address_groups": [{
                "ipv4": {
                    "address_object": {
                        "ipv4": [{"name": "wan_ao1"}, {"name": "wan_ao2"}]
                    },
                    "name": 'wan_nat_group'
                }
            }]
        }
        res = agapi.add_addressgroup(**ag_dict)
        Assertion.assert_equal(res, True, 'ERR: create dmz pc group failed')

    def test_03_add_nat_policy(self):
        base_dict = copy.deepcopy(nat_base_dict)
        base_dict.update(edit_dict_tc37)
        nat_dict = {"nat_policies": [{"ipv4": base_dict}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        logger.info(f'add nat policy result: {addres}')
        resp = natpolicyapi.get_nat_policy(name=edit_dict_tc37['name'])
        Assertion.assert_regular(json.dumps(
            resp), '"name": "test_for_case_37"', 'ERR: add nat policy failed')

    def test_04_verify_traffic(self):
        # ping from wan host 1: pc2
        res1 = pc2_login.ping_from_eth(
            ip=Parameter.X1_NAT_IP, eth='eth1', num=10)
        # ping from wan host 2: pc1 eth3
        res2 = localhost.ping_from_eth(
            ip=Parameter.X3_NAT_IP, eth='eth3', num=10)
        Assertion.assert_equal(res1 & res2, True, "ERR: verify traffic failed")

    def test_05_del_nat_policy(self):
        res = natpolicyapi.del_nat_policy_by_name(name=edit_dict_tc37['name'])
        Assertion.assert_equal(res, True, 'ERR: remove config failed')


# Expect: Verify WAN to DMZ One-to-Many policy for inbound traffic
class TestDMZNAT_TC40(Test):
    uuid = "SOSAIOT-TC-55941"
    description = show_testcase_info(TESTPLAN, '40', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '40')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_nat_policy(self):
        base_dict = copy.deepcopy(nat_base_dict)
        base_dict.update(edit_dict_tc40)
        nat_dict = {"nat_policies": [{"ipv4": base_dict}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        logger.info(f'add nat policy result: {addres}')
        resp = natpolicyapi.get_nat_policy(name=edit_dict_tc40['name'])
        Assertion.assert_regular(json.dumps(
            resp), '"name": "test_for_case_40"', 'ERR: add nat policy failed')

    def test_02_verify_traffic(self):
        res = pc2_login.ping_from_eth(
            ip=Parameter.X1_NAT_IP, eth='eth1', num=10)
        Assertion.assert_equal(res, True, "ERR: verify traffic failed")

    def test_03_del_nat_policy(self):
        res = natpolicyapi.del_nat_policy_by_name(name=edit_dict_tc40['name'])
        Assertion.assert_equal(res, True, 'ERR: remove config failed')


# Expect: Verify inbound Port Address Translation via One-to-One NAT Policy
class TestDMZNAT_TC41(Test):
    uuid = "SOSAIOT-TC-55942"
    description = show_testcase_info(TESTPLAN, '41', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '41')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_service_object(self):
        service_dict = {
            "object_type": "tcp",
            "name": "http_8888",
            "tcp": {
                "begin": 8888,
                "end": 8888
            }
        }
        res, uuidname = serviceobjectapi.config_service_object(**service_dict)
        logger.info(f'create service object result: {res}, {uuidname}')
        Assertion.assert_equal(res, True, "ERR: add service object failed")

    def test_02_add_nat_policy(self):
        base_dict = copy.deepcopy(nat_base_dict)
        edit_dict_tc41 = {
            "name": "test_for_case_41",
            "destination": {
                "name": "wan_ao1"
            },
            "translated_destination": {
                "name": "dmz_pc1"
            },
            "inbound": "X1",
            "service": {"name": "http_8888"},
            "translated_service": {"name": "HTTPS"}
        }
        base_dict.update(edit_dict_tc41)
        nat_dict = {"nat_policies": [{"ipv4": base_dict}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        logger.info(f'add nat policy result: {addres}')
        resp = natpolicyapi.get_nat_policy(name=edit_dict_tc41['name'])
        Assertion.assert_regular(json.dumps(
            resp), '"name": "test_for_case_41"', 'ERR: add nat policy failed')

    def test_03_add_wan_to_dmz_https_acl(self):
        acl_dict = {
            "name": "wan_to_lan_acl_https",
            'from': "WAN",
            "to": "DMZ",
            "action": "allow",
            "source_addr": {"any": True},
            "dst_addr": {"any": True},
            "service": {"name": "http_8888"}
        }
        res = aclapi.add_ipv4_access_rule(**acl_dict)
        Assertion.assert_equal(res, True, "ERR: add access rules failed")

    @repeat_method(5)
    def test_04_verify_service_map(self):
        res = pc2_login.send_command(
            f'curl -k https://{Parameter.X1_NAT_IP}:8888')
        Assertion.assert_regular(
            res, f'hello', "ERR: service map one to one nat policy failed")


# Expect: Verify when One-to-One NAT Policy configured, LAN host can access DMZ server by using server's public address
class TestDMZNAT_TC44(Test):
    uuid = "SOSAIOT-TC-55943"
    description = show_testcase_info(TESTPLAN, '44', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dmz_ao(self):
        dmz_ao = {
            'object_type': 'host',
            'name': 'dmz_ao',
            'zone': 'DMZ',
            'value': Parameter.X4_NAT_IP
        }
        lan_ao = {
            'object_type': 'host',
            'name': 'lan_ao',
            'zone': 'LAN',
            'value': PC1_ETH1_IP
        }
        res = aoapi.config_addressobject(**dmz_ao)
        res &= aoapi.config_addressobject(**lan_ao)
        Assertion.assert_equal(res, True, 'ERR: add dmz ao failed')

    def test_02_add_nat_policy(self):
        base_dict = copy.deepcopy(nat_base_dict)
        base_dict.update(edit_dict_tc44)
        nat_dict = {"nat_policies": [{"ipv4": base_dict}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        logger.info(f'add nat policy result: {addres}')
        resp = natpolicyapi.get_nat_policy(name=edit_dict_tc44['name'])
        Assertion.assert_regular(json.dumps(
            resp), '"name": "test_for_case_44"', 'ERR: add nat policy failed')

    def test_04_verify_traffic(self):
        res = False
        clearres = packetapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetapi.start_capture()
        logger.info(f'start capture result: {startres}')
        pingres = localhost.ping_from_eth(
            ip=PC4_ETH1_IP, eth='eth1', num=10)
        time.sleep(10)
        stopres = packetapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        if pingres:
            resp = packetapi.export_captured_packets()
            logger.info(resp)
            res, output = icmp_packet_check(
                resp, PC1_ETH1_IP, PC4_ETH1_IP, 'X5')
            logger.info(output)
        Assertion.assert_equal(res, True, "ERR: verify traffic failed")

    def test_05_del_nat_policy(self):
        natpolicyapi.del_nat_policy_by_name(name=edit_dict_tc44['name'])
        Assertion.assert_equal(True, True, 'ERR: remove config failed')


# Expect: Verify WAN to DMZ One-to-One policy for inbound traffic when WAN is PPTP mode
class TestDMZNAT_TC47(Test):
    uuid = "SOSAIOT-TC-55944"
    description = show_testcase_info(TESTPLAN, '47', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '47')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x1_to_pptp_mode(self):
        x1_pptp = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pptp',
            'pptp_user': 'test',
            'pptp_passwd': 'password',
            'pptp_server': PC2_ETH1_IP,
            'pptp_ip': '10.10.0.100',
            'pptp_netmask': '255.255.255.0',
            'pptp_gateway': '10.10.0.1',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        res = interfacev4api.config_interface(**x1_pptp)
        Assertion.assert_equal(res, True, 'ERR: config x1 to pptp mode failed')

    def test_02_configure_route_on_pc2(self):
        pc2_login.send_command('route del -net 10.10.0.0/24 gw 10.10.0.168')
        logger.info('=> check del route on pc2 result.')
        output = pc2_login.send_command('ip -4 r')
        res = True if '10.10.0.0/24 via 10.10.0.168' not in output else False
        Assertion.assert_equal(
            res, True, 'ERR: configure route on pc2 failed')

    def test_03_verify_x1_ip(self):
        res = False
        for i in range(5):
            time.sleep(5)
            resp = interfacev4api.get_interface_address("X1")
            try:
                x1_ip = resp["ip_address"]
                if x1_ip != '0.0.0.0':
                    if x1_ip.startswith('11.11.11'):
                        logger.info(f'x1 pptp ip is: {x1_ip}')
                        res = True
                        break
                else:
                    logger.info('x1 failed to get pptp ip.')
            except Exception as e:
                logger.error(repr(e))
        Assertion.assert_equal(
            res, True, "ERR: Verify X1 as PPTP mode failed!")

    def test_04_add_wan_ao(self):
        wan_host3 = {
            'object_type': 'host',
            "name": "wan_ao3",
            "zone": "WAN",
            "value": Parameter.X1_PPTP_NAT_IP
        }
        res = aoapi.config_addressobject(**wan_host3)
        Assertion.assert_equal(res, True, 'ERR: add wan host ao failed')

    def test_05_add_nat_policy(self):
        base_dict = copy.deepcopy(nat_base_dict)
        edit_dict_tc47 = {
            "name": "test_for_case_47",
            "destination": {
                "name": "wan_ao3"
            },
            "translated_destination": {
                "name": "dmz_pc2"
            },
            "inbound": "X1"
        }
        base_dict.update(edit_dict_tc47)
        nat_dict = {"nat_policies": [{"ipv4": base_dict}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        logger.info(f'add nat policy result: {addres}')
        resp = natpolicyapi.get_nat_policy(name=edit_dict_tc47['name'])
        Assertion.assert_regular(json.dumps(
            resp), '"name": "test_for_case_47"', 'ERR: add nat policy failed')

    def test_06_add_route_to_pptp_network_on_pc2(self):
        resp = interfacev4api.get_interface_address("X1")
        x1_ip = ''
        try:
            x1_ip = resp['ip_address']
        except Expection as e:
            logger.error(repr(e))
        logger.info(f'x1 ip addr: {x1_ip}')
        cmd = f'route add -net 11.11.11.0/24 gw {x1_ip}'
        pc2_login.send_command(cmd)
        logger.info('=> check add route result')
        output = pc2_login.send_command('ip -4 r')
        res = True if f'11.11.11.0/24 via {x1_ip}' in output else False
        Assertion.assert_equal(res, True, 'ERR: add route failed on pc2')

    def test_07_verify_traffic(self):
        res = False
        clearres = packetapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetapi.start_capture()
        logger.info(f'start capture result: {startres}')
        pingres = pc2_login.ping_from_eth(
            ip=Parameter.X1_PPTP_NAT_IP, eth='eth1', num=10)
        time.sleep(10)
        stopres = packetapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        if pingres:
            resp = packetapi.export_captured_packets()
            logger.info(resp)
            res, output = icmp_packet_check(
                resp, PC2_ETH1_IP, PC4_ETH1_IP, 'X5')
            logger.info(output)
        Assertion.assert_equal(res, True, "ERR: verify traffic failed")
