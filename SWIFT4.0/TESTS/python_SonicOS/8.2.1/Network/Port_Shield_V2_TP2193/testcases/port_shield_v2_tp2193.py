from definition.settings import *
from definition.utils import *


# Expect: Creating a Portshield Group
# this case including TC15
class TestPortShield_TC2(Test):
    uuid = "SOSAIOT-TC-57107"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = interfacev4api.config_interface(**x2_static)
        Assertion.assert_equal(res, True, 'ERR: config x2 failed')

    def test_02_config_x3_portshield_to_x2(self):
        resp = {}
        x3_dict = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'portshield',
            'portshield_to': 'X2'
        }
        conf_res = interfacev4api.config_interface(**x3_dict)
        if conf_res:
            resp = interfacev4api.get_interface_status('x3')
        Assertion.assert_regular(json.dumps(
            resp), '"mode": {"portshield": "X2"}', 'ERR: config x2 failed')

    def test_03_add_dhcpserver_bound_to_x2(self):
        dynamic_scope_x2 = {
            "dhcp_server":
                {"ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "12.12.2.10",
                                "to": "12.12.2.100",
                                "enable": True,
                                "lease_time": 60,
                                "default_gateway": "12.12.2.168",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "domain_name": "",
                                "dns": {"server": {"inherit": True}},
                            }
                        ]
                    }
                }
                }
        }
        res = dhcpserverapi.add_dhcp_server_scope_dynamic(**dynamic_scope_x2)
        Assertion.assert_equal(
            res, True, 'ERR: add dhcp server bound to X2 interface failed')

    def test_04_verify_traffic_of_portshield_group(self):
        res2 = False
        res1, pc3_eth1_ip = pc_get_ip_lease(pc3_ssh, 'eth1')
        if res1:
            res2 = pc3_ssh.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1')
        Assertion.assert_equal(
            res1 & res2, True, "ERR: verify traffic between portshiled group failed.")


# Expect: DHCP on a Portshield Group
class TestPortShield_TC15(Test):
    uuid = "SOSAIOT-TC-57103"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x4_portshield_to_x2(self):
        resp = {}
        x4_dict = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'portshield',
            'portshield_to': 'X2'
        }
        conf_res = interfacev4api.config_interface(**x4_dict)
        if conf_res:
            resp = interfacev4api.get_interface_status('x4')
        Assertion.assert_regular(json.dumps(
            resp), '"mode": {"portshield": "X2"}', 'ERR: config x2 failed')

    def test_01_verify_dhcp_function(self):
        res, pc4_eth1_ip = pc_get_ip_lease(pc4_ssh, 'eth1')
        Assertion.assert_equal(
            res, True, "ERR: verify dhcp function of portshiled group failed.")


#Expect: Verify traffic connectivity after portshield host interface link down.
class TestPortShield_TC17(Test):
    uuid = "SOSAIOT-TC-57096"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unplug_x2(self):
        res = interfacev4api.disable_interface(name='x2')
        Assertion.assert_equal(res, True, 'shutdown x2 failed.')

    @repeat_method(3)
    def test_02_verify_connction(self):
        res = True
        for i in range(3):
            res = pc3_ssh.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1')
            if not res:
                break
        Assertion.assert_equal(res, False, 'verify connection failed.')

    @repeat_method(3)
    def test_03_up_x2(self):
        res = interfacev4api.enable_interface(name='x2')
        Assertion.assert_equal(res, True, 'up x2 failed.')


# Expect: Configuration restrictions after an interface is configured in Portshield Switch Mode
class TestPortShield_TC6(Test):
    uuid = "SOSAIOT-TC-57111"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_group_and_member_zone_cannot_be_changed(self):
        x3_dict = {
            'if': 'x3',
            'zone': 'DMZ',
            'mode': 'portshield',
            'portshield_to': 'X2'
        }
        x2_dict = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res1 = interfacev4api.config_interface(**x3_dict)
        res2 = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(
            res1 | res2, False, 'ERR: verify portshield group and member interface can not be changed failed')

    def test_02_verify_member_cannot_be_routing(self):
        tag = []
        x3_rip_dict = {
            'interface': 'X3',
            'mode': 'send_and_receive',
        }
        res_rip1, msg1 = droutingapi.set_rip(**x3_rip_dict, msg=True)
        tag.append(not res_rip1)
        res_rip2 = True if 'RIP: RIP Mode: Cannot update unconfigured interface' in str(
            msg1) else False
        tag.append(res_rip2)
        x3_ospf_dict = {
            'interface': 'X3',
            'mode': 'enable',
            'hello_interval': '5',
            'dead_interval': '20',
        }
        res_ospf1, msg2 = droutingapi.set_ospf2(**x3_ospf_dict, msg=True)
        tag.append(not res_ospf1)
        res_ospf2 = True if 'OSPF: OSPF Mode: Interface with 0.0.0.0/0 address is not allowed to enable OSPF' in str(
            msg2) else False
        tag.append(res_ospf2)
        Assertion.assert_equal(all(
            tag), True, 'ERR: verify portshield group member interface can not be routing failed')

    def test_03_verify_vlan_cannot_bound_to_member(self):
        vlan_dict = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': 100,
            'zone': 'LAN',
            'mode': 'static',
            'ip': '100.1.1.1'
        }
        res1, msg = interfacev4api.add_interface(**vlan_dict, msg=True)
        res2 = True if '"vlan" is not a reasonable value' in str(
            msg) else True
        Assertion.assert_equal(
            res1 & res2, False, 'ERR: verify vlan can not bound to portshield member interface failed.')


# Expect: Removing an interface from a Portshield Group
class TestPortShield_TC7(Test):
    uuid = "SOSAIOT-TC-57112"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_remove_portshield_group(self):
        res = interfacev4api.unassign_interface(interface='x3')
        Assertion.assert_equal(
            res, True, 'ERR: remove portshield group failed.')

    def test_02_config_x3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = interfacev4api.config_interface(**x3_static)
        Assertion.assert_equal(res, True, 'ERR: config x3 failed')

    def test_03_verify_address_object_back(self):
        tag = []
        resp1 = aoapi.get_addressobject_by_name(name='X3 IP', version='ipv4')
        resp2 = aoapi.get_addressobject_by_name(
            name='X3 Subnet', version='ipv4')
        try:
            res1 = True if resp1['address_objects'][0]['ipv4']['host']['ip'] == Parameter.X3_IP else False
            res2 = True if resp2['address_objects'][0]['ipv4']['network']['subnet'] == Parameter.X3_NET else False
            tag.append(res1)
            tag.append(res2)
        except Exception as e:
            logger.error(repr(e))
            tag.append(False)
        Assertion.assert_equal(all(
            tag), True, 'ERR: verify address object back after remove portshield group failed.')

    def test_04_verify_nat_policy_back(self):
        tag = []
        resp = str(natapi.get_nat_policy())
        try:
            if "'inbound': 'X3'" in resp and "'outbound': 'X3'" in resp:
                if "'service': {'group': 'Ping'}" in resp:
                    logger.info(
                        'check default Ping management nat policy success.')
                    tag.append(True)
            else:
                logger.info('check default Ping management nat policy failed.')
                tag.append(False)
            if "'inbound': 'X3'" in resp and "'outbound': 'X3'" in resp:
                if "translated_source': {'name': 'X1 IP'}" in resp:
                    logger.info('check default out nat policy failed.')
                    tag.append(True)
            else:
                logger.info('check default out nat policy failed.')
                tag.append(False)
        except Exception as e:
            logger.error(repr(e))
            tag.append(False)
        Assertion.assert_equal(all(
            tag), True, 'ERR: verify nat policy back after remove portshield group failed.')

    def test_05_verify_route_policy_back(self):
        res = False
        resp = str(routeapi.show_route_policy(version='ipv4'))
        try:
           if "'interface': 'X3'" in resp and "'destination': {'name': 'X3 Subnet'}" in resp:
               res = True
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(
            res, True, 'ERR: verify route policy back after remove portshield group failed.')


# Expect: Verify that broadcast frames are flooded to all portshield group member interfaces
class TestPortShield_TC12(Test):
    uuid = "SOSAIOT-TC-57100"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x3_portshield_to_x2(self):
        x3_dict = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'portshield',
            'portshield_to': 'X2'
        }
        res = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(
            res, True, 'ERR: config x3 port shield to X2 failed')

    def test_02_config_x4_portshield_to_x2(self):
        x4_dict = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'portshield',
            'portshield_to': 'X2'
        }
        res = interfacev4api.config_interface(**x4_dict)
        Assertion.assert_equal(
            res, True, 'ERR: config x4 port shield to X2 failed')

    @repeat_method(10, sleep=10)
    def test_03_verify_broadcast_frames(self):
        #capture on pc3, pc4
        cmd = "rm -f /tmp/tcpdump.file; timeout 5 tcpdump -i eth1 -c 5 arp  &> /tmp/tcpdump.file &"
        pc3_ssh.send_command(cmd)
        pc4_ssh.send_command(cmd)
        time.sleep(2)

        #send arp packets on pc2
        pc2_eth1_mac = get_pc_mac(pc2_ssh, 'eth1')
        src_ip = "12.12.2.4"
        cmd = f'python3 {script_path} -srcmac {pc2_eth1_mac} -iface eth1 -psrc {src_ip} -pdst {Parameter.X2_IP}'
        pc2_ssh.send_command(cmd)
        time.sleep(30)

        # check arp packets on pc3,pc4
        pc3_ssh.send_command('killall tcpdump')
        pc4_ssh.send_command('killall tcpdump')
        out1 = pc3_ssh.send_command('cat /tmp/tcpdump.file')
        out2 = pc4_ssh.send_command('cat /tmp/tcpdump.file')
        logger.info(f'packets captured on PC3:\n{out1}')
        logger.info(f'packets captured pn PC4:\n{out2}')
        res1 = 'ARP' in out1 and src_ip in out1
        logger.info(f'check packets result for PC3: {res1}')
        res2 = 'ARP' in out2 and src_ip in out2
        logger.info(f'check packets result for PC4: {res2}')
        Assertion.assert_equal(
            res1 & res2, True, 'ERR: verify broadcast frames failed')
