from definition.settings import *
from definition.utils import *


# Excepted: an NDP entry can be added successfully and the related NDP cache will be added too with STATIC state.
class TestBaseFun_TC1(Test):
    uuid = "SOSAIOT-TC-58536"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_x2_v4(self):
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 ip address failed")

    def test_03_configure_x2_with_proper_ipv6_address_and_check_ipv6_route_policy(self):
        flag = False
        res = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        if res:
            output = routepolicyapi.get_auto_route_policy(version='v6')
            if Parameter.X2_V6_PREFIX + '/' + str(Parameter.PREFIX_LENGTH_1) in str(output):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: configure X2 and check ipv6 route policy failed")

    def test_04_modify_x2_and_check_ipv6_route_policy(self):
        flag = False
        res = interfacev6api.config_interface_ipv6(**x2_v6_modify_dict)
        if res:
            output = routepolicyapi.get_auto_route_policy(version='v6')
            if Parameter.X2_V6_MODIFY_PREFIX + '/' + str(Parameter.PREFIX_LENGTH_2) in str(output):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: modify X2 and check ipv6 route policy failed")

    def test_05_unassign_x2_and_check_ipv6_route_policy(self):
        flag = False
        res = interfacev4api.unassign_interface(interface='X2')
        if res:
            output = routepolicyapi.get_auto_route_policy(version='v6')
            if Parameter.X2_V6_MODIFY_PREFIX + '/' + str(Parameter.PREFIX_LENGTH_2) not in str(output):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: unassign X2 and check ipv6 route policy failed")


# Excepted:a PBR entry with valid ipv6 network: destination AO type: network can be added and traffic can hit this PBR
class TestBaseFun_TC6(Test):
    uuid = "SOSAIOT-TC-58544"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_x2_with_proper_ipv6_address(self):
        res1 = interfacev4api.config_interface(**x2_static)
        res2 = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: Config X2 ipv4 and ipv6 address failed")

    def test_03_add_network_ao_and_host_ao(self):
        ao_gateway = {
            "object_type": "host",
            "name": 'gw',
            "zone": 'WAN',
            "ip": '2001:1::169'
        }
        dest_ao_network = {
            'name': 'dest_network_ao',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '2002:1::0',
            'mask': '/64',
        }
        rc1 = addressobjectapi.config_ipv6_addressobject(**ao_gateway)
        rc2 = addressobjectapi.config_ipv6_addressobject(**dest_ao_network)
        logger.info(f'rc1:{rc1},rc2:{rc2}')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: configure AOs failed")

    def test_04_add_ipv6_route_policy(self):
        dict_update = {
            "name": "dest_network_test",
            "interface": "X2",
            "destination": {"name": "dest_network_ao"},
            "gateway": {"name": "gw"}
        }
        ipv6_route_base_dict.update(dict_update)
        res = routepolicyapi.add_route_policy(**ipv6_route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add ipv6 route policy failed")

    def test_05_check_added_ipv6_pbr_in_route_policy(self):
        flag = False
        output = routepolicyapi.get_route_policy(version='ipv6')
        if output:
            for route in output['route_policies']:
                if '"name": "dest_network_ao"' in json.dumps(route):
                    flag = True
                    break
        Assertion.assert_equal(flag, True, "ERR: check added ipv6 route policy failed")

    def test_06_traffic_pass_through_new_ipv6_route(self):
        pc_run_dict = {
            'type': 'ping6',  # ping, cmd, http, script
            'pc': 'pc1',
            'eth': 'eth1',
            'des': Parameter.PC3_ETH1_IPV6
        }
        icmp_check_dict = {
            'src_ip': Parameter.PC1_ETH1_IPV6,
            'dst_ip': Parameter.PC3_ETH1_IPV6,
            'iface_in': 'X0',
            'iface_out': 'X2'
        }
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_Login, **pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_traffic_check(packets, **icmp_check_dict)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(checkres, True, "ERR: check traffic hit route failed.")

    def test_07_del_dest_ao_and_ipv6_pbr(self):
        res1 = routepolicyapi.del_route_policy_by_name('dest_network_test', version='ipv6')
        res2 = addressobjectapi.del_ao_by_name(name='dest_network_ao', version='ipv6')
        Assertion.assert_equal(res1 & res2, True, "ERR: del ipv6 pbr and network ao failed.")


# Excepted:a PBR entry with valid ipv6 network: destination AO type: Range can be added and traffic can hit this PBR
class TestBaseFun_TC7(Test):
    uuid = "SOSAIOT-TC-58545"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dest_range_ao(self):
        dest_range_ao = {
            'name': 'dest_range_ao',
            'zone': 'WAN',
            'object_type': 'range',
            'begin': '2002:1::18',
            'end': '2002:1::21',
        }
        rc = addressobjectapi.config_ipv6_addressobject(**dest_range_ao)
        Assertion.assert_equal(rc, True, "ERR: configure dest range AO failed")

    def test_03_add_ipv6_route_policy(self):
        dict_update = {
            "name": "dest_range_test",
            "interface": "X2",
            "destination": {"name": "dest_range_ao"},
            "gateway": {"name": "gw"}
        }
        ipv6_route_base_dict.update(dict_update)
        res = routepolicyapi.add_route_policy(**ipv6_route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add ipv6 route policy failed")

    def test_04_check_added_ipv6_pbr_in_route_policy(self):
        flag = False
        output = routepolicyapi.get_route_policy(version='ipv6')
        if output:
            for route in output['route_policies']:
                if '"name": "dest_range_ao"' in json.dumps(route):
                    flag = True
                    break
        Assertion.assert_equal(flag, True, "ERR: check added ipv6 route policy failed")

    def test_05_traffic_pass_through_new_ipv6_route(self):
        pc_run_dict = {
            'type': 'ping6',  # ping, cmd, http, script
            'pc': 'pc1',
            'eth': 'eth1',
            'des': Parameter.PC3_ETH1_IPV6
        }
        icmp_check_dict = {
            'src_ip': Parameter.PC1_ETH1_IPV6,
            'dst_ip': Parameter.PC3_ETH1_IPV6,
            'iface_in': 'X0',
            'iface_out': 'X2'
        }
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_Login, **pc_run_dict)
        (checkres, packet) = icmp_traffic_check(packets, **icmp_check_dict)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(checkres, True, "ERR: check traffic hit route failed.")

    def test_06_del_dest_ao_and_ipv6_pbr(self):
        res1 = routepolicyapi.del_route_policy_by_name('dest_range_test', version='ipv6')
        res2 = addressobjectapi.del_ao_by_name(name='dest_range_ao', version='ipv6')
        Assertion.assert_equal(res1 & res2, True, "ERR: del ipv6 pbr and range ao failed.")


# Excepted:Add a PBR entry with valid ipv6 network: destination AO type: Host can be added traffic can hit this PBR
class TestBaseFun_TC8(Test):
    uuid = "SOSAIOT-TC-58546"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dest_host_ao(self):
        dest_host_ao = {
            'name': 'dest_host_ao',
            'zone': 'WAN',
            'object_type': 'host',
            'ip': Parameter.PC3_ETH1_IPV6,
        }
        rc = addressobjectapi.config_ipv6_addressobject(**dest_host_ao)
        Assertion.assert_equal(rc, True, "ERR: add dest range AO failed")

    def test_03_add_ipv6_route_policy(self):
        dict_update = {
            "name": "dest_host_test",
            "interface": "X2",
            "destination": {"name": "dest_host_ao"},
            "gateway": {"name": "gw"}
        }
        ipv6_route_base_dict.update(dict_update)
        res = routepolicyapi.add_route_policy(**ipv6_route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add ipv6 route policy failed")

    def test_04_check_added_ipv6_pbr_in_route_policy(self):
        flag = False
        output = routepolicyapi.get_route_policy(version='ipv6')
        if output:
            for route in output['route_policies']:
                if '"name": "dest_host_ao"' in json.dumps(route):
                    flag = True
                    break
        Assertion.assert_equal(flag, True, "ERR: check added ipv6 route policy failed")

    def test_05_traffic_pass_through_new_ipv6_route(self):
        pc_run_dict = {
            'type': 'ping6',  # ping, cmd, http, script
            'pc': 'pc1',
            'eth': 'eth1',
            'des': Parameter.PC3_ETH1_IPV6
        }
        icmp_check_dict = {
            'src_ip': Parameter.PC1_ETH1_IPV6,
            'dst_ip': Parameter.PC3_ETH1_IPV6,
            'iface_in': 'X0',
            'iface_out': 'X2'
        }
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_Login, **pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_traffic_check(packets, **icmp_check_dict)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(checkres, True, "ERR: check traffic hit route failed.")

    def test_06_del_dest_ao_and_ipv6_pbr(self):
        res1 = routepolicyapi.del_route_policy_by_name('dest_host_test', version='ipv6')
        res2 = addressobjectapi.del_ao_by_name(name='dest_host_ao', version='ipv6')
        Assertion.assert_equal(res1 & res2, True, "ERR: del ipv6 pbr and dest ao failed.")


# TC11,TC24,TC25.TC19 run together
# Excepted:ipv6 PRB with regular interface can be added,traffic can hit it and can find location in Diagnostic
# Tool->Find Network Pat
class TestBaseFun_TC11(Test):
    uuid = "SOSAIOT-TC-58537"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_network_ao_and_host_ao(self):
        tag = []
        ao_src_host_pc2 = {
            "object_type": "host",
            "name": 'src_ipv6_host_pc2',
            "zone": 'LAN',
            "ip": '1001:2::10'
        }
        ao_gateway_x2 = {
            "object_type": "host",
            "name": 'gw_x2',
            "zone": 'WAN',
            "ip": '2001:1::169'
        }
        ao_gateway_x4 = {
            "object_type": "host",
            "name": 'gw_x4',
            "zone": 'WAN',
            "ip": '2001:2::169'
        }
        dest_ao_network_x3 = {
            'name': 'dest_network_ao_x3',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '2002:1::0',
            'mask': '/64',
        }
        dest_ao_network_other = {
            'name': 'dest_network_ao_other',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '2002:2::0',
            'mask': '/64',
        }
        ao_lists = [ao_src_host_pc2, ao_gateway_x2, ao_gateway_x4, dest_ao_network_x3, dest_ao_network_other]
        for ao in ao_lists:
            res = addressobjectapi.config_ipv6_addressobject(**ao)
            if res is False:
                logger.error(f'add ao {ao["name"]} failed')
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: configure AOs failed")

    def test_03_add_ipv6_route_policy(self):
        tag = []
        dict_update_1 = {
            "name": "pc1_to_pc3",
            "interface": "X2",
            "source": {"any": True},
            "destination": {"name": "dest_network_ao_x3"},
            "gateway": {"name": "gw_x2"}
        }
        dict_update_2 = {
            "name": "pc2_to_other",
            "interface": "X4",
            "service": {"group": "ICMPv6"},
            "source": {"name": "src_ipv6_host_pc2"},
            "destination": {"name": "dest_network_ao_other"},
            "gateway": {"name": "gw_x4"}
        }
        pbr_lists = [dict_update_1, dict_update_2]
        for pbr_list in pbr_lists:
            ipv6_route_base_dict.update(pbr_list)
            res = routepolicyapi.add_route_policy(**ipv6_route_policy_dict)
            if res is False:
                logger.error(f'add ipv6 pbr {pbr_list["name"]} failed')
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: Add ipv6 route policy failed")

    def test_04_check_added_ipv6_pbr_in_route_policy(self):
        output = routepolicyapi.get_route_policy(version='ipv6')
        dest_ao_lists = ['dest_network_ao_x3', 'dest_network_ao_other']
        flag = True if all(i in str(output) for i in dest_ao_lists) else False
        Assertion.assert_equal(flag, True, "ERR: check added ipv6 route policy failed")

    def test_05_traffic_pass_through_new_ipv6_route(self):
        pc_run_dict = {
            'type': 'ping6',  # ping, cmd, http, script
            'pc': 'pc1',
            'eth': 'eth1',
            'des': Parameter.PC3_ETH1_IPV6
        }
        icmp_check_dict = {
            'src_ip': Parameter.PC1_ETH1_IPV6,
            'dst_ip': Parameter.PC3_ETH1_IPV6,
            'iface_in': 'X0',
            'iface_out': 'X2'
        }
        (res, packets) = fw_packet_monitor_run(packetmonitorapi,PC1_Login, **pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_traffic_check(packets, **icmp_check_dict)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(checkres, True, "ERR: check traffic hit route failed.")
    
    def test_06_diagnostic_tool_find_network_path(self):
        flag = False
        res = diagnosticapi.diag_find_network_path(Parameter.PC3_ETH1_IPV6)
        logger.info(f'res is :{res}')
        output = diagnosticapi.get_find_network_path_Result()
        logger.info(f'diag find network path resutl is:{output}')
        if output:
            pathlist = [
                Parameter.PC3_ETH1_IPV6 + ' is located on the X2',
                'through the router at ' + Parameter.R_X2_IPV6,
                'through Ethernet address'
            ]
            logger.info(f'pathlist is : {pathlist}')
            flag = True if all(i in str(output['data']) for i in pathlist) else False
        Assertion.assert_equal(flag, True, "ERR: diag network path faied")


# Excepted:all ipv6 PBR routes are intact after FW rebooting. See Result 1
class TestBaseFun_TC24(Test):
    uuid = "SOSAIOT-TC-58540"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_restart_dut(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Restart DUT failed")

    def test_03_check_ipv6_pbr_settings(self):
        time.sleep(10)
        output = routepolicyapi.get_route_policy(version='v6')
        dest_ao_list = ['dest_network_ao_x3', 'dest_network_ao_other']
        ipv6routes = output['route_policies']
        flag = True if all(i in str(json.dumps(ipv6routes)) for i in dest_ao_list) else False
        Assertion.assert_equal(flag, True, "ERR: check ipv6 pbr settings failed.")


# Excepted:after importing the pefs file and FW rebooting, all ipv6 PBR routes should be intact.
class TestBaseFun_TC25(Test):
    uuid = "SOSAIOT-TC-58541"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_export_exp_file(self):
        logger.info('=> export exp file.')
        res = settingapi.export_setting_exp('/tmp/jlian_ipv6_pbr_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_03_restore_fw(self):
        logger.info('=> restore DUT.')
        res = settingapi.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_04_import_exp_file(self):
        logger.info('=> import exp file.')
        res = settingapi.import_setting_exp(
            filepath='/tmp/jlian_ipv6_pbr_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_05_check_ipv6_pbr_settings(self):
        time.sleep(10)
        output = routepolicyapi.get_route_policy(version='v6')
        dest_ao_list = ['dest_network_ao_x3', 'dest_network_ao_other']
        ipv6routes = output['route_policies']
        flag = True if all(i in str(json.dumps(ipv6routes)) for i in dest_ao_list) else False
        Assertion.assert_equal(flag, True, "ERR: check ipv6 pbr settings failed.")

    def test_06_verify_traffic(self):
        pingres = PC1_Login.send_command(f'ping6 -I eth1 -c 5 {Parameter.PC3_ETH1_IPV6_112}')
        logger.info(f'res is :{pingres}')
        res = True if "0% packet loss" in pingres else False
        Assertion.assert_equal(res, True, "ERR: verify traffic failed")


# Excepted: You should be able to edit an ip6 PBR entry by modifying it to another valid ipv6
# address/subnet/metric/comment etc.
class TestBaseFun_TC19(Test):
    uuid = "SOSAIOT-TC-58539"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_edit_ipv6_pbr(self):
        src_host_ao_new = {
            "object_type": "host",
            "name": 'src_ipv6_new',
            "zone": 'LAN',
            "ip": '1001:1::100'
        }
        dict_update = {
            "name": "pc1_to_pc3",
            "interface": "X2",
            "service": {"group": "ICMPv6"},
            "destination": {"name": "dest_network_ao_x3"},
            "source": {"name": "src_ipv6_new"},
            "gateway": {"name": "gw_x2"}
        }
        ipv6_route_base_dict.update(dict_update)
        logger.info(ipv6_route_policy_dict)
        res1 = addressobjectapi.config_ipv6_addressobject(**src_host_ao_new)
        res2 = routepolicyapi.edit_route_policy('pc1_to_pc3', version='V6', **ipv6_route_policy_dict)

        # initial dict
        initial_dict = {"service": {"any": True},
                        "source": {"any": True},
                        }
        ipv6_route_base_dict.update(initial_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: edit ipv6 route policy failed")

    def test_03_del_ipv6_pbr_and_ao(self):
        res1 = routepolicyapi.del_route_policy_by_name('pc1_to_pc3', version='ipv6')
        res2 = routepolicyapi.del_route_policy_by_name('pc2_to_other', version='ipv6')
        res3 = addressobjectapi.del_ao_by_name(name='dest_network_ao_x3', version='ipv6')
        res4 = addressobjectapi.del_ao_by_name(name='dest_network_ao_other', version='ipv6')
        Assertion.assert_equal(res1 & res2 & res3 & res4, True, "ERR: del ipv6 pbr and network ao failed.")


# Excepted:the route which with the longest prefix match will has higher priority and traffic will hit this route
class TestBaseFun_TC28(Test):
    uuid = "SOSAIOT-TC-58542"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_multiple_ipv6_pbr_with_different_prefix(self):
        ao_tag = []
        pbr_tag = []
        dest_ao_prefix_64 = {
            'name': 'dest_ao_prefix_64',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '2002:1::0',
            'mask': '/64',
        }
        dest_ao_prefix_96 = {
            'name': 'dest_ao_prefix_96',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '2002:1:0:0:1:2::0',
            'mask': '/96',
        }
        dest_ao_prefix_112 = {
            'name': 'dest_ao_prefix_112',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '2002:1:0:0:1:2:3:0',
            'mask': '/112',
        }
        dict_update_dest_64 = {
            "name": "dest_prefix_64",
            "interface": "X2",
            "destination": {"name": "dest_ao_prefix_64"},
            "gateway": {"name": "gw_x2"}
        }
        dict_update_dest_96 = {
            "name": "dest_prefix_96",
            "interface": "X2",
            "destination": {"name": "dest_ao_prefix_96"},
            "gateway": {"name": "gw_x2"}
        }
        dict_update_dest_112 = {
            "name": "dest_prefix_112",
            "interface": "X2",
            "destination": {"name": "dest_ao_prefix_112"},
            "gateway": {"name": "gw_x2"}
        }
        ao_lists = [dest_ao_prefix_64, dest_ao_prefix_96, dest_ao_prefix_112]
        pbr_lists = [dict_update_dest_64, dict_update_dest_96, dict_update_dest_112]
        for ao_list in ao_lists:
            aores = addressobjectapi.config_ipv6_addressobject(**ao_list)
            if aores is False:
                logger.error(f'add route policy {ao_list["name"]} failed')
            ao_tag.append(aores)
        for pbr_list in pbr_lists:
            ipv6_route_base_dict.update(pbr_list)
            pbrres = routepolicyapi.add_route_policy(**ipv6_route_policy_dict)
            if pbrres is False:
                logger.error(f'add route policy {pbr_list["name"]} failed')
            pbr_tag.append(pbrres)
        logger.info(f'ao_tag is:{ao_tag},pbr_tag is: {pbr_tag}')
        Assertion.assert_equal(all(ao_tag) & all(pbr_tag), True, "ERR: configure AOs and ipv6 pbr failed")

    def test_03_test_longgest_prefix_match(self):
        flag = False
        # get hit time in tsr before send traffic
        tsrrouting = diagnosticapi.get_tsr_route_policy_part(func='Network : Routing')
        hittimebefore = get_pbr_hit_time_in_tsr(tsrrouting, 'dest_prefix_112')
        logger.info(f'hittimebefore is :{hittimebefore}')
        remoteres = PC3_Login.send_command(f'ifconfig eth1 inet6 add {Parameter.PC3_ETH1_IPV6_112}/112')
        lanres = PC1_Login.send_command(f'ping6 -I eth1 -c 5 {Parameter.PC3_ETH1_IPV6_112}')
        res = True if "0% packet loss" in lanres else False
        logger.info(f'remoteres is :{remoteres},lanres is:{lanres}')
        if res:
            tsrrouting_1 = diagnosticapi.get_tsr_route_policy_part(func='Network : Routing')
            hittimeafter = get_pbr_hit_time_in_tsr(tsrrouting_1, 'dest_prefix_112')
            logger.info(f'hittimeafter is {hittimeafter}')
            logger.info(f'hittimebefore is {hittimebefore}')
            if hittimeafter != hittimebefore:
                flag = True

        # initial PC2 eth2
        remoteres = PC3_Login.send_command(f'ifconfig eth1 inet6 del {Parameter.PC3_ETH1_IPV6_112}/112')
        logger.info(f'remoteres is :{remoteres}')

        Assertion.assert_equal(flag, True, "ERR: test hit longest prefix match failed")
