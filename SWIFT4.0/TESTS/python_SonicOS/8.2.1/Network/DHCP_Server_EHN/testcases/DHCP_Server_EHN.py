from definition.settings import *
from definition.utils import *


# Expect: enable dhcp server
class TestDHCPServer_TC01(Test):
    uuid = "SOSAIOT-TC-55865"
    description = show_testcase_info(TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_dhcp_server(self):
        dhcp_server_settings = {
            "dhcp_server": {
                "ipv4": {
                    "enable": False
                }
            }
        }
        res = dhcpserverapi.config_dhcp_server_settings(**dhcp_server_settings)
        Assertion.assert_equal(res, True, 'ERR: disable dhcp server failed')

    def test_02_enable_dhcp_server_option(self):
        dhcp_server_settings = {
            "dhcp_server": {
                "ipv4": {
                    "enable": True
                }
            }
        }
        res = dhcpserverapi.config_dhcp_server_settings(**dhcp_server_settings)
        Assertion.assert_equal(res, True, 'ERR: enable dhcp server failed')


# Expect: dhcp server scope with Vaild Domain Value
class TestDHCPServer_TC10(Test):
    uuid = "SOSAIOT-TC-55866"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x1(self):
        x1_static = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS_1,
            'dns2': Parameter.X1_DNS_2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        res = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(res, True, 'ERR: config x1 failed')

    def test_02_test_max_number_and_specail_character_for_dns(self):
        res = False
        x2_dhcp_scope = copy.deepcopy(dynamic_scope_base)
        x2_dhcp_scope["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc10_x2_dhcp_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(**x2_dhcp_scope)
        if addres:
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            res = True if tc10_x2_dhcp_dict['comment'] in str(
                output) else False
        else:
            logger.info('add dhcp lease for x2 interface failed')
        Assertion.assert_equal(
            res, True, "ERR: test max number and special character for dhcp scope dns failed")

    def test_03_check_client_domain_with_maximum(self):
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        res, ipaddr = pc_get_ip_lease(pc2_login, 'eth2')
        logger.info('check client domain info....')
        output = pc2_login.send_command(f'cat {DHCLIEN_LEASE_FILE}')
        res &= True if tc10_x2_dhcp_dict['domain_name'] in output else False
        Assertion.assert_equal(
            res, True, "ERR: check client domain with maximun cases info failed")

    def test_04_test_domain_including_upper_cases(self):
        edit_dict = copy.deepcopy(dynamic_scope_base)
        edit_dict["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc10_edit_dict1)
        editres = dhcpserverapi.edit_dhcp_server_scope_v4(scope='dynamic',
            p1=tc10_x2_dhcp_dict['from'], p2=tc10_x2_dhcp_dict['to'], **edit_dict)
        if editres:
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            res = True if tc10_edit_dict1['comment'] in str(output) else False
        else:
            logger.info('edit dhcp lease for x2 interface failed')
            res = False
        Assertion.assert_equal(
            res, True, "ERR: test domain including upper cases for dhcp scope dns failed")

    def test_05_check_client_domain_with_upper_cases(self):
        res = pc_release_ip(pc2_login, 'eth2')
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        res &= pc_get_ip_lease(pc2_login, 'eth2')[0]
        out = pc2_login.send_command(f'cat {DHCLIEN_LEASE_FILE}')
        res &= True if tc10_edit_dict1['domain_name'] in out else False
        Assertion.assert_equal(
            res, True, "ERR: check client domain with upper cases info failed")

    def test_06_domain_with_multiple_level(self):
        res = False
        edit_dict = copy.deepcopy(dynamic_scope_base)
        edit_dict["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc10_edit_dict2)
        editres = dhcpserverapi.edit_dhcp_server_scope_v4(scope='dynamic',
            p1=tc10_edit_dict1['from'], p2=tc10_edit_dict1['to'], **edit_dict)
        if editres:
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            res = True if tc10_edit_dict2['comment'] in str(output) else False
        else:
            logger.info('edit dhcp lease for x2 interface failed')
        Assertion.assert_equal(
            res, True, "ERR: test domain including upper cases for dhcp scope dns failed")

    def test_07_check_client_domain_with_multiple_level(self):
        res = pc_release_ip(pc2_login, 'eth2')
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        res &= pc_get_ip_lease(pc2_login, 'eth2')[0]
        out = pc2_login.send_command(f'cat {DHCLIEN_LEASE_FILE}')
        res &= True if tc10_edit_dict2['domain_name'] in out else False
        Assertion.assert_equal(
            res, True, "ERR: check client domain with multiple level info failed")

    def test_08_init_test_env(self):
        pc2_login.send_command('ifdown eth2; timeout 5 ifup eth2')
        res = dhcpserverapi.delete_dhcp_server_scope_v4(
            scope='dynamic', p1=tc10_edit_dict2['from'], p2=tc10_edit_dict2['to'])
        logger.info(res)
        Assertion.assert_equal(
            True, True, "ERR: restore test environment failed")


# Expect: check client dns info when DUT is DNS Inherit Setting Option For Dynamic Entry
# this case configuration including TC14, TC19, TC21, TC97, TC25
class TestDHCPServer_TC14(Test):
    uuid = "SOSAIOT-TC-55867"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dhcp_lease_scope_for_x2(self):
        res = False
        dynamic_scope_case14 = copy.deepcopy(dynamic_scope_base)
        dynamic_scope_case14["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc14_dynamic_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
            **dynamic_scope_case14)
        if addres:
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            res = True if tc14_dynamic_dict["comment"] in str(
                output) else False
        Assertion.assert_equal(res, True, 'ERR: add dhcp lease for x2 failed')

    def test_02_pc2_get_dhcp_lease(self):
        pc2_login.send_command('cp /dev/null /etc/resolv.conf')
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        (res, ip_addr) = pc_get_ip_lease(pc2_login, 'eth2')
        CaseParams.tc14_res = res
        CaseParams.tc14_pc2_ip = ip_addr
        Assertion.assert_equal(
            res, True, 'ERR: PC2 get dhcp lease from DUT failed')

    def test_03_check_dhcp_client_dns_info(self):
        logger.info('check client dns info...')
        output = pc2_login.send_command(
            'cat /etc/resolv.conf | grep nameserver')
        res = True if Parameter.X1_DNS_1 in output and Parameter.X1_DNS_2 in output else False
        Assertion.assert_equal(
            res, True, 'ERR: dhcp client dns info does not match DUT')


# Expect: client get IP lease successfully
class TestDHCPServer_TC19(Test):
    uuid = "SOSAIOT-TC-55872"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_client_get_dynamic_ip(self):
        res = CaseParams.tc14_res
        Assertion.assert_equal(
            res, True, "ERR: Client gets the specific IP lease failed.")


# Expect: client get correct Domain Name info
class TestDHCPServer_TC21(Test):
    uuid = "SOSAIOT-TC-55874"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_client_Domain_name_info(self):
        output = pc2_login.send_command(f'cat {DHCLIEN_LEASE_FILE}')
        res = True if tc14_dynamic_dict['domain_name'] in output else False
        Assertion.assert_equal(
            res, True, 'ERR: verify client can get corret Domain Name info from DUT failed')


# Expect: current DHCP leases table display correct info
class TestDHCPServer_TC97(Test):
    uuid = "SOSAIOT-TC-55912"
    description = show_testcase_info(TESTPLAN, '97', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '97')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_curent_dhcp_lease_table(self):
        output = dhcpserverapi.get_dhcp_server_leases()
        res = True if CaseParams.tc14_pc2_ip in str(output) else False
        Assertion.assert_equal(
            res, True, 'ERR: check current lease table failed')


# Expect: dhcp dynamic client get correct lease time
class TestDHCPServer_TC25(Test):
    uuid = "SOSAIOT-TC-55878"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verfiy_client_lease_time(self):
        lease_time_on_client = 0
        try:
            out = pc2_login.send_command(
                "cat /var/lib/dhclient/dhclient.leases | grep dhcp-lease-time | awk '{print$3}'")
            logger.info(out)
            lease_time_on_client = int(out.strip()[:-1])
        except BaseException as e:
            logger.error(repr(e))

        logger.info('lease time on client is {}s'.format(lease_time_on_client))
        lease_time_on_server = dynamic_scope_base["dhcp_server"]["ipv4"]["scope"]["dynamic"][0]["lease_time"]*60
        logger.info('lease time on server is {}s'.format(lease_time_on_server))
        res = True if lease_time_on_client == lease_time_on_server else False
        Assertion.assert_equal(
            res, True, "ERR: verify dynamic client get correct lease time failed")

    def test_02_init_test_env(self):
        pc2_login.send_command('ifdown eth2; timeout 5 ifup eth2')
        res = dhcpserverapi.delete_dhcp_server_scope_v4(
            scope='dynamic', p1=tc14_dynamic_dict['from'], p2=tc14_dynamic_dict['to'])
        logger.info(f'init test env result: {res}')
        Assertion.assert_equal(
            True, True, "ERR: restore test environment failed")


# Expect: test dns manual settings of dhcp static entry
# this case configuration including TC16, TC18, TC20, TC26
class TestDHCPServer_TC16(Test):
    uuid = "SOSAIOT-TC-55869"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_static_dhcp_lease_scope_for_x3(self):
        # tc16_static_dict.update({'mac': CaseParams.pc3_eth1_mac})
        tc16_static_dict.update({'mac': get_pc_eth_mac(pc3_login, 'eth1')})
        static_lease_case16 = copy.deepcopy(static_scope_base)
        static_lease_case16["dhcp_server"]['ipv4']["scope"]['static'][0].update(
            **tc16_static_dict)
        res = dhcpserverapi.add_dhcp_server_scope_static(**static_lease_case16)
        CaseParams.tc16_res1 = res
        Assertion.assert_equal(
            res, True, 'ERR: add dhcp static lease for x3 failed')

    def test_02_pc3_get_dhcp_static_lease_and_check_dns_info(self):
        pc3_login.send_command('cp /dev/null /etc/resolv.conf')
        pc3_login.send_command(
            f'cp /dev/null {DHCLIEN_LEASE_FILE}')
        logger.info('pc3 get dhcp static lease')
        res, ip_addr = pc_get_ip_lease(pc3_login, 'eth1')
        CaseParams.tc16_res2 = res
        output = pc3_login.send_command(
            'cat /etc/resolv.conf | grep nameserver')
        if tc16_static_dict['dns']['server']['static']['primary'] in output:
            if tc16_static_dict['dns']['server']['static']['secondary'] in output:
                res &= True
        Assertion.assert_equal(
            res, True, 'ERR: test dns manual settings for static entry failed')


# Expect: able to add static lease scope
class TestDHCPServer_TC18(Test):
    uuid = "SOSAIOT-TC-55871"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_can_add_static_lease(self):
        res = CaseParams.tc16_res1
        Assertion.assert_equal(
            res, True, 'ERR: failed to add static lease scope')


# Expect: dhcp client able to get static ip lease
class TestDHCPServer_TC20(Test):
    uuid = "SOSAIOT-TC-55873"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_get_static_lease(self):
        res = CaseParams.tc16_res2
        Assertion.assert_equal(
            res, True, 'ERR: client failed to get static ip lease from DUT')


# Expect: dhcp static client get correct lease time
class TestDHCPServer_TC26(Test):
    uuid = "SOSAIOT-TC-55879"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verfiy_client_lease_time(self):
        lease_time_on_client = 0
        try:
            out = pc3_login.send_command(
                "cat /var/lib/dhclient/dhclient.leases | grep dhcp-lease-time | awk '{print$3}'")
            logger.info(out)
            lease_time_on_client = int(out.strip()[:-1])
        except BaseException as e:
            logger.error(repr(e))
        logger.info('expire_time on client is {}s'.format(
            lease_time_on_client))
        lease_time_on_server = tc16_static_dict["lease_time"]*60
        logger.info('expire_time on server is {}s'.format(
            lease_time_on_server))
        res = True if lease_time_on_client == lease_time_on_server else False
        Assertion.assert_equal(
            res, True, "ERR: verify dhcp static client lease time failed")

    def test_02_init_test_env(self):
        pc3_login.send_command('ifdown eth1; timeout 5 ifup eth1')
        res = dhcpserverapi.delete_dhcp_server_scope_v4(
            'static', tc16_static_dict['ip'], tc16_static_dict['mac'])
        logger.info(f'init test env result: {res}')
        Assertion.assert_equal(
            True, True, "ERR: restore test environment failed")


# Expect: dhcp leases recycling
class TestDHCPServer_TC27(Test):
    uuid = "SOSAIOT-TC-55880"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dynamic_range(self):
        res = False
        dynamic_scope_case27 = copy.deepcopy(dynamic_scope_base)
        dynamic_scope_case27["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc27_dynamic_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
            **dynamic_scope_case27)
        if addres:
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            res = True if tc27_dynamic_dict["comment"] in str(
                output) else False
        Assertion.assert_equal(res, True, 'ERR: add dhcp lease for x2 failed')

    def test_02_test_dhcp_address_recycling(self):
        res = []
        dhclients = {pc2_login: 'eth2', pc4_login: 'eth1'}
        for client in dhclients:
            getres, ip_addr = pc_get_ip_lease(client, dhclients[client])
            if ip_addr:
                logger.info(f'pc get ip address: {ip_addr}')
            res.append(getres)
        logger.info('pc4 eth1 do release....')
        release_res = pc_release_ip(pc4_login, 'eth1')
        if release_res:
            logger.info('pc5 eth1 get ip....')
            pc5_getres, pc5_eth1_ip = pc_get_ip_lease(pc5_login, 'eth1')
            logger.info('pc5 eth1 ip address is {}'.format(pc5_eth1_ip))
            res.append(pc5_getres)
            pc5_getres = True if pc5_eth1_ip == tc27_dynamic_dict[
                'from'] or pc5_eth1_ip == tc27_dynamic_dict['to'] else False
            res.append(pc5_getres)
        else:
            res.append(release_res)
        Assertion.assert_equal(all(res),
                               True, 'ERR: test dhcp leases recycling failed')

    def test_03_init_test_env(self):
        pc2_login.send_command('ifdown eth2 ; timeout 5 ifup eth2')
        pc4_login.send_command('ifdown eth1 ; timeout 5 ifup eth1')
        pc5_login.send_command('ifdown eth1 ; timeout 5 ifup eth1')
        res = dhcpserverapi.delete_dhcp_server_scope_v4(
            scope='dynamic', p1=tc27_dynamic_dict['from'], p2=tc27_dynamic_dict['to'])
        logger.info(f'init test env result: {res}')
        Assertion.assert_equal(
            True, True, "ERR: restore test environment failed")


# Expect: multiple dhcp dynamic client on signal interface
class TestDHCPServer_TC30(Test):
    uuid = "SOSAIOT-TC-55884"
    description = show_testcase_info(TESTPLAN, '30', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dynamic_range_for_x2(self):
        res = False
        dynamic_scope_case30 = copy.deepcopy(dynamic_scope_base)
        dynamic_scope_case30["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc30_dynamic_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
            **dynamic_scope_case30)
        if addres:
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            res = True if tc30_dynamic_dict["comment"] in str(
                output) else False
        Assertion.assert_equal(res, True, 'ERR: add dhcp lease for x2 failed')

    def test_02_verify_multiple_dynamic_entries(self):
        res = []
        dhclients = {pc2_login: 'eth2', pc4_login: 'eth1'}
        for client in dhclients:
            getres, ip_addr = pc_get_ip_lease(client, dhclients[client])
            if ip_addr:
                logger.info(f'get ip address: {ip_addr}')
            res.append(getres)
        Assertion.assert_equal(
            all(res), True, 'ERR: verify multiple dynamic entries on signal interface failed')

    def test_03_init_test_env(self):
        pc2_login.send_command('ifdown eth2 ; timeout 5 ifup eth2')
        pc4_login.send_command('ifdown eth1 ; timeout 5 ifup eth1')
        res = dhcpserverapi.delete_dhcp_server_scope_v4(
            scope='dynamic', p1=tc30_dynamic_dict['from'], p2=tc30_dynamic_dict['to'])
        logger.info(f'init test env result: {res}')
        Assertion.assert_equal(
            True, True, "ERR: restore test environment failed")


# Expect: DUT update settings can ack when client request ip at half of lease time
class TestDHCPServer_TC28(Test):
    uuid = "SOSAIOT-TC-55881"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_client_get_ip_lease(self):
        dynamic_scope_case28 = copy.deepcopy(dynamic_scope_base)
        dynamic_scope_case28["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc28_dynamic_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
            **dynamic_scope_case28)
        if addres:
            res, ip_addr = pc_get_ip_lease(pc3_login, 'eth1')
            CaseParams.tc28_pc3_eth1_ip = ip_addr
        else:
            logger.error('add dhcp lease scope for x3 failed')
            res = False
        Assertion.assert_equal(res, True, 'ERR: client get ip lease failed')

    def test_02_config_packet_monitor(self):
        packetapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'ip_types': 'udp',
                'destination_ports': '67,68'
            }
        }
        res = packetapi.conf_packmon(monitor_conf_dict)[0]
        Assertion.assert_equal(res, True, 'ERR: config packet monitor failed')

    def test_03_test_dhcp_ack_packets(self):
        packetapi.clear_packets()
        startres = packetapi.start_capture()
        logger.info(f'start packet monitor result: {startres}')
        time.sleep(120)
        stopres = packetapi.stop_capture()
        logger.info(f'stop packet monitor result: {stopres}')
        outputs = packetapi.export_captured_packets()
        res, packet = check_dhcp_ack_packet(
            outputs, tc28_dynamic_dict["default_gateway"], CaseParams.tc28_pc3_eth1_ip, "X3")
        logger.info(packet)
        Assertion.assert_equal(
            res, True, 'ERR: test DUT send ACK packets failed')

    def test_04_init_env(self):
        pc3_login.send_command('ifdown eth1; timeout 5 ifup eth1')
        res = dhcpserverapi.delete_dhcp_server_scope_v4(
            scope='dynamic', p1=tc28_dynamic_dict['from'], p2=tc28_dynamic_dict['to'])
        logger.info(f'init test env result: {res}')
        Assertion.assert_equal(True, True, 'ERR: init test env failed')


# Expect: Multiple dhcp static client on signal interface
# this case configuration including TC29, TC32
class TestDHCPServer_TC29(Test):
    uuid = "SOSAIOT-TC-55882"
    description = show_testcase_info(TESTPLAN, '29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_multiple_static_entries(self):
        tc29_static_dict1.update({'mac': get_pc_eth_mac(pc2_login, 'eth2')})
        tc29_static_dict2.update({'mac': get_pc_eth_mac(pc4_login, 'eth1')})

        res = []
        scopes = [tc29_static_dict1, tc29_static_dict2]
        for scope in scopes:
            static_scope = copy.deepcopy(static_scope_base)
            static_scope["dhcp_server"]["ipv4"]["scope"]["static"][0].update(
                scope)
            addres = dhcpserverapi.add_dhcp_server_scope_static(**static_scope)
            res.append(addres)
        Assertion.assert_equal(
            all(res), True, 'ERR: add static entries on signal failed')

    def test_02_test_multi_clients_on_signal_interface(self):
        dhclients = {pc2_login: 'eth2', pc4_login: 'eth1'}
        res = []
        for client in dhclients:
            getres, ip_addr = pc_get_ip_lease(client, dhclients[client])
            res.append(getres)
        Assertion.assert_equal(
            all(res), True, 'ERR: test multiple static entries on signal failed')


# Expect: able to delete multiple static entries
class TestDHCPServer_TC32(Test):
    uuid = "SOSAIOT-TC-55886"
    description = show_testcase_info(TESTPLAN, '32', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_multiple_static_entries(self):
        res = []
        del_scopes = [tc29_static_dict1, tc29_static_dict2]
        for scope in del_scopes:
            delres = dhcpserverapi.delete_dhcp_server_scope_v4(
                'static', scope['ip'], scope['mac'])
            res.append(delres)
        if all(res):
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            if tc29_static_dict1['comment'] not in output and tc29_static_dict2['comment'] not in output:
                res.append(True)
            else:
                res.append(False)
        Assertion.assert_equal(
            all(res), True, "ERR: delete multiple static entries failed")

    def test_02_init_test_env(self):
        pc2_login.send_command('ifdown eth2; timeout 5 ifup eth2')
        pc4_login.send_command('ifdown eth1; timeout 5 ifup eth1')


# Expect: able to delete multiple dynamic entries
class TestDHCPServer_TC34(Test):
    uuid = "SOSAIOT-TC-55888"
    description = show_testcase_info(TESTPLAN, '34', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_multiple_dynamic_entries(self):
        scopes = [tc34_dynamic_dict1, tc34_dynamic_dict2]
        res = []
        for scope in scopes:
            dynamic_scope = copy.deepcopy(dynamic_scope_base)
            dynamic_scope["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
                scope)
            addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
                **dynamic_scope)
            res.append(addres)
        Assertion.assert_equal(
            all(res), True, 'ERR: add multiple dynamic entries failed')

    def test_02_delete_multiple_dynamic_entries(self):
        res = []
        del_scopes = [tc34_dynamic_dict1, tc34_dynamic_dict2]
        for scope in del_scopes:
            delres = dhcpserverapi.delete_dhcp_server_scope_v4(
                'dynamic', scope['from'], scope['to'])
            res.append(delres)
        if all(res):
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            if tc34_dynamic_dict1['comment'] not in output and tc34_dynamic_dict2['comment'] not in output:
                res.append(True)
            else:
                res.append(False)
        Assertion.assert_equal(
            all(res), True, 'delete multiple dynamic entries failed')


# Expect: multiple interface with dynamic lease
class TestDHCPServer_TC35(Test):
    uuid = "SOSAIOT-TC-55889"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dynamic_ranges(self):
        scopes = [tc35_dynamic_dict1, tc35_dynamic_dict2]
        res = []
        for scope in scopes:
            dynamic_scope = copy.deepcopy(dynamic_scope_base)
            dynamic_scope["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
                scope)
            addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
                **dynamic_scope)
            res.append(addres)
        Assertion.assert_equal(
            all(res), True, 'ERR: add multiple dynamic entries failed')

    def test_02_test_multi_clients_with_multi_interfaces(self):
        res = []
        dhclients = {pc2_login: 'eth2', pc3_login: 'eth1'}
        for client in dhclients:
            getres, ip_addr = pc_get_ip_lease(client, dhclients[client])
            res.append(getres)
        Assertion.assert_equal(
            all(res), True, 'test multiple interface with dynamic lease failed')

    def test_03_init_test_env(self):
        pc2_login.send_command('ifdown eth2; timeout 5 ifup eth2')
        pc3_login.send_command('ifdown eth1; timeout 5 ifup eth1')
        res = []
        del_scopes = [tc35_dynamic_dict1, tc35_dynamic_dict2]
        for scope in del_scopes:
            del_res = dhcpserverapi.delete_dhcp_server_scope_v4(
                'dynamic', scope['from'], scope['to'])
            res.append(del_res)
        logger.info(f'init test env result: {all(res)}')
        Assertion.assert_equal(True, True, 'restore test env failed')


# Expect: multiple interface with static lease
class TestDHCPServer_TC36(Test):
    uuid = "SOSAIOT-TC-55890"
    description = show_testcase_info(TESTPLAN, '36', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_static_scopes(self):
        res = []
        tc36_static_dict1.update({'mac': get_pc_eth_mac(pc2_login, 'eth2')})
        tc36_static_dict2.update({'mac': get_pc_eth_mac(pc4_login, 'eth1')})

        scopes = [tc36_static_dict1, tc36_static_dict2]
        for scope in scopes:
            static_range = copy.deepcopy(static_scope_base)
            static_range["dhcp_server"]["ipv4"]["scope"]["static"][0].update(
                scope)
            addres = dhcpserverapi.add_dhcp_server_scope_static(**static_range)
            res.append(addres)
        Assertion.assert_equal(all(res), True, 'add static lease scope failed')

    def test_01_test_on_multiple_interface(self):
        res = []
        dhclients = {pc2_login: 'eth2', pc4_login: 'eth1'}
        for client in dhclients:
            getres, ip_addr = pc_get_ip_lease(client, dhclients[client])
            res.append(getres)
        Assertion.assert_equal(
            all(res), True, 'test multiple interface with static lease failed')

    def test_02_init_test_env(self):
        pc2_login.send_command('ifdown eth2 down; timeout 5 ifup eth2 up')
        pc4_login.send_command('ifdown eth1 down; timeout 5 ifup eth1 up')
        res = []
        del_scopes = [tc36_static_dict1, tc36_static_dict2]
        for scope in del_scopes:
            del_res = dhcpserverapi.delete_dhcp_server_scope_v4(
                'static', scope['ip'], scope['mac'])
            res.append(del_res)
        logger.info(f'init test env result: {all(res)}')
        Assertion.assert_equal(True, True, 'restore test env failed')


# Expect: combination settings function
class TestDHCPServer_TC37(Test):
    uuid = "SOSAIOT-TC-55891"
    description = show_testcase_info(TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_configure_combination_settings(self):
        res = []
        tc37_static_dict1.update({'mac': get_pc_eth_mac(pc4_login, 'eth1')})
        tc37_static_dict2.update({'mac': get_pc_eth_mac(pc5_login, 'eth1')})

        scopes = [tc37_dynamic_dict1, tc37_dynamic_dict2,
                  tc37_static_dict1, tc37_static_dict2]
        for scope in scopes:
            if 'dynamic' in str(scope):
                dynamic_scope = copy.deepcopy(dynamic_scope_base)
                dynamic_scope["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
                    scope)
                addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
                    **dynamic_scope)
            else:
                static_scope = copy.deepcopy(static_scope_base)
                static_scope["dhcp_server"]["ipv4"]["scope"]["static"][0].update(
                    scope)
                addres = dhcpserverapi.add_dhcp_server_scope_static(
                    **static_scope)
            res.append(addres)
        Assertion.assert_equal(
            all(res), True, 'configure combination settings failed')
    
    @repeat_method(3)
    def test_02_combination_settings_function(self):
        res = []
        dhclients = {pc2_login: 'eth2', pc3_login: 'eth1',
                     pc4_login: 'eth1', pc5_login: 'eth1'}
        for client in dhclients:
            getres, ip_addr = pc_get_ip_lease(client, dhclients[client])
            res.append(getres)
        Assertion.assert_equal(
            all(res), True, 'test combination settings function failed')

    def test_03_init_test_env(self):
        pc2_login.send_command('ifdown eth2 down; timeout 3 ifup eth2 up')
        pc3_login.send_command('ifdown eth1 down; timeout 3 ifup eth1 up')
        pc4_login.send_command('ifdown eth1 down; timeout 3 ifup eth1 up')
        pc5_login.send_command('ifdown eth1 down; timeout 3 ifup eth1 up')
        res = []
        del_scopes = [tc37_dynamic_dict1, tc37_dynamic_dict2,
                      tc37_static_dict1, tc37_static_dict2]
        for scope in del_scopes:
            if 'dynamic' in str(scope):
                del_res = dhcpserverapi.delete_dhcp_server_scope_v4(
                    'dynamic', p1=scope['from'], p2=scope['to'])
                res.append(del_res)
            else:
                dhcpserverapi.delete_dhcp_server_scope_v4(
                    'static', scope['ip'], scope['mac'])
                res.append(del_res)
        logger.info(f'init test env result: {all(res)}')
        Assertion.assert_equal(True, True, 'restore test env failed')


# Expect: DUT serve as client
# this case configuration including TC38, TC39
class TestDHCPServer_TC38(Test):
    uuid = "SOSAIOT-TC-55892"
    description = show_testcase_info(TESTPLAN, '38', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x1_to_dhcp(self):
        x1_dhcp_dict = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'dhcp'
        }
        res = interfacev4api.config_interface(**x1_dhcp_dict)
        Assertion.assert_equal(res, True, 'ERR: config x1 to dhcp failed')

    @repeat_method(3)
    def test_02_x1_renew_dhcp_lease_from_server(self):
        res = False
        pc2_login.send_command('service dhcpd restart')
        time.sleep(3)
        status = pc2_login.send_command('service dhcpd status')
        if re.search('dhcpd.* is running', status):
            logger.info('restart dhcpd success'.center(40, '='))
            for i in range(3):
                logger.info(f'dhcp renew ip for the {i+1} time')
                time.sleep(10)
                x1_ip = interfacev4api.get_interface_ip('X1')
                logger.info(x1_ip)
                if x1_ip == '0.0.0.0':
                    logger.info('renew x1...')
                    interfacev4cli.click_dhcp_renew('x1')
                else:
                    break
            res = True if '172.17.1.' in x1_ip else False
        else:
            logger.info('restart dhcpd failed.'.center(40, '='))
        CaseParams.tc38_res = res
        Assertion.assert_equal(
            res, True, 'ERR: check dut serve as dhcp client failed')

    def test_03_assign_X1_to_static(self):
        x1_static = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS_1,
            'dns2': Parameter.X1_DNS_2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        res = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(res, True, 'ERR: restore x1 to static failed')


# Expect: FW can renew lease
class TestDHCPServer_TC39(Test):
    uuid = "SOSAIOT-TC-55893"
    description = show_testcase_info(TESTPLAN, '39', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_renew_lease(self):
        res = CaseParams.tc38_res
        Assertion.assert_equal(res, True, "ERR: FW renew lease failed")


# Expect: FW still send last remain DNS info to DHCP client when X1 disconnect after reboot
class TestDHCPServer_TC91(Test):
    uuid = "SOSAIOT-TC-55906"
    description = show_testcase_info(TESTPLAN, '91', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '91')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_client_dns(self):
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        dynamic_range_dict = copy.deepcopy(dynamic_scope_base)
        dynamic_range_dict["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc91_x2_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
            **dynamic_range_dict)
        if addres:
            get_ip_res = pc_get_ip_lease(pc2_login, 'eth2')
            if get_ip_res:
                out = pc2_login.send_command(f'cat {DHCLIEN_LEASE_FILE}')
                res = True if Parameter.X1_DNS_1 in out and Parameter.X1_DNS_2 in out else False
            else:
                logger.error('pc get ip failed')
        else:
            logger.error("config dynamic range scope for x2 interface failed")
            res = False
        Assertion.assert_equal(res, True, "ERR: check dns for client failed")

    def test_02_disconnect_x1(self):
        res = interfacev4api.disable_interface(name='X1')
        Assertion.assert_equal(res, True, "ERR: disable X1 interface failed")

    def test_03_reboot_fw(self):
        res = settingsapi.boot_fw(mode=1)
        Assertion.assert_equal(res, True, "ERR: reboot FW failed")

    def test_04_client_renew_lease_and_check_dns(self):
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        res = pc_release_ip(pc2_login, 'eth2')
        res &= pc_get_ip_lease(pc2_login, 'eth2')[0]
        if res:
            out = pc2_login.send_command(
                f'cat {DHCLIEN_LEASE_FILE}')
            res &= True if Parameter.X1_DNS_1 in out and Parameter.X1_DNS_2 in out else False
        else:
            logger.error('ifconfig/release renew failed')
        Assertion.assert_equal(
            res, True, "ERR: check dns for client failed after X1 disconnect")

    def test_05_init_test_env(self):
        pc2_login.send_command('ifdown eth2; timeout 5 ifup eth2')
        interfacev4api.enable_interface(name='X1')
        dhcpserverapi.delete_dhcp_server_scope_v4(
            scope='dynamic', p1=tc91_x2_dict['from'], p2=tc91_x2_dict['to'])
        Assertion.assert_equal(True, True, "ERR: restore env failed")


# Expect: Fw still send DNS info to DHCP client after X1 disconnect
class TestDHCPServer_TC92(Test):
    uuid = "SOSAIOT-TC-55907"
    description = show_testcase_info(TESTPLAN, '92', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '92')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_client_dns(self):
        pc2_login.send_command('rm -rf dhclient/dhclient.leases')
        dynamic_range_dict = copy.deepcopy(dynamic_scope_base)
        dynamic_range_dict["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc91_x2_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
            **dynamic_range_dict)
        if addres:
            get_ip_res = pc_get_ip_lease(pc2_login, 'eth2')
            if get_ip_res:
                out = pc2_login.send_command(
                    f'cat {DHCLIEN_LEASE_FILE}')
                res = True if Parameter.X1_DNS_1 in out and Parameter.X1_DNS_2 in out else False
            else:
                logger.error('pc get ip failed')
        else:
            logger.error("config dynamic range scope for x2 interface failed")
            res = False
        Assertion.assert_equal(res, True, "ERR: check dns for client failed")

    def test_02_disconnect_x1(self):
        res = interfacev4api.disable_interface(name='X1')
        Assertion.assert_equal(res, True, "ERR: disable X1 interface failed")

    def test_03_client_renew_lease_and_check_dns(self):
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        res = pc_release_ip(pc2_login, 'eth2')
        res &= pc_get_ip_lease(pc2_login, 'eth2')[0]
        if res:
            output = pc2_login.send_command(
                f'cat {DHCLIEN_LEASE_FILE}')
            res &= True if Parameter.X1_DNS_1 in output and Parameter.X1_DNS_2 in output else False
        else:
            logger.error('ifconfig/release renew failed')
        Assertion.assert_equal(
            res, True, "ERR: check dns for client failed after X1 disconnect")

    def test_04_init_test_env(self):
        pc2_login.send_command('ifdown eth2; timeout 5 ifup eth2')
        interfacev4api.enable_interface(name='X1')
        res = dhcpserverapi.delete_dhcp_server_scope_v4(
            scope='dynamic', p1=tc91_x2_dict['from'], p2=tc91_x2_dict['to'])
        logger.info(f'init test env result: {res}')
        Assertion.assert_equal(True, True, "ERR: restore env failed")


# Expect: DNS Server in DHCP client is updated when DHCP WAN get new DNS Server.
class TestDHCPServer_TC95(Test):
    uuid = "SOSAIOT-TC-55910"
    description = show_testcase_info(TESTPLAN, '95', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '95')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_client_dns(self):
        res = False
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        dynamic_range_dict = copy.deepcopy(dynamic_scope_base)
        dynamic_range_dict["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            tc91_x2_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
            **dynamic_range_dict)
        if addres:
            get_res, ip_addr = pc_get_ip_lease(pc2_login, 'eth2')
            if get_res:
                output = pc2_login.send_command(
                    f'cat {DHCLIEN_LEASE_FILE}')
                res = True if Parameter.X1_DNS_1 in output and Parameter.X1_DNS_2 in output else False
            else:
                logger.error('pc get ip failed')
        else:
            logger.error("config dynamic range scope for x2 interface failed")
        Assertion.assert_equal(res, True, "ERR: check dns for client failed")

    def test_02_update_dns_server(self):
        res = False
        setres = dnsapi.set_dns(**tc95_dns_dict)
        if setres:
            output = dnsapi.get_dns()
            if tc95_dns_dict['dns']['server']['static']['primary'] in str(output):
                if tc95_dns_dict['dns']['server']['static']['secondary'] in str(output):
                    if tc95_dns_dict['dns']['server']['static']['tertiary'] in str(output):
                        res = True
        else:
            logger.error('set dns settings failed')
        Assertion.assert_equal(res, True, "ERR: update FW dns failed")

    def test_03_client_renew_lease_and_check_dns(self):
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        res = pc_release_ip(pc2_login, 'eth2')
        res &= pc_get_ip_lease(pc2_login, 'eth2')[0]
        if res:
            output = pc2_login.send_command(
                f'cat {DHCLIEN_LEASE_FILE}')
            if tc95_dns_dict['dns']['server']['static']['primary'] in str(output):
                if tc95_dns_dict['dns']['server']['static']['secondary'] in str(output):
                    if tc95_dns_dict['dns']['server']['static']['tertiary'] in str(output):
                        res &= True
        else:
            logger.error('ifconfig/release renew failed')
        Assertion.assert_equal(
            res, True, "ERR: check dns for client failed after X1 disconnect")

    def test_04_init_test_env(self):
        pc2_login.send_command('ifdown eth2; timeout 5 ifup eth2')
        interfacev4api.enable_interface(name='X1')
        dnsapi.set_dns(**tc95_dns_inhert_dict)
        res = dhcpserverapi.delete_dhcp_server_scope_v4(
            scope='dynamic', p1=tc91_x2_dict['from'], p2=tc91_x2_dict['to'])
        logger.info(f'init test env result: {res}')
        Assertion.assert_equal(True, True, "ERR: init env failed")


# Expect: the DNS Server in client is valid when DUT with PPPoE WAN is rebooting.
class TestDHCPServer_TC96(Test):
    uuid = "SOSAIOT-TC-55911"
    description = show_testcase_info(TESTPLAN, '96', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '96')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x1_to_pppoe_mode(self):
        x1_static = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'pppoe',
            'pppoe_user': 'pppoe',
            'pppoe_servicename': '',
            'pppoe_passwd': 'password',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 2,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        res = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(res, True, 'ERR: config x1 failed')

    def test_02_x1_renew_ip_from_pppoe_server(self):
        time.sleep(60)
        for i in range(10):
            logger.info(f'pppoe renew ip for the {i+1} time')
            x1_ip = interfacev4api.get_interface_ip('X1')
            logger.info("Interface X1 IP: " + x1_ip)
            if x1_ip == '0.0.0.0':
                interfacev4cli.click_pppoe_reconnect('X1')
                time.sleep(60)
            else:
                break
        res = True if '172.17.2.' in x1_ip else False
        Assertion.assert_equal(
            res, True, 'ERR: check dut serve as dhcp client failed')

    def test_03_check_client_dns(self):
        res = False
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        x2_dict = {
            "from": "2.2.2.6",
            "to": "2.2.2.26",
            "default_gateway": "2.2.2.168"
        }
        dynamic_range_dict = copy.deepcopy(dynamic_scope_base)
        dynamic_range_dict["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            x2_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
            **dynamic_range_dict)
        if addres:
            get_ip_res = pc_get_ip_lease(pc2_login, 'eth2')[0]
            if get_ip_res:
                output = pc2_login.send_command(
                    f'cat {DHCLIEN_LEASE_FILE}')
                res = True if Parameter.PPPOE_DNS in output else False
            else:
                logger.error('pc get ip failed')
        else:
            logger.error("config dynamic range scope for x2 interface failed")
        Assertion.assert_equal(res, True, "ERR: check dns for client failed")

    def test_04_disconnect_x1(self):
        res = interfacev4api.disable_interface(name='X1')
        Assertion.assert_equal(res, True, "ERR: disable X1 interface failed")

    def test_05_reboot_fw(self):
        res = settingsapi.boot_fw(mode=1)
        Assertion.assert_equal(res, True, "ERR: reboot FW failed")

    def test_06_client_renew_lease_and_check_dns(self):
        pc2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        res = pc_release_ip(pc2_login, 'eth2')
        res &= pc_get_ip_lease(pc2_login, 'eth2')[0]
        if res:
            output = pc2_login.send_command(
                f'cat {DHCLIEN_LEASE_FILE}')
            res &= True if Parameter.PPPOE_DNS in output else False
        else:
            logger.error('ifconfig/release renew failed')
        Assertion.assert_equal(
            res, True, "ERR: check dns for client failed after X1 disconnect")

    def test_07_init_test_env(self):
        pc2_login.send_command('ifdown eth2; timeout 5 ifup eth2')
        interfacev4api.enable_interface(name='X1')
        res = dhcpserverapi.delete_dhcp_server_scope_v4(
            scope='dynamic', p1=tc91_x2_dict['from'], p2=tc91_x2_dict['to'])
        logger.info(f'init test env result: {res}')
        Assertion.assert_equal(True, True, "ERR: restore env failed")


# Expect: DHCP ranges should be imported back
class TestDHCPServer_TC78(Test):
    uuid = "SOSAIOT-TC-55902"
    description = show_testcase_info(TESTPLAN, '78', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '78')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dhcp_ranges(self):
        res = []
        scopes = [tc78_dynamic_dict1, tc78_dynamic_dict2, tc78_dynamic_dict3,
                  tc78_dynamic_dict4, tc78_static_dict1, tc78_static_dict2]
        for scope in scopes:
            if 'dynamic' in str(scope):
                dscope_range = copy.deepcopy(dynamic_scope_base)
                dscope_range["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
                    scope)
                addres = dhcpserverapi.add_dhcp_server_scope_dynamic(
                    **dscope_range)
                res.append(addres)
            else:
                sscope_range = copy.deepcopy(static_scope_base)
                sscope_range["dhcp_server"]["ipv4"]["scope"]["static"][0].update(
                    scope)
                addres = dhcpserverapi.add_dhcp_server_scope_static(
                    **sscope_range)
                res.append(addres)
        Assertion.assert_equal(all(res), True, 'ERR: set dhcp ranges failed')

    def test_02_export_pref_file(self):
        res = settingsapi.export_setting_exp(filepath=EXP_FILE)
        logger.info('check exp file...')
        output = pc1_login.send_command('ls -l /tmp | grep exp')
        res &= True if 'cyuan_dhcp_test.exp' in output else False
        Assertion.assert_equal(res, True, 'ERR: export pref file failed')

    def test_03_fac_default_fw(self):
        res = settingsapi.boot_fw(mode=2)
        Assertion.assert_equal(
            res, True, 'ERR: boots fw with fac-default failed')

    def test_04_import_dhcp_settings(self):
        res = settingsapi.import_setting_exp(EXP_FILE)
        Assertion.assert_equal(res, True, "ERR: import settings failed")

    def test_05_check_dhcp_settings(self):
        out_static = dhcpserverapi.get_dhcp_server_scope_static()
        res = True if tc78_static_dict1['comment'] in str(
            out_static) and tc78_static_dict2['comment'] in str(out_static) else False
        out_dynamic = dhcpserverapi.get_dhcp_server_scope_dynamic()
        if tc78_dynamic_dict1['comment'] in str(out_dynamic):
            if tc78_dynamic_dict2['comment'] in str(out_dynamic):
                if tc78_dynamic_dict3['comment'] in str(out_dynamic):
                    if tc78_dynamic_dict4['comment'] in str(out_dynamic):
                        res &= True
        Assertion.assert_equal(res, True, "ERR: check dhcp settings failed")

    def test_06_init_TB(self):
        logger.info('remove exp file on localhost...')
        out = pc1_login.send_command(f'rm -rf {EXP_FILE}')
        logger.info('stop dhcp service on server...')
        for i in range(5):
            pc2_login.send_command('service dhcpd stop')
            status = pc2_login.send_command('service dhcpd status')
            logger.info(status)
            if re.search('is stopped', status, re.I):
                logger.info('dhcp service is stopped')
                break
        logger.info('stop pppoe-server...')
        pc2_login.send_command('killall pppoe-server')
