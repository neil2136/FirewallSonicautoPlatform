from definition.settings import *
from definition.utils import *


# Excepted: GUI: OSPFv3 can be enabled on GUI
class TestBaseFun_TC1(Test):
    uuid = "SOSAIOT-TC-56640"
    description = show_testcase_info(TESTPLAN, '1514354', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514354')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_ospfv3_on_dut_X2(self):
        ospfv3_dict = {
            'interface': 'X2',
            'mode': 'enable',
            'area': '0',
        }
        res = dyroutingapi.set_ospf3(**ospfv3_dict)
        logger.info(f"config ospf on dut: {res}")
        Assertion.assert_equal(res, True, "ERR: Failed To enable ospfv3 on dut")

    def test_03_check_ospfv3_status_on_x2(self):
        (res, status) = check_interface_ospfv3_status(dyroutingapi, 'X2')
        logger.info(f'res is {res},ospfv3 neighbor status is : {status}')
        Assertion.assert_equal(status, 'down', "ERR: check X2 ospfv3 neighbor status failed")


# Excepted:DUT can establish neighborhood with another router.
class TestBaseFun_TC11(Test):
    uuid = "SOSAIOT-TC-56641"
    description = show_testcase_info(TESTPLAN, '1514355', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514355')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_ospfv3_settings_on_dut(self):
        ospfv3_setting_dict = {
            'route_metric': '110',
            'router_id': Parameter.UTM_ROUTER_ID,
        }
        res = dyroutingapi.ospf3_config(**ospfv3_setting_dict)
        logger.info(res)
        Assertion.assert_equal(res, True, "ERR: configure ospfv3 settings failed")

    def test_03_enable_ospfv3_on_remote_dut_x2(self):
        ospfv3_dict = {
            'interface': 'X2',
            'mode': 'enable',
            'area': '0',
        }
        ospfv3_setting_dict = {
            'route_metric': '110',
            'router_id': Parameter.REMOTE_ROUTER_ID,
        }
        res1 = r_dyroutingapi.set_ospf3(**ospfv3_dict)
        res2 = r_dyroutingapi.ospf3_config(**ospfv3_setting_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: enable ospfv3 failed on remote dut")

    def test_04_check_ospf_neighbor_on_cli(self):
        flag = False
        for i in range(3):
            time.sleep(20)
            showres = routecli.show_ospf3(mode='neighbor')
            if Parameter.REMOTE_ROUTER_ID in showres and 'Full' in showres:
                logger.info(f'ospf neighbors are established')
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: check ospf neighbor on cli failed")

    def test_05_check_ospf_neighbor_on_gui(self):
        (res, status) = check_interface_ospfv3_status(dyroutingapi, 'X2')
        logger.info(f'res is {res},ospfv3 neighbor status is : {status}')
        Assertion.assert_equal(status, 'full', "ERR: check X2 ospfv3 neighbor status on gui failed")


# Excepted: DUT can establish neighborhood with other router and can learn IPv6 routes from its neighbor router
class TestBaseFun_TC12(Test):
    uuid = "SOSAIOT-TC-56642"
    description = show_testcase_info(TESTPLAN, '1514356', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514356')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_redistribute_static_and_connected_routes_on_remote_dut(self):
        ospfv3_setting_dict = {
            'router_id': Parameter.REMOTE_ROUTER_ID,
            'static_route': 'on',
            'connect_network': 'on',
        }
        res = r_dyroutingapi.ospf3_config(**ospfv3_setting_dict)
        Assertion.assert_equal(res, True, "ERR:redistribute static and connected routes on remote dut failed")

    def test_03_check_ipv6_route_table_on_gui(self):
        time.sleep(30)
        flag = False
        dyroutes = routepolicyapi.route_policies_reporting(version='v6', r_type='dynamic')
        logger.info(f'dynamic route policyies is:{dyroutes}')
        if dyroutes:
            for route in dyroutes:
                if f'"destination": "{Parameter.REMOTE_DEST_PREFIX}"' in json.dumps(route):
                    flag = True
                    break
        Assertion.assert_equal(flag, True, "ERR: check ipv6 dynamic route policy on gui failed")

    def test_04_check_ipv6_routes_on_cli(self):
        showres = r_routecli.show_ospf3_database(mode='external')
        flag = True if f'Prefix: {Parameter.REMOTE_DEST_PREFIX}' in showres and f'Prefix: {Parameter.R_X3_V6_PREFIX}' in showres else False
        Assertion.assert_equal(flag, True, "ERR: check dynamic ipv6 route policy in cli failed")


# Excepted: IPv6 traffic that hit the learnt OSPFv3 routes could be forwarded properly
class TestBaseFun_TC46(Test):
    uuid = "SOSAIOT-TC-56650"
    description = show_testcase_info(TESTPLAN, '1514366', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514366')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_03_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'X0,X2',
                'ether_types': 'ipv6',
                'ip_types': 'icmpv6',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_04_check_traffic_hit_learnt_ospfv3_routes(self):
        clearres = packetmonitorapi.clear_packets()
        startres = packetmonitorapi.start_capture()
        res = PC1_Login.ping6('200:1:1::100', num=2)
        time.sleep(30)
        logger.info(res)
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'clearres is :{clearres},start packets is :{startres},stop packets on FW result: {stopres}')
        resp = packetmonitorapi.export_captured_packets()
        logger.info(resp)
        check_traffic_dict = {
            'iface_in': '--',
            'iface_out': 'X2',
            'src_ip': Parameter.PC1_ETH1_IPV6,
            'dst_ip': Parameter.REMOTE_DEST_HOST,
        }
        checkres = icmpv6_traffic_hit_check(resp, **check_traffic_dict)
        Assertion.assert_equal(checkres, True, "ERR: check traffic hit learnt OSPFv3 routes failed")


# Excepted: static ipv6 routes can be redistribute out
class TestBaseFun_TC13(Test):
    uuid = "SOSAIOT-TC-56643"
    description = show_testcase_info(TESTPLAN, '1514357', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514357')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_redistribute_static_route_on_dut(self):
        ospfv3_setting_dict = {
            'router_id': Parameter.UTM_ROUTER_ID,
            'static_route': 'on',
        }
        res = dyroutingapi.ospf3_config(**ospfv3_setting_dict)
        Assertion.assert_equal(res, True, "ERR:redistribute static routes failed")

    def test_03_check_route_policies_on_remote_dut_gui(self):
        time.sleep(60)
        flag = False
        dyroutes = r_routepolicyapi.route_policies_reporting(version='v6', r_type='dynamic')
        logger.info(f'dynamic route policyies is:{dyroutes}')
        if dyroutes:
            for route in dyroutes:
                if f'"destination": "{Parameter.UTM_DEST_PREFIX}"' in json.dumps(route):
                    flag = True
                    break
        Assertion.assert_equal(flag, True, "ERR: check ipv6 dynamic routes on remote dut failed")

    def test_04_check_ospfv3_database_remote_on_cli(self):
        showres = r_routecli.show_ospf3_database(mode='external')
        flag = True if f'Prefix: {Parameter.UTM_DEST_PREFIX}' in showres else False
        Assertion.assert_equal(flag, True, "ERR: check ospfv3 datebase on remote dut in CLI failed")

    def test_05_disable_redistribute_static_route_on_dut(self):
        ospfv3_setting_dict = {
            'router_id': Parameter.UTM_ROUTER_ID,
            'static_route': 'off',
        }
        res = dyroutingapi.ospf3_config(**ospfv3_setting_dict)
        Assertion.assert_equal(res, True, "ERR:disable redistribute static routes on remote dut failed")


# Excepted: connected Routes can be redistribute out
class TestBaseFun_TC14(Test):
    uuid = "SOSAIOT-TC-56644"
    description = show_testcase_info(TESTPLAN, '1514358', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514358')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_redistribute_connnected_route_on_dut(self):
        ospfv3_setting_dict = {
            'router_id': Parameter.UTM_ROUTER_ID,
            'connect_network': 'on',
        }
        res = dyroutingapi.ospf3_config(**ospfv3_setting_dict)
        Assertion.assert_equal(res, True, "ERR:redistribute connected routes failed")

    def test_03_check_dynamic_routes_on_remote_dut_gui(self):
        time.sleep(60)
        dyroutes = r_routepolicyapi.route_policies_reporting(version='v6', r_type='dynamic')
        logger.info(f'dynamic route policyies is:{dyroutes}')
        destlist = ['1001:1::/64', '1001:2::/64']
        flag = True if all(i in str(dyroutes) for i in destlist) else False
        Assertion.assert_equal(flag, True, "ERR: check the dynamic routes on remote dut on GUI failed")

    def test_04_check_ospfv3_database_remote_on_cli(self):
        showres = r_routecli.show_ospf3_database(mode='external')
        flag = True if 'Prefix: 1001:1::/64' in showres and 'Prefix: 1001:2::/64' in showres else False
        Assertion.assert_equal(flag, True, "ERR: check ospfv3 datebase in CLI failed")


# Excepted: Download TSR and check all OSPFv3 related information.
class TestBaseFun_TC143(Test):
    uuid = "SOSAIOT-TC-56651"
    description = show_testcase_info(TESTPLAN, '1514367', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514367')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_get_tsr_dynamic_settings(self):
        tsrres = diagnosticapi.get_tsr_dynamic_routing_protocol_setting('OSPFv3')
        logger.info(f'ospfv3 settings in tsr is:{tsrres}')
        flag = True if 'ipv6 router ospf area 0' in tsrres else False
        Assertion.assert_equal(flag, True, "ERR: check ospfv3 settings in tsr failed")


# Excepted: After a reboot all OSPFv3 settings and status remain intact
class TestBaseFun_TC33(Test):
    uuid = "SOSAIOT-TC-56647"
    description = show_testcase_info(TESTPLAN, '1514362', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514362')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_restart_dut(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Restart DUT failed")

    def test_03_check_ospfv3_neighbor_status(self):
        (res, status) = check_interface_ospfv3_status(dyroutingapi, 'X2')
        logger.info(f'res is {res},ospfv3 neighbor status is : {status}')
        Assertion.assert_equal(status, 'full', "ERR: check X2 ospfv3 neighbor status failed")

    def test_04_check_route_table_on_gui(self):
        dyroutes = routepolicyapi.route_policies_reporting(version='v6', r_type='dynamic')
        logger.info(f'dynamic route policyies is:{dyroutes}')
        destlist = [Parameter.REMOTE_DEST_PREFIX, Parameter.R_X3_V6_PREFIX]
        flag = True if all(i in str(dyroutes) for i in destlist) else False
        Assertion.assert_equal(flag, True, "ERR: check ipv6 route table on gui failed")


# Excepted: OSPFv3 can be enabled in CLI
class TestBaseFun_TC16(Test):
    uuid = "SOSAIOT-TC-56645"
    description = show_testcase_info(TESTPLAN, '1514360', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514360')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_inital_ospf_settings_in_gui(self):
        ospfv3_dict = {
            'interface': 'X2',
            'mode': 'disable',
            'area': '0',
        }
        ospfv3_setting_dict = {
            'route_metric': '110',
            'router_id': '10.0.0.1',
            'static_route': 'off',
            'connect_network': 'off',
        }
        res1 = dyroutingapi.set_ospf3(**ospfv3_dict)
        res2 = dyroutingapi.ospf3_config(**ospfv3_setting_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: inital ospfv3 settings in GUI failed")

    def test_03_configure_ospfv3_in_cli(self):
        configure_ospfv3_dict = {
            'if': 'X2',
            'type': 'enable',
            'area': '0',
        }
        res = routecli.config_ospf3(**configure_ospfv3_dict)
        logger.info(f'res is {res}')
        showres = routecli.show_ospf3()
        logger.info(f'showres is:{showres}')
        flag = True if 'ipv6 router ospf area 0' in showres else False
        Assertion.assert_equal(flag, True, "ERR: configure OSPFv3 in CLI failed")

    def test_04_check_ospfv3_neighbor_in_cli(self):
        flag = False
        for i in range(3):
            time.sleep(20)
            showres = routecli.show_ospf3(mode='neighbor')
            if 'Full' in showres:
                logger.info(f'ospf neighbors are established')
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: check ospf neighbor in cli is failed")


# Excepted: Config an interface as OSPFv3 passive mode. 3DUT
class TestBaseFun_TC23(Test):
    uuid = "SOSAIOT-TC-56646"
    description = show_testcase_info(TESTPLAN, '1514361', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514361')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_ospfv3_passive_on_remote(self):
        ospfv3_dict = {
            'interface': 'X3',
            'mode': 'passive',
            'area': '0',
        }
        res = dyroutingapi.set_ospf3(**ospfv3_dict)
        logger.info(f"config ospf on dut: {res}")
        Assertion.assert_equal(res, True, "ERR: configure x3 passive mode failed on dut")

    def test_03_check_database_ospf_link_on_dut_in_cli(self):
        showres = routecli.show_ospf3_database(mode='link')
        flag = True if 'Link-LSA (Interface X3)' in showres and 'Prefix: 1001:2::/64' in showres else False
        Assertion.assert_equal(flag, True, "ERR: check ospfv6 database link on dut failed")

    def test_04_check_ipv6_routes_on_remote_dut(self):
        showres = r_routecli.show_ospf3(mode='routes')
        flag=True if 'O  1001:2::/64' in showres else False
        Assertion.assert_equal(flag, True, "ERR: check ospfv6 routes on remote dut failed")

    def test_05_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'X3',
                'ether_types': 'ipv6',
                'ip_types': 'ospf',
                'destination_ips': 'ff02::5',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_06_check_ospfv3_packets_on_dut_x3(self):
        clearres = packetmonitorapi.clear_packets()
        startres = packetmonitorapi.start_capture()
        time.sleep(30)
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'clearres is :{clearres},start packets is :{startres},stop packets on FW result: {stopres}')
        resp = packetmonitorapi.export_captured_packets()
        logger.info(resp)
        ospfv3_hello_out_dict = {
            'iface_in': '--',
            'iface_out': 'X3'
        }
        num = check_ospfv3_hello_packets_num(resp, **ospfv3_hello_out_dict)
        logger.info(f'ospfv3 hello packets sent from vlan interface num is:{num}')
        flag = True if num == 0 else False
        Assertion.assert_equal(flag, True, "ERR: Config packet monitor failed")

    def test_07_disable_ospfv3_on_x3(self):
        ospfv3_dict = {
            'interface': 'X3',
            'mode': 'disable',
            'area': '0',
        }
        res = dyroutingapi.set_ospf3(**ospfv3_dict)
        logger.info(f"config ospf on dut: {res}")
        Assertion.assert_equal(res, True, "ERR: disable ospfv3 for X3 on dut")


# Excepted: DUT can establish neighborhood with another router with specified hello-interval time
class TestBaseFun_TC36(Test):
    uuid = "SOSAIOT-TC-56648"
    description = show_testcase_info(TESTPLAN, '1514363', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514363')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_ospfv3_hello_interva_on_dut(self):
        ospfv3_dict = {
            'interface': 'X2',
            'mode': 'enable',
            'hello_interval': 5,
        }
        res = dyroutingapi.set_ospf3(**ospfv3_dict)
        logger.info(f"config ospf on dut: {res}")
        Assertion.assert_equal(res, True, "ERR: configure ospf hello interval time")

    def test_03_config_ospfv3_hello_interval_on_remote_dut(self):
        ospfv3_dict = {
            'interface': 'X2',
            'mode': 'enable',
            'hello_interval': 5,
        }
        res = r_dyroutingapi.set_ospf3(**ospfv3_dict)
        logger.info(f"config ospf on dut: {res}")
        Assertion.assert_equal(res, True, "ERR: configure ospf hello interval time failed")

    def test_04_check_ospfv3_neighbor_status(self):
        time.sleep(50)
        (res, status) = check_interface_ospfv3_status(dyroutingapi, 'X2')
        logger.info(f'res is {res},ospfv3 neighbor status is : {status}')
        Assertion.assert_equal(status, 'full', "ERR: check X2 ospfv3 neighbor status failed")

    def test_05_restore_ospfv4_configure(self):
        utm_ospfv3_dict = {
            'interface': 'X2',
            'mode': 'disable',
            'hello_interval': 10,
        }
        r_ospfv3_dict = {
            'interface': 'X2',
            'mode': 'disable',
            'hello_interval': 10,
        }
        res1 = dyroutingapi.set_ospf3(**utm_ospfv3_dict)
        res2 = r_dyroutingapi.set_ospf3(**r_ospfv3_dict)
        logger.info(f"config ospf on dut: {res1},on remote is :{res2}")
        Assertion.assert_equal(res1 & res2, True, "ERR: configure ospf hello interval time")


# Excepted:  OSPFv3 can works on vlan sub-interface
class TestBaseFun_TC37(Test):
    uuid = "SOSAIOT-TC-56649"
    description = show_testcase_info(TESTPLAN, '1514364', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514364')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_ospfv3_on_utm_X4(self):
        ospfv3_dict = {
            'interface': f'X4:V{UTM_X4_VLAN1_ID}',
            'mode': 'enable',
            'area': '0',
        }
        ospfv3_setting_dict = {
            'route_metric': '110',
            'router_id': Parameter.UTM_ROUTER_ID,
            'static_route': 'on',
            'connect_network': 'on',
        }
        res1 = dyroutingapi.set_ospf3(**ospfv3_dict)
        res2 = dyroutingapi.ospf3_config(**ospfv3_setting_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: Failed To enable ospf on dut")

    def test_03_enable_ospfv3_on_remote_X4(self):
        ospfv3_dict = {
            'interface': f'X4:V{REMOTRGEN7_X4_VLAN1_ID}',
            'mode': 'enable',
            'area': '0',
        }
        ospfv3_setting_dict = {
            'route_metric': '110',
            'router_id': Parameter.REMOTE_ROUTER_ID,
            'static_route': 'on',
            'connect_network': 'on',
        }
        res1 = r_dyroutingapi.set_ospf3(**ospfv3_dict)
        res2 = r_dyroutingapi.ospf3_config(**ospfv3_setting_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: Failed To enable ospf on remote")

    def test_04_check_ospf_neighbor_on_gui(self):
        time.sleep(60)
        (res, status) = check_interface_ospfv3_status(dyroutingapi, f'X4:V{UTM_X4_VLAN1_ID}')
        logger.info(f'res is {res},ospfv3 neighbor status is : {status}')
        Assertion.assert_equal(status, 'full', "ERR: check ospfv3 neighbor status on vlan interface failed")

    def test_05_check_ipv6_route_table_on_gui(self):
        flag = False
        dyroutes = routepolicyapi.route_policies_reporting(version='v6', r_type='dynamic')
        logger.info(f'dynamic route policyies is:{dyroutes}')
        if dyroutes:
            logger.info(json.dumps(dyroutes))
            logger.info(f'"destination": "{Parameter.REMOTE_DEST_PREFIX}"')
            for route in dyroutes:
                if f'"destination": "{Parameter.REMOTE_DEST_PREFIX}"' in json.dumps(route) and '"metric": 110' in json.dumps(route):
                    flag = True
                    break
        Assertion.assert_equal(flag, True, "ERR: check ipv6 route policy failed")

    def test_06_show_ospfv3_neighbor(self):
        flag = False
        for i in range(3):
            time.sleep(20)
            showres = routecli.show_ospf3(mode='neighbor')
            if Parameter.REMOTE_ROUTER_ID in showres and 'Full' in showres:
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: check ospfv6 neighbor failed")


    def test_07_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': f'X4:V{UTM_X4_VLAN1_ID}',
                'ether_types': 'ipv6',
                'ip_types': 'ospf',
                'destination_ips': 'ff02::5',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_08_check_ospf_hello_packets_num_send_out_on_vlan_if(self):
        clearres = packetmonitorapi.clear_packets()
        startres = packetmonitorapi.start_capture()
        time.sleep(30)
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'clearres is :{clearres},start packets is :{startres},stop packets on FW result: {stopres}')
        resp = packetmonitorapi.export_captured_packets()
        logger.info(resp)
        ospfv3_hello_check_dict = {
            'iface_in': '--',
            'iface_out': f'X4:V{UTM_X4_VLAN1_ID}'
        }
        num = check_ospfv3_hello_packets_num(resp, **ospfv3_hello_check_dict)
        logger.info(f'ospfv3 hello packets sent from vlan interface num is:{num}')
        flag = True if 2 <= num <= 4 else False
        Assertion.assert_equal(flag, True, "ERR: Config packet monitor failed")

    def test_09_disable_ospfv3_0n_utm_and_remote(self):
        ospfv3_dict = {
            'interface': f'X4:V{REMOTRGEN7_X4_VLAN1_ID}',
            'mode': 'disable',
            'area': '0',
        }
        res1 = dyroutingapi.set_ospf3(**ospfv3_dict)
        res2 = r_dyroutingapi.set_ospf3(**ospfv3_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: Failed To enable osfp on dut")