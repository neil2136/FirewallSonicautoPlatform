from settings import *

fw = Firewall(Parameter.DUT_X0_IP, user='admin', password='password', supported_config_mode='api')
interface = network.InterfaceIPv4Api(fw)
inter_v6_obj = network.InterfaceIPv6Api(fw)
route_obj = network.RoutePolicyApi(fw)
ao_obj = network.AddressobjectsApi(fw)
nm_obj = network.NetworkMonitorApi(fw)
pkg_api = system.PacketmonitorApi(fw)
cdrouter = cdrouter_test.CDRTest(Parameter.NTA1000,path=Parameter.TESTPATH, case=Parameter.CASE1, conf=Parameter.CONF, log=Parameter.LOG)


class Test_06_Check_Route(Test):
    uuid = "SOSAIOT-TC-56631"
    description= 'Edit an IPv6 Network Monitor policy'

    def test_06_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_06_01_add_ipv6_network_monitor(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv6": {
                        "name": 'tc6',
                        'probe': {'target': {'name': 'probe_remote'}, 'type':{"tcp":{"port":1234,"explicit":True}}, 'interval': 5,},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'outbound_interface':'X0',
                        'next_hop':{'name':'probe_gw'},
                        'comment':'nm for tc6'
                    }
                }
            }]
        }
        rc = nm_obj.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add ipv6 network monitor policy fail .")

    def test_06_02_edit_network_monitor_policy(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv6": {
                        "name": 'tc6-new',
                        'probe': {'target': {'name': 'probe_remote'}, 'type':{ "ping": "explicit"}, 'interval': 5,},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'outbound_interface':'X0',
                        'next_hop':{'name':'probe_gw'},
                        'comment':'nm for tc6'
                    }
                }
            }]
        }
        rc = nm_obj.edit_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: edit network monitor fail.")

    def test_06_03_del_network_monitor_policy(self):
        rc = nm_obj.del_network_monitor(name='tc6-new',version='v6')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")


class Test_10_Check_TCP_Explicit_Route(Test):
    uuid = "SOSAIOT-TC-56626"
    description= 'Test Probe Type-TCP-Explicit Route'

    def test_10_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_10_01_add_nm_policy(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv6": {
                        "name": 'tc10',
                        'probe': {'target': {'name': 'probe_remote'}, 'type':{"tcp":{"port":Parameter.PORT,"explicit":True}}, 'interval': 5,},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'outbound_interface':'X1',
                        'next_hop':{'name':'probe_gw'},
                        'comment':'nm for tc10'
                    }
                }
            }]
        }
        rc = nm_obj.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add ipv6 network monitor policy fail .")    

    def test_10_02_run_cdrouter(self):
        cdrouter.run_case(backend=True, testvar=' -testvar swl_remoteHostTcpPort='+str(Parameter.PORT))
        time.sleep(20)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_10_03_capture_packet(self):
        pkg_api.start_capture()
        time.sleep(10)
        pkg_api.stop_capture()
        packets = pkg_api.export_captured_packets()
        # logger.info(packets)
        pkg_api.clear_packets()
        foundit = False
        for packet in re.split('Packet number: \d+\*', packets):
            if not re.search(r''+ Parameter.DUT_X1_IPV6 +'', packet) and not re.search(r''+ Parameter.PROBE_REMOTE +'', packet):
                continue
            pattern = 'TCP.*' + str(Parameter.PORT)
            logger.info(pattern)
            if re.search(r'' + pattern +'', packet, re.I):
                logger.info(f'Found TCP traffic with port {Parameter.PORT} send from x1 to {Parameter.PROBE_REMOTE}')
                foundit =True
                break
        if not foundit:
            logger.info('Packets as follows:')
            logger.info(packets)
        Assertion.assert_equal(foundit, True, f"ERR:  Not found TCP traffic from X1 to target {Parameter.PROBE_REMOTE}.")

    def test_10_04_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        Assertion.assert_equal(rc, True, "ERR: terminate cdrouter failed")

    def test_10_05_del_network_monitor_policy(self):
        rc = nm_obj.del_network_monitor(name='tc10',version='v6')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")


class Test_26_IPv6_probe(Test):
    uuid = "SOSAIOT-TC-56628"
    description= 'Test IPv6 Probe using in PBR policy'

    def test_26_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_26_01_add_nm_policy(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv6": {
                        "name": 'tc26',
                        'probe': {'target': {'name': 'probe_remote'}, 'type':{"tcp":{"port":80,"explicit":True}}, 'interval': 5,},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'outbound_interface':'X1',
                        'next_hop':{'name':'probe_gw'},
                        'comment':'nm for tc26'
                    }
                }
            }]
        }
        rc = nm_obj.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add ipv6 network monitor policy fail .") 

    @repeat_method(5)
    def test_26_02_check_network_monitor_policy_before_traffic(self):
        output = nm_obj.get_network_monitor_status()
        led = output['data']['netMonArray'][0]['led']
        if led != 'red':
            time.sleep(5)
        Assertion.assert_equal(led, 'red', f"ERR: The led should be red but {led}")

    def test_26_03_add_route_with_probe_up(self):
        route_dict = {"route_policies":
            [{"ipv6":
                {
                    "name":"tc26",
                    "comment":"",
                    "interface":"X0",
                    "metric":3,
                    "service":{"any":True},
                    "gateway":{"default":True},
                    "source":{"name":"X0 IPv6 Primary Static Address Subnet"},
                    "destination":{"name":"X1 IPv6 Primary Static Address Subnet"},
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"tc26",
                    "distance":{"auto":True},
                    "disable_when_probes_succeed":False,
                    "default_probe_state_up":True,
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]}
        rc = route_obj.add_route_policy(**route_dict)
        Assertion.assert_equal(rc, True, "ERR: add route policy with probe failed")

    @repeat_method(5)
    def test_26_04_get_route_policy(self):
        rc = route_obj.show_route_policy_status('tc26', version = 'ipv6')
        if rc != 'inactive':
            time.sleep(5)
        Assertion.assert_equal(rc, 'inactive', "ERR: route policy status should be disable")

    def test_26_05_run_cdrouter(self):
        cdrouter.run_case(backend=True, testvar=' -testvar swl_remoteHostTcpPort='+str(Parameter.PORT))
        time.sleep(20)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(10)
    def test_26_06_check_network_monitor_policy(self):
        output = nm_obj.get_network_monitor_status()
        led = output['data']['netMonArray'][0]['led']
        if led != 'green':
            time.sleep(15)
        Assertion.assert_equal(led, 'green', f"ERR: The led should be green but {led}")

    def test_26_07_get_route_policy(self):
        rc = route_obj.show_route_policy_status('tc26', version = 'ipv6')
        print(rc)    
        Assertion.assert_equal(rc, 'active', "ERR: route policy status should be enable")

    def test_26_08_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        Assertion.assert_equal(rc, True, "ERR: terminate cdrouter failed")

    @repeat_method(5)
    def test_26_09_check_network_monitor_policy(self):
        output = nm_obj.get_network_monitor_status()
        led = output['data']['netMonArray'][0]['led']
        if led != 'red':
            time.sleep(5)
        Assertion.assert_equal(led, 'green', f"ERR: The led should be red but {led}")

    def test_26_10_delete_route_policy(self):
        rc = route_obj.del_route_policy_by_name('tc26', version = 'ipv6')
        Assertion.assert_equal(rc, True, "ERR: delete route policy failed")

    def test_26_11_del_network_monitor_policy(self):
        rc = nm_obj.del_network_monitor(name='tc26',version='v6')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")


class Test_44_Verify_Monitor_Status(Test):
    uuid = "SOSAIOT-TC-56629"
    description= 'Verify the monitor status change from Down to UP when the probe target come back'
    pc1 = Host('localhost')

    def test_44_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '44')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_44_01_add_nm_policy(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv6": {
                        "name": 'tc44',
                        'probe': {'target': {'name': 'probe_remote'}, 'type':{ "ping": "explicit"}, 'interval': 5,},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'outbound_interface':'X1',
                        'next_hop':{'name':'probe_gw'},
                        'comment':'nm for tc44'
                    }
                }
            }]
        }
        rc = nm_obj.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add ipv6 network monitor policy fail .") 

    @repeat_method(5)
    def test_44_02_check_network_monitor_policy_before_traffic(self):
        output = nm_obj.get_network_monitor_status()
        led = output['data']['netMonArray'][0]['led']
        if led != 'red':
            time.sleep(5)
        Assertion.assert_equal(led, 'red', f"ERR: The led should be red but {led}")

    def test_44_03_run_cdrouter(self):
        cdrouter.run_case(backend=True)
        time.sleep(20)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_44_04_check_network_monitor_policy_after_pc_up(self):
        output = nm_obj.get_network_monitor_status()
        led = output['data']['netMonArray'][0]['led']
        if led != 'green':
            time.sleep(5)
        Assertion.assert_equal(led, 'green', f"ERR: The led should be red but {led}")  

    def test_44_05_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        Assertion.assert_equal(rc, True, "ERR: terminate cdrouter failed")

    @repeat_method(5)
    def test_44_06_check_network_monitor_policy_after_pc_down(self):
        output = nm_obj.get_network_monitor_status()
        led = output['data']['netMonArray'][0]['led']
        if led != 'red':
            time.sleep(5)
        Assertion.assert_equal(led, 'green', f"ERR: The led should be red but {led}")   

    def test_44_07_run_cdrouter(self):
        cdrouter.run_case(backend=True)
        time.sleep(20)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_44_08_check_network_monitor_policy_after_pc1_recover(self):
        output = nm_obj.get_network_monitor_status()
        led = output['data']['netMonArray'][0]['led']
        if led != 'green':
            time.sleep(5)
        Assertion.assert_equal(led, 'green', f"ERR: The led should be green but {led}")

    def test_44_09_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        Assertion.assert_equal(rc, True, "ERR: terminate cdrouter failed")

    def test_44_10_del_network_monitor_policy(self):
        rc = nm_obj.del_network_monitor(name='tc44',version='v6')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")
