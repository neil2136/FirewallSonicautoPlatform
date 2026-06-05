from definition.settings import *


# Expected: add VLAN1 and VLAN2 to X4 successful
class TestVLAN_TC01(Test):
    uuid = "SOSAIOT-TC-57262"
    description = show_testcase_info(
        Parameter.TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X4_LAN_zone(self):
        x4_static_dict = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfacev4api.config_interface(**x4_static_dict)
        Assertion.assert_equal(
            rc, True, "ERR: Config X4 to static LAN Zone failed")

    def test_02_add_VLAN_subinterface_to_X4(self):
        x4_dmz_vlan1_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN1_ID,
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X4_VLAN1_IP,
        }
        x4_lan_vlan2_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN2_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN2_IP,
        }
        rc1 = interfacev4api.add_interface(**x4_dmz_vlan1_dict)
        rc2 = interfacev4api.add_interface(**x4_lan_vlan2_dict)
        Assertion.assert_equal(
            rc1 & rc2, True, "ERR: Add Vlan interfaces to X4 failed")


# Expected: delete VLAN1 and VLAN2 in X4 successful
class TestVLAN_TC24(Test):
    uuid = "SOSAIOT-TC-57277"
    description = show_testcase_info(
        Parameter.TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_VLAN_subinterface(self):
        x4_del_vlan1_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': str(X4_VLAN1_ID),
        }
        x4_del_vlan2_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': str(X4_VLAN2_ID),
        }
        rc1 = interfacev4api.del_interface(**x4_del_vlan1_dict)
        rc2 = interfacev4api.del_interface(**x4_del_vlan2_dict)
        Assertion.assert_equal(
            rc1 & rc2,
            True,
            "ERR: Delete X4 Vlan sub interfaces failed")


# Expected: add VLAN use LAN/WAN/DMZ zone to X1 in WAN DHCP mode successful
class TestVLAN_TC06(Test):
    uuid = "SOSAIOT-TC-57313"
    description = show_testcase_info(
        Parameter.TESTPLAN, '6', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_WAN_zone(self):
        tag = False
        x1_static_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'dhcp',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        getres = interfacev4api.get_interface_status(name='X1')
        if 'dhcp' in str(getres):
            logger.info('X1 mode already dhcp, dont need edit.')
        else:
            res = interfacev4api.config_interface(**x1_static_dict)
            time.sleep(10)
            if res is False:
                tag = True
        Assertion.assert_equal(
            tag, False, "ERR: Config X1 to DHCP WAN Zone failed")

    def test_02_add_VLAN_subinterface_to_X4(self):
        vlan_list = [1231, 1233, 1235]
        x1_lan_dict = {
            'if': 'x1',
            'type': 'vlan',
            'vlan_tag': vlan_list[0],
            'zone': 'lan',
            'mode': 'static',
            'ip': '12.13.12.10',
        }
        x1_dmz_dict = {
            'if': 'x1',
            'type': 'vlan',
            'vlan_tag': vlan_list[1],
            'zone': 'dmz',
            'mode': 'static',
            'ip': '12.14.12.10',
        }
        x1_wan_dict = {
            'if': 'X1',
            'type': 'vlan',
            'vlan_tag': vlan_list[2],
            'zone': 'wan',
            'mode': 'static',
            'ip': '12.12.12.10',
            'netmask': '255.255.255.0',
            'gateway': '12.12.4.1',
            'dns1': '4.4.4.4',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        x1_vlan_dict = {
            'if': 'x1',
            'type': 'vlan',
            'vlan_tag': '',
        }

        res1 = interfacev4api.add_interface(**x1_lan_dict)
        if res1:
            x1_vlan_dict['vlan_tag'] = str(vlan_list[0])
            interfacev4api.del_interface(**x1_vlan_dict)
        res2 = interfacev4api.add_interface(**x1_dmz_dict)
        if res2:
            x1_vlan_dict['vlan_tag'] = str(vlan_list[1])
            interfacev4api.del_interface(**x1_vlan_dict)
        res3 = interfacev4api.add_interface(**x1_wan_dict)
        if res3:
            x1_vlan_dict['vlan_tag'] = str(vlan_list[2])
            interfacev4api.del_interface(**x1_vlan_dict)
        Assertion.assert_equal(
            res1 & res2 & res3, True, "ERR: Add VLAN interfaces to X1 failed")


# Expected: PC2 can login to X4 VLAN1 successful
class TestVLAN_TC26(Test):
    uuid = "SOSAIOT-TC-57279"
    description = show_testcase_info(
        Parameter.TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_VLAN_subinterface_to_X4(self):
        rc1 = interfacev4api.add_interface(**x4_vlan1_dict)
        Assertion.assert_equal(
            rc1, True, "ERR: Add Vlan interfaces to X4 failed")

    @repeat_method(3)
    def test_02_verify_VLAN_subinterface_PC_management_DUT(self):
        fw.api_logout()
        command = 'python3 ' + scripts_path + 'LoginDUTFromVLANInterface.py -i ' + \
            Parameter.X4_VLAN1_IP + ' -a login'
        res = PC2_login.send_command(command)
        logger.info(f'run login dut script result: {res}')
        result = True if re.search('Successfully login', res) else False
        Assertion.assert_equal(
            result, True, "ERR: Login DUT from vlan subinterface failed")


# Expected: X3 host PC1 ping to X4 VLAN1 host successful
class TestVLAN_TC37(Test):
    uuid = "SOSAIOT-TC-57290"
    description = show_testcase_info(
        Parameter.TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X3_and_PC(self):
        x3_static_dict = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        res = interfacev4api.config_interface(**x3_static_dict)
        os.system(
            f'route add -net {Parameter.X4_VLAN1_SUB} netmask {Parameter.MASK} gw {Parameter.X3_IP}')
        PC2_login.send_command(
            f'route add -host {PC1_ETH2_IP} gw {Parameter.X4_VLAN1_IP}')
        Assertion.assert_equal(
            res, True, "ERR: Config X3 to static LAN Zone failed")

    @repeat_method(3)
    def test_02_verify_traffic_from_X3_to_X4_sub_interface(self):
        res = PC1_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth2')
        Assertion.assert_equal(
            res, True, "ERR: Traffic from X3 host to X4 sub interface host failed")

    def test_03_init_pc_route(self):
        os.system(
            f'route del -net {Parameter.X4_VLAN1_SUB} netmask {Parameter.MASK} gw {Parameter.X3_IP}')
        PC2_login.send_command(
            f'route del -host {PC1_ETH2_IP} gw {Parameter.X4_VLAN1_IP}')
        Assertion.assert_equal(True, True, "ERR: init pc route failed")

# Expected: ping successful form VLAN1 to VLAN2 in X4
class TestVLAN_TC39(Test):
    uuid = "SOSAIOT-TC-57292"
    description = show_testcase_info(
        Parameter.TESTPLAN, '39', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_VLAN_and_conf_PC(self):
        x4_vlan2_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN2_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN2_IP,
        }
        rc1 = interfacev4api.add_interface(**x4_vlan2_dict)

        PC2_login.send_command(
            f'route add -host {PC4_ETH1_IP} gw {Parameter.X4_VLAN1_IP}')
        PC4_login.send_command(
            f'route add -host {PC2_ETH1_IP} gw {Parameter.X4_VLAN2_IP}')
        Assertion.assert_equal(
            rc1, True, "ERR: Add Vlan interfaces to X4 failed")

    @repeat_method(3)
    def test_02_verify_traffic_from_X4_sub_interface1_to_X4_sub_interface2(self):
        res = PC4_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth2')
        Assertion.assert_equal(res, True, 'ERR: ping from vlan1 to vlan2 failed')

    def test_03_init_pc_route(self):
        PC2_login.send_command(
            f'route del -host {PC4_ETH1_IP} gw {Parameter.X4_VLAN1_IP}')
        PC4_login.send_command(
            f'route del -host {PC2_ETH1_IP} gw {Parameter.X4_VLAN2_IP}')
        Assertion.assert_equal(True, True, "ERR: init pc route failed")


# Expected: PC2 ping to X4 VLAN1 successful
class TestVLAN_TC10(Test):
    uuid = "SOSAIOT-TC-57263"
    description = show_testcase_info(
        Parameter.TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_VLAN1_subinterface_to_X4(self):
        tag = False
        getres = interfacev4api.get_vlan_interface_status(name='X4', vlan_id=str(X4_VLAN1_ID))
        logger.info(f'check vlan1 interface result: {getres}')
        if Parameter.X4_VLAN1_IP in str(getres):
            logger.info('vlan1 interface exist, dont need add.')
        else:
            addres = interfacev4api.add_interface(**x4_vlan1_dict)
            if addres is False:
                tag = True
        Assertion.assert_equal(
            tag, False, "ERR: Add Vlan1 interfaces to X4 failed")

    @repeat_method(3)
    def test_01_verify_VLAN_ping(self):
        command = f'ping {Parameter.X4_VLAN1_IP} -c 5'
        res = PC2_login.send_command(command)
        logger.info(f'PC2 command result: {res}')
        result = True if '100% packet loss' not in res else False
        Assertion.assert_equal(
            result, True, "ERR: ping DUT from vlan subinterface failed")


# Expected: PC2 ping to X4 VLAN1 successful while add static arp
class TestVLAN_TC42(Test):
    uuid = "SOSAIOT-TC-57296"
    description = show_testcase_info(
        Parameter.TESTPLAN, '42', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '42')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_static_arp_for_PC2(self):
        # check X4 vlan interface
        TestVLAN_TC10().test_01_add_VLAN1_subinterface_to_X4()

        tag = False
        # send cmd can get eth2 MAC from PC2
        # command = 'ifconfig eth1 | grep HWaddr'
        command = 'ip link show eth1 | grep "link/ether"'
        sendres = PC2_login.send_command(command)
        if sendres:
            macres = re.search('([0-9a-fA-F]{2}\\:){5}[0-9a-fA-F]{2}', sendres).group()
            if macres:
                arp_dict['mac'] = macres
                addres = arpapi.add_static_arp(**arp_dict)
                if addres:
                    arpcaches = arpapi.show_arp_caches()
                    for cache in arpcaches:
                        if cache['ip_address'] == PC2_ETH1_IP and cache['timeout'] == 'Permanent ':
                            tag = True
                else:
                    logger.info('add static arp fail')
        else:
            logger.info('can not get mac form PC2 eth1')
        Assertion.assert_equal(
            tag, True, "ERR: add static arp form fw using PC2 eth1 mac failed")

    @repeat_method(3)
    def test_03_verify_VLAN_ping(self):
        command = f'ping {Parameter.X4_VLAN1_IP} -c 5'
        res = PC2_login.send_command(command)
        logger.info(f'PC2 command result: {res}')
        result = True if '100% packet loss' not in res else False
        Assertion.assert_equal(
            result, True, "ERR: ping DUT from vlan subinterface failed")

    def test_04_delete_static_arp_entry(self):
        # init static arp entry
        arp_dict['mac'] = arp_dict['mac'].replace(':', '')
        arpapi.del_static_arp(**arp_dict)
        Assertion.assert_equal(
            True, True, "ERR: delete static arp entry failed")


# Expected: PC5 ping to X1 ip will forward to X4 vlan1's host PC2 via NAT policy
class TestVLAN_TC46(Test):
    uuid = "SOSAIOT-TC-57300"
    description = show_testcase_info(
        Parameter.TESTPLAN, '46', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '46')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1(self):
        x1_wan_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': False,
        }
        res = interfacev4api.config_interface(**x1_wan_dict)
        # check X4 vlan interface
        TestVLAN_TC10().test_01_add_VLAN1_subinterface_to_X4()
        Assertion.assert_equal(
            res, True, "ERR: edit X1 interface failed")

    def test_01_add_nat_policy_and_access_rule(self):
        nat_ao_dict = {
            "object_type": "host",
            "name": PC2_ETH1_IP,
            "zone": "LAN",
            "value": PC2_ETH1_IP
        }
        nat_ipv4_dict = {
            "nat_policies": [
                {
                    "ipv4": {
                        "comment": 'autoadd01',
                        "destination": {
                            "name": 'X1 IP'
                        },
                        "enable": True,
                        "inbound": "X1",
                        "name": "AutoAddRule",
                        "outbound": "any",
                        "service": {
                            "group": "ICMP"
                        },
                        "translated_destination": {
                            "name": PC2_ETH1_IP
                        },
                        "source": {
                            "any": True
                        }
                    }
                }
            ]
        }
        access_rule_dict = {
            'name': 'AutoNatWANToLANTest01',
            'from': 'WAN',
            'to': 'LAN',
            'source_addr': {'name': 'X1 Subnet'},
            'dst_addr': {'any': True},
            'service': {'any': True},
            'action': 'allow',
        }
        res = aoapi.config_addressobject(**nat_ao_dict)
        logger.info(res)
        addv4res = natpolicyconfapi.add_nat_policy(**nat_ipv4_dict)
        logger.info(addv4res)
        time.sleep(5)

        addaclres = accessruleapi.add_ipv4_access_rule(**access_rule_dict)
        logger.info(addaclres)
        Assertion.assert_equal(addv4res & addaclres, True, "ERR: add nat policy failed")

    @repeat_method(3)
    def test_02_verify_traffic_from_wan_to_X4_sub_interface1(self):
        PC2_login.send_command(
            f'route add -host {PC5_ETH1_IP} gw {Parameter.X4_VLAN1_IP}')
        time.sleep(5)
        res = PC5_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        Assertion.assert_equal(res, True, 'ERR: ping from WAN to LAN failed')

    def test_03_init_pc_route(self):
        PC2_login.send_command(
            f'route del -host {PC5_ETH1_IP} gw {Parameter.X4_VLAN1_IP}')
        Assertion.assert_equal(True, True, "ERR: init pc route failed")


# Expected: PC5 ping to PC2 successful via VPN tunnel
class TestVLAN_TC65(Test):
    uuid = "SOSAIOT-TC-57318"
    description = show_testcase_info(
        Parameter.TESTPLAN, '65', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '65')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_route_to_pc2_and_pc3(self):
        command1 = f'route add -net {Parameter.X0_REMOTE_SUB}/24 gw {Parameter.X4_VLAN1_IP}'
        PC2_login.send_command(command1)
        command2 = f'route add -net {Parameter.X4_VLAN1_SUB}/24 gw {Parameter.X0_REMOTE_IP}'
        PC3_login.send_command(command2)
        Assertion.assert_equal(True, True, "ERR: add route to pc2 and pc3 failed")

    @repeat_method(3)
    def test_02_ping_from_remote_sub_to_local_sub(self):
        time.sleep(10)
        command = f'ping {PC2_ETH1_IP} -c 5'
        res = PC3_login.send_command(command)
        logger.info(f'PC3 command result: {res}')
        result = True if '100% packet loss' not in res else False
        Assertion.assert_equal(
            result, True, "ERR: ping from remote X0 host to local X4:1 host failed")

    def test_03_init_pc_route(self):
        command1 = f'route del -net {Parameter.X0_REMOTE_SUB}/24 gw {Parameter.X4_VLAN1_IP}'
        PC2_login.send_command(command1)
        command2 = f'route del -net {Parameter.X4_VLAN1_SUB}/24 gw {Parameter.X0_REMOTE_IP}'
        PC3_login.send_command(command2)
        Assertion.assert_equal(True, True, "ERR: init pc route failed")
