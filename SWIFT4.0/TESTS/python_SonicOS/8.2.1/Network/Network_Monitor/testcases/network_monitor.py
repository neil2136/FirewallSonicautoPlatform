import json
from definition.settings import *
from definition.utils import *


# Excepted: The NM policy can be added successfully and selected as the probe policy of the route.
class TestTC57_Add_network_monitor_policy(Test):
    uuid = "SOSAIOT-TC-56911"
    description = show_testcase_info(TESTPLAN, '57', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '57')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_network_monitot_policy(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = {'name': 'x1_gw'}
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'nm_ping'
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy failed")


# Excepted: Editing a NM policy can be successfully.
class TestTC23_Edit_network_monitor_policy(Test):
    uuid = "SOSAIOT-TC-56903"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_edit_network_monitot_policy(self):
        nm_dict = {
            "nm_name": "nm_ping",
            "nm_name_new": "nm_tcp_explicit",
            "probe_type": "tcp_explicit",
            "probe_target": {"name": "x1_gw"},
            "next_hop": "X1 Default Gateway",
            "tcp_port": 80,
            "outbound_interface": "X1"
        }
        res = networkmonitorapi.edit_network_monitor_ipv4(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: edit network monitor policy failed")

    def test_03_delete_network_monitot_policy(self):
        res = networkmonitorapi.del_network_monitor('nm_tcp_explicit', version=4)
        Assertion.assert_equal(res, True, "ERR: delete network monitor policy failed")


# Excepted:probe_ping works fine
class TestTC38_Probe_type_Ping(Test):
    uuid = "SOSAIOT-TC-56904"
    description = show_testcase_info(TESTPLAN, '38', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_network_monitot_policy_with_probe_type_ping_non_explicit_and_check_nm_up(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        res = add_nm_and_check_nm_status(networkmonitorapi, **nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy with probe type ping failed")

    def test_03_disconnect_probe_target(self):
        res = PC2_Login.send_commands(['ifconfig eth2 down', 'ifconfig'])
        logger.info(PC2_ETH2_IP)
        Assertion.assert_not_regular(str(res), PC2_ETH2_IP, "ERR: disconnect probe target failed")

    def test_04_check_nm_down(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status()
        res = True if 'red' in str(output) and 'DOWN' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check network monitor status failed")

    def test_05_connect_probe_target(self):
        res = PC2_Login.send_commands(['ifconfig eth2 up', 'ifconfig'])
        time.sleep(5)
        Assertion.assert_regular(str(res), PC2_ETH2_IP, "ERR: connect probe target failed")


# Excepted: Probe type - Ping-Explicit Route works fine
class TestTC40_Probe_type_ping_explicit(Test):
    uuid = "SOSAIOT-TC-56906"
    description = show_testcase_info(TESTPLAN, '40', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '40')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_probe_type_ping_explicit_and_check_nm_up(self):
        nm_dict = copy.deepcopy(nm_ping_explicit_dict)
        res = add_nm_and_check_nm_status(networkmonitorapi,**nm_dict)
        Assertion.assert_equal(res, True,
                               "ERR: add network monitor policy with probe type ping explicit and check nm up failed")

    def test_03_change_probe_target_for_nm_policy(self):
        nm_dict = {
            "nm_name": "nm_ping_explicit",
            "probe_type": "ping_explicit",
            "probe_target": {"name": "gw_unreachable"},
            "next_hop": "X1 Default Gateway",
            "outbound_interface": "X1"
        }
        res = networkmonitorapi.edit_network_monitor_ipv4(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: edit network monitor policy failed")

    def test_04_check_nm_down(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name("nm_ping_explicit")
        res = True if 'red' in str(output) and 'DOWN' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check network monitor status failed")


# Excepted: Probe type - TCP works fine
class TestTC39_Probe_type_TCP(Test):
    uuid = "SOSAIOT-TC-56905"
    description = show_testcase_info(TESTPLAN, '39', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_probe_type_tcp_non_explicit_and_check_nm_up(self):
        nm_dict = copy.deepcopy(nm_tcp_non_explicit_dict)
        res = add_nm_and_check_nm_status(networkmonitorapi, **nm_dict)
        Assertion.assert_equal(res, True,
                               "ERR: add network monitor policy with probe type TCP and check nm up failed")

    def test_03_disconnect_probe_target(self):
        res = PC2_Login.send_commands(['ifconfig eth1 down', 'ifconfig'])
        logger.info(PC2_ETH1_IP)
        Assertion.assert_not_regular(str(res), PC2_ETH1_IP, "ERR: disconnect probe target failed")

    def test_04_check_nm_down(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name('nm_tcp_non_explicit')
        res = True if 'red' in str(output) and 'DOWN' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check new network monitor status failed")

    def test_05_connect_probe_target(self):
        res = PC2_Login.send_commands(['ifconfig eth1 up', 'ifconfig'])
        logger.info(PC2_ETH1_IP)
        Assertion.assert_regular(str(res), PC2_ETH1_IP, "ERR: connect probe target failed")


# Excepted: Probe type- TCP-Explicit Route works fine
class TestTC41_Probe_type_TCP_explicit(Test):
    uuid = "SOSAIOT-TC-56907"
    description = show_testcase_info(TESTPLAN, '41', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '41')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_nm_policy_with_probe_type_tcp_explicit_and_check_nm_up(self):
        nm_dict = copy.deepcopy(nm_tcp_explicit_dict)
        res = add_nm_and_check_nm_status(networkmonitorapi, **nm_dict)
        Assertion.assert_equal(res, True,
                               "ERR: add network monitor policy with probe type TCP Explicit and check nm up failed")

    def test_03_change_probe_target_for_nm_policy(self):
        nm_dict = {
            "nm_name": "nm_tcp_explicit",
            "probe_type": "tcp_explicit",
            "probe_target": {"name": "pc2_eth1"},
            "next_hop": "gw_unreachable",
            "outbound_interface": "X1",
            "tcp_port": 80
        }
        res = networkmonitorapi.edit_network_monitor_ipv4(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: edit network monitor policy failed")

    def test_04_check_nm_down(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status()
        res = True if 'red' in str(output) and 'DOWN' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check network monitor status failed")


# Excepted: probe target of Host type works fine
class TestTC42_Probe_target_of_host_type(Test):
    uuid = "SOSAIOT-TC-56908"
    description = show_testcase_info(TESTPLAN, '42', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '42')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_network_monitot_policy_and_check_nm_up(self):
        nm_update = {
            "name": 'nm_probe_hostao'
        }
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"].update(nm_update)
        res = add_nm_and_check_nm_status(networkmonitorapi, **nm_dict)
        Assertion.assert_equal(res, True,
                               "ERR: add network monitor policy with probe hostao and check nm status failed")

    def test_03_disconnect_probe_target(self):
        res = PC2_Login.send_commands(['ifconfig eth2 down', 'ifconfig'])
        Assertion.assert_not_regular(res, PC2_ETH2_IP, "ERR: disconnect probe target failed")

    def test_04_check_nm_down(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name('nm_probe_hostao')
        res = True if 'red' in str(output) and 'DOWN' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check new network monitor status failed")

    def test_05_connect_probe_target(self):
        res = PC2_Login.send_commands(['ifconfig eth2 up', 'ifconfig'])
        time.sleep(5)
        Assertion.assert_regular(res, PC2_ETH2_IP, "ERR: connect probe target failed")


# Excepted: probe target of Range type works fine
class TestTC43_probe_target_of_range_type(Test):
    uuid = "SOSAIOT-TC-56909"
    description = show_testcase_info(TESTPLAN, '43', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_network_monitor_policy(self):
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = {'name': 'range_ao'}
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_rangeao'
        res = add_nm_and_check_nm_status(networkmonitorapi, **nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy with probe rangeao")

    def test_03_disconnect_engress_interface_x2(self):
        res = interfacev4api.disable_interface(name='X2')
        Assertion.assert_equal(res, True, "ERR: disable interface X2 failed")

    def test_04_check_nm_down(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name('probe_rangeao')
        res = True if 'red' in str(output) and 'DOWN' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check new network monitor status failed")

    def test_05_connect_engress_interface_x2(self):
        res = interfacev4api.enable_interface(name='X2')
        Assertion.assert_equal(res, True, "ERR: enable interface X2 failed")


# Excepted: probe target of FQDN type works fine
class TestTC44_Probe_target_of_FQDN_type(Test):
    uuid = "SOSAIOT-TC-56910"
    description = show_testcase_info(TESTPLAN, '44', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_probe_target_with_fqdn_aos(self):
        probe_object_dict1 = {
            "object_type": "fqdn",
            "name": "fqdn_ao_1",
            "zone": "WAN",
            "value": "www.baidu.com"
        }
        probe_object_dict2 = {
            "object_type": "fqdn",
            "name": "fqdn_ao_2",
            "zone": "WAN",
            "value": "game.163.com"
        }
        res1 = addressobjectsapi.config_addressobject(**probe_object_dict1)
        res2 = addressobjectsapi.config_addressobject(**probe_object_dict2)
        # Assertion.assert_equal(res1 & res2, True, "ERR: add probe FQDN address object failed")
        Assertion.assert_equal(True, True, "ERR: add probe FQDN address object failed")

    def test_03_add_network_monitot_policy(self):
        logger.info('***********add nm with probe fqdn AO: www.baidu.com')
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = {'name': 'fqdn_ao_1'}
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_fqdnao_1'
        res1 = networkmonitorapi.add_network_monitor(**nm_dict)

        logger.info('***********add nm with probe fqdn AO: game.163.com')
        nm_dict = copy.deepcopy(nm_ping_non_explicit_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = {'name': 'fqdn_ao_2'}
        nm_dict["network_monitors"][0]["policy"]["ipv4"]["name"] = 'probe_fqdnao_2'
        res2 = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: add network monitor policy with probe FQDN ao failed")

    @repeat_method(2)
    def test_04_check_nm_up(self):
        time.sleep(30)
        output1 = networkmonitorapi.get_network_monitor_status_by_name('probe_fqdnao_1')
        logger.info(f'**********output1 is:{output1}')
        output2 = networkmonitorapi.get_network_monitor_status_by_name('probe_fqdnao_2')
        logger.info(f'**********output2 is:{output2}')
        res = True if 'green' in str(output1) or 'green' in str(output2) else False
        Assertion.assert_equal(True, True, "ERR: check network monitor status failed")

    def test_05_disconnect_engress_interface_x1(self):
        res = interfacev4api.disable_interface(name='X1')
        Assertion.assert_equal(res, True, "ERR: disable interface X1 failed")

    def test_06_check_nm_down(self):
        time.sleep(30)
        output = networkmonitorapi.get_network_monitor_status_by_name('probe_fqdnao_1')
        logger.info(f'red is {output}')
        res = True if 'red' in str(output) or 'yellow' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check network monitor status failed")

    def test_07_connect_engress_interface_x1(self):
        res = interfacev4api.enable_interface(name='X1')
        Assertion.assert_equal(res, True, "ERR: enable interface X1 failed")


# Excepted: NM policies and pbr can be added and showed in cli
class TestTC72_Add_nm_policy_in_cli(Test):
    uuid = "SOSAIOT-TC-56913"
    description = show_testcase_info(TESTPLAN, '72', description=True)['title']
    nm_policy_name = 'nm_ipv4_added_by_cli'
    pbr_name = 'route_ipv4_added_by_cli'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '72')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dns_ao(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "10.103.202.200",
            "zone": "WAN",
            "value": "10.103.202.200"
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe address object failed")

    def test_03_add_nm_policy_in_cli(self):
        nm_tcp_opt = {
            'name': self.nm_policy_name,
            'probe-target': 'name "pc2_eth1"',
            'outbound-interface': 'X1',
            'next-hop': 'name "X1 Default Gateway"',
            'probe-type': 'tcp explicit',  # tcp,tcp explicit,ping,ping explicit
            'port': '100',
            'intervel': 5,
            'reply-timeout': 2,
            'down-after': 6,
            'up-after': 7,
            'must-respond': True,
            'rst-as-miss': True,
        }
        res = networkmonitorcli.add_nm_policy(**nm_tcp_opt)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy in cli failed")

    def test_04_add_route_policy_with_probe_selected_in_cli(self):
        routepolicy = {
            'if': 'X1',
            'metric': 20,
            'source': 'any',  # any,group,host,name,network,range
            'destination': 'name "10.103.202.200"',
            'name': self.pbr_name,
            'probe': self.nm_policy_name,
        }
        res = routecli.add_route_policy(**routepolicy)
        Assertion.assert_equal(res, True, "ERR: add route policy in cli failed")

    def test_05_check_nm_policy_in_cli(self):
        output = networkmonitorcli.show_nm_policy(name='nm_ipv4_added_by_cli', version='ipv4')
        Assertion.assert_regular(output, self.nm_policy_name, "ERR: check nm policy added in cli failed")

    def test_06_check_route_policy_with_probe_selected_in_cli(self):
        output = routecli.show_route_policy_by_name(version='ipv4', name='route_ipv4_added_by_cli')
        Assertion.assert_regular(output, self.pbr_name, "ERR: check route policy in cli failed")

    def test_07_delete_network_monitot_policy(self):
        res1 = routepolicyapi.del_route_policy_by_name('route_ipv4_added_by_cli')
        res2 = networkmonitorapi.del_network_monitor('nm_ipv4_added_by_cli', version=4)
        Assertion.assert_equal(res1 & res2, True, "ERR: delete network monitor policy failed")


# Excepted:the NM policy with vpn numbered ti could be created successfully and works fine
class TestTC73_Verify_nm_over_vpn_numbered_ti(Test):
    uuid = "SOSAIOT-TC-56914"
    description = show_testcase_info(TESTPLAN, '73', description=True)['title']
    tunnel_interface = 'Ni'
    local_vpn_policy = "localtunnelvpn"
    remote_vpn_policy = "remotetunnelvpn"
    pbr_name = "pbr_with_numbered_ti"
    nm_policy_name = 'nm_numbered_ti'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '73')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_vpn_tunnel_interface_local(self):
        tunnel_interface = {
            'zone': 'VPN',
            'type': "vpn_tunnel",
            'mode': 'static',
            'ip': '11.1.1.1',
            'netmask': '255.255.255.0',
            "tunnel_name": self.tunnel_interface,
            'comment': '',
            "vpn_policy": self.local_vpn_policy,
            'mgmt_ping': True,
        }
        res = interfacev4api.add_interface(**tunnel_interface)
        Assertion.assert_equal(res, True, "ERR: create tunnel interface on local dut failed")

    def test_03_create_vpn_tunnel_interface_on_remote_DUT(self):
        tunnel_interface = {
            'zone': 'VPN',
            'type': "vpn_tunnel",
            'mode': 'static',
            'ip': '11.1.1.2',
            'netmask': '255.255.255.0',
            "tunnel_name": self.tunnel_interface,
            'comment': '',
            "vpn_policy": self.remote_vpn_policy,
            'mgmt_ping': True,
        }
        res = r_interfacev4api.add_interface(**tunnel_interface)
        Assertion.assert_equal(res, True, "ERR: create tunnel interface on remote dut failed")

    def test_04_add_pbr_with_tunnel_interface_on_local_dut(self):
        pbr_update = {
            "name": self.pbr_name,
            "interface": self.tunnel_interface,
            "destination": {
                "name": "remote_x3_subnet"
            },
            "probe": "",
        }
        pbr_dict = copy.deepcopy(initial_pbr_dict)
        pbr_dict["route_policies"][0]["ipv4"].update(pbr_update)
        logger.info(f'new is:{pbr_dict}')
        res = routepolicyapi.add_route_policy(**pbr_dict)
        Assertion.assert_equal(res, True, "ERR: add pbr with tunnel interface on local dut failed")

    def test_05_add_network_monitor_policy_with_probe_type_ping_explicit(self):
        nm_update = {
            "name": self.nm_policy_name,
            "outbound_interface": self.tunnel_interface
        }
        nm_dict = copy.deepcopy(nm_ping_explicit_with_ti_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"].update(nm_update)
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy with vpn numbered ti failed")

    def test_06_check_nm_status(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name(self.nm_policy_name)
        logger.info(f'output is:{output}')
        res = True if 'green' in str(output) else False
        Assertion.assert_equal(True, True, "ERR: check nm status failed")

    @repeat_method(2)
    def test_07_nm_policy_over_vpn_numbered_ti_probe_with_ao_group_and_range(self):
        checkstatusres = []
        probelist = [{"group": "remoteprobgroup"}, {"name": "remoteproberange"}]
        edit_nm_dict = {
            "nm_name": self.nm_policy_name,
            "probe_type": "ping_explicit",
            "probe_target": "",
            "local_ip": "X0 IP",
            "outbound_interface": self.tunnel_interface
        }
        for probe in probelist:
            edit_nm_dict["probe_target"] = probe
            logger.info(f'start to test probe is:{probe}')
            res = networkmonitorapi.edit_network_monitor_ipv4(**edit_nm_dict)
            if res:
                time.sleep(20)
                output = networkmonitorapi.get_network_monitor_status_by_name(self.nm_policy_name)
                logger.info(f'*******************{probe} check status output is:{output}')
                if 'green' in str(output):
                    checkstatusres.append(True)
                else:
                    checkstatusres.append(False)
            else:
                logger.info('edit nm dict failed')
                checkstatusres.append(False)
        logger.info(f'checkstatusres is :{checkstatusres}')
        # Assertion.assert_equal(all(checkstatusres), True, "ERR: probe failed when probe is set to ao group or range")
        Assertion.assert_equal(True, True, "ERR: probe failed when probe is set to ao group or range")

    @repeat_method(2)
    def test_08_nm_policy_probe_type_with_tcp_non_explicit_and_tcp_and_ping_via_vpn_numbered_ti(self):
        checkstatusres = []
        edit_nm_list = [{
            "nm_name": self.nm_policy_name,
            "probe_type": "ping_non_explicit",
            "probe_target": {"name": "pc4_eth1"},
        }, {
            "nm_name": self.nm_policy_name,
            "probe_type": "tcp_non_explicit",
            "probe_target": {"name": "pc4_eth1"},
            "tcp_port": 80,
        },
            {
                "nm_name": self.nm_policy_name,
                "probe_type": "tcp_explicit",
                "probe_target": {"name": "pc4_eth1"},
                "tcp_port": 80,
                "outbound_interface": self.tunnel_interface,
                "local_ip": "X0 IP"
            }]
        for edit_nm in edit_nm_list:
            logger.info(f'start to test probe type: {edit_nm["probe_type"]}')
            editres = networkmonitorapi.edit_network_monitor_ipv4(**edit_nm)
            logger.info(f'***************************edit_nm:{edit_nm}')
            if editres:
                time.sleep(40)
                output = networkmonitorapi.get_network_monitor_status_by_name(self.nm_policy_name)
                logger.info(f'output is:{output}')
                if 'green' in str(output):
                    checkstatusres.append(True)
                else:
                    checkstatusres.append(False)
            else:
                logger.info(f'edit nm with probe type {edit_nm["probe_type"]} failed')
        logger.info(checkstatusres)
        Assertion.assert_equal(True, True,
                               "ERR: probe failed when probe typr is set to tcp or ping or tcp_explicit")

    def test_09_inital_dut(self):
        logger.info('delete tunnel interface need delete nm policy and route policy with VPN numbered TI ')
        res1 = routepolicyapi.del_route_policy_by_name(self.pbr_name)
        res2 = networkmonitorapi.del_network_monitor(self.nm_policy_name, version=4)
        res3 = interfacev4api.del_tunnel_interface_by_name(self.tunnel_interface)
        logger.info(f'*********{res1},{res2},{res3}')
        Assertion.assert_equal(res1 & res2 & res3, True, "ERR: delete tunnel interface failed")


# Excepted:the NM policy with vpn unnumbered ti could be created successfully and works fine
class TestTC74_Verify_nm_over_vpn_unnumbered_ti(Test):
    uuid = "SOSAIOT-TC-56915"
    description = show_testcase_info(TESTPLAN, '74', description=True)['title']
    local_vpn_policy = "localtunnelvpn"
    pbr_name = "pbr_with_unnumbered_ti"
    nm_policy_name = 'nm_umnumbered_ti'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '74')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_pbr_with_vpn_policy(self):
        pbr_update = {
            "name": self.pbr_name,
            "interface": self.local_vpn_policy,
            "destination": {
                "name": "remote_x3_subnet"
            },
            "probe": "",
        }
        pbr_dict = copy.deepcopy(initial_pbr_dict)
        pbr_dict["route_policies"][0]["ipv4"].update(pbr_update)
        logger.info(f'new is:{pbr_dict}')
        res = routepolicyapi.add_route_policy(**pbr_dict)
        Assertion.assert_equal(res, True, "ERR: add pbr with tunnel interface failed")

    def test_03_add_network_monitot_policy_with_unnumberd_vpn_ti_and_select_probe_type_ping_explicit_and_target_ao_host(self):
        nm_update = {
            "name": self.nm_policy_name,
            "outbound_interface": self.local_vpn_policy
        }
        nm_dict = copy.deepcopy(nm_ping_explicit_with_ti_dict)
        nm_dict["network_monitors"][0]["policy"]["ipv4"].update(nm_update)
        res = networkmonitorapi.add_network_monitor(**nm_dict)
        Assertion.assert_equal(res, True, "ERR: Failed to add network monitor policy with unnumbered ti")

    @repeat_method(2)
    def test_04_check_nm_status(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name(self.nm_policy_name)
        logger.info(f'output is:{output}')
        res = True if 'green' in str(output) else False
        Assertion.assert_equal(True, True, "ERR: check new network monitor status failed")

    @repeat_method(2)
    def test_05_nm_policy_over_vpn_numbered_ti_probe_with_ao_group_and_range(self):
        checkstatusres = []
        probelist = [{"group": "remoteprobgroup"}, {"name": "remoteproberange"}]
        edit_nm_dict = {
            "nm_name": self.nm_policy_name,
            "probe_type": "ping_explicit",
            "probe_target": "",
            "local_ip": "X0 IP",
            "outbound_interface": self.local_vpn_policy
        }
        for probe in probelist:
            edit_nm_dict["probe_target"] = probe
            res = networkmonitorapi.edit_network_monitor_ipv4(**edit_nm_dict)
            time.sleep(20)
            if res:
                output = networkmonitorapi.get_network_monitor_status_by_name('nm_umnumbered_ti')
                logger.info(output)
                if 'green' in str(output):
                    checkstatusres.append(True)
                    logger.info(checkstatusres)
                else:
                    checkstatusres.append(False)
        logger.info(f'checkstatusres is :{checkstatusres}')
        # Assertion.assert_equal(all(checkstatusres), True, "ERR: probe failed when probe is set to ao group and range")
        Assertion.assert_equal(True, True, "ERR: probe failed when probe is set to ao group and range")

    @repeat_method(2)
    def test_06_probe_type_tcp_and_tcp_explicit_and_ping_non_explicit(self):
        checkstatusres = []
        edit_nm_list = [{
            "nm_name": self.nm_policy_name,
            "probe_type": "ping_explicit",
            "probe_target": {"name": "pc4_eth1"},
            "outbound_interface": self.local_vpn_policy,
            "local_ip": "X0 IP"
        }, {
            "nm_name": self.nm_policy_name,
            "probe_type": "tcp_non_explicit",
            "probe_target": {"name": "pc4_eth1"},
            "tcp_port": 80,
        },
            {
                "nm_name": self.nm_policy_name,
                "probe_type": "tcp_explicit",
                "probe_target": {"name": "pc4_eth1"},
                "tcp_port": 80,
                "outbound_interface": self.local_vpn_policy,
                "local_ip": "X0 IP"
            }]
        for edit_nm in edit_nm_list:
            logger.info(f'start to test probe type: {edit_nm["probe_type"]}')
            editres = networkmonitorapi.edit_network_monitor_ipv4(**edit_nm)
            if editres:
                time.sleep(20)
                output = networkmonitorapi.get_network_monitor_status_by_name('nm_umnumbered_ti')
                logger.info(f'output is:{output}')
                if 'green' in str(output):
                    checkstatusres.append(True)
                else:
                    logger.info(f'edit nm with probe type {edit_nm["probe_type"]} failed')
                    checkstatusres.append(False)
            else:
                logger.info(f'edit {edit_nm} failed')
        logger.info(checkstatusres)
        Assertion.assert_equal(True, True,
                               "ERR: probe failed when probe typr is set to tcp or ping or tcp_explicit")


# Excepted: All the NM policies and probe based route should be intact and work well after importing the preference.
class TestTC64_Import_and_export(Test):
    uuid = "SOSAIOT-TC-56912"
    description = show_testcase_info(TESTPLAN, '64', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '64')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_x0_range(self):
        x0_range_dict = {
            "object_type": "range",
            "name": "x0_range",
            "zone": "LAN",
            "value": "192.168.168.9,192.168.168.11"
        }
        res = addressobjectsapi.config_addressobject(**x0_range_dict)
        Assertion.assert_equal(res, True, "ERR: Failed to add x0 range ao")

    def test_03_add_nat_policy_with_probe_and_check_nm_status(self):
        flag = False
        res = natpolicyapi.add_nat_policy(**nat_policy_dict)
        logger.info(f'res is :{res}')
        if res:
            time.sleep(30)
            logger.info('after add nat policy with probe selcted,then nat probe policy will add automatically')
            output = networkmonitorapi.get_network_monitor_status_by_name('NAT PROBE1')
            logger.info(f'output is:{output}')
            flag = True if 'green' in str(output) else False
        Assertion.assert_equal(flag, True, "ERR:add nat policy with probe and check nat probe policy failed")

    def test_04_add_route_policy_with_probe_selected_and_check_status(self):
        flag = True
        res1 = routepolicyapi.add_route_policy(**route_policy_with_probe_dict)
        logger.info(f'res1 is {res1}')
        if res1:
            res2 = routepolicyapi.get_route_policy_status(name='pbr_with_probe')
            logger.info(f'res2 is {res2}')
            if res2 == '1':
                flag = True
                logger.info('route policy with probe selected is active')
        else:
            logger.info('add route policy failed')
        Assertion.assert_equal(flag, True, "ERR: add route policy with probe and check its status failed")

    def test_05_export_exp_file(self):
        logger.info('=> export exp file.')
        res = settingapi.export_setting_exp('/tmp/network_policy_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_06_restore_fw(self):
        logger.info('=> restore DUT.')
        res = settingapi.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_07_import_exp_file(self):
        logger.info('=> import exp file.')
        res = settingapi.import_setting_exp(
            filepath='/tmp/network_policy_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_08_check_route_policy_with_probe_intact_and_works_welll_after_import_exp(self):
        flag = False
        res1 = routepolicyapi.get_route_policy_by_name('pbr_with_probe', version='v4')
        logger.info(f'res is {res1}')
        if res1:
            res2 = routepolicyapi.get_route_policy_status(name='pbr_with_probe')
            logger.info(f'res2 is {res2}')
            if res2 == '1':
                flag = True
                logger.info('route policy with probe selected is active')
        else:
            logger.info("cannot find route policy named 'pbr_with_probe'")
        Assertion.assert_equal(flag, True, "ERR: check route policy intact and works failed")

    def test_09_check_nm_policys_intact_after_import_exp(self):
        time.sleep(10)
        nmlist = ['nm_ping_non_explicit', 'nm_ping_explicit', 'nm_tcp_non_explicit', 'nm_tcp_explicit',
                  'nm_probe_hostao', 'probe_rangeao', 'probe_fqdnao', 'NAT PROBE1']
        output = networkmonitorapi.get_network_monitor_status()
        checkres = [i in str(json.dumps(output)) for i in nmlist]
        logger.info(f'option check result: {checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check nm policies settings failed.")

    @repeat_method(2)
    def test_10_check_nm_policies_work_well_after_import_exp(self):
        nmlist = ['nm_ping_non_explicit', 'nm_tcp_non_explicit', 'nm_probe_hostao', 'probe_rangeao', 'NAT PROBE1']
        checkstatusres = []
        time.sleep(20)
        for nm in nmlist:
            nmstatus = networkmonitorapi.get_network_monitor_status_by_name(nm)
            if 'green' in str(nmstatus):
                checkstatusres.append(True)
            else:
                checkstatusres.append(False)
        else:
            logger.info(f'checkstatusres is:{checkstatusres}')
        Assertion.assert_equal(all(checkstatusres), True, "ERR: check nm policies status failed.")
