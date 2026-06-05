from definition.settings import *
from definition.utils import *


# Excepted: pc2 can respond to ARP request to x1 successful.
class TestDHCPClient_TC01(Test):
    uuid = "SOSAIOT-TC-55832"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x1',
                'ether_types': 'arp',
                # 'ip_types': 'icmp',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_03_get_x1_default_gateway_and_x1_dhcp_ip(self):
        flag = False
        for i in range(10):
            getx1res = interfacev4api.get_interface_address('X1')
            logger.info(getx1res)
            if getx1res['default_gateway'] != Parameter.ALL0IP and getx1res["ip_address"] != Parameter.ALL0IP:
                flag = True
                Parameter.X1_GW = getx1res['default_gateway']
                Parameter.X1_DHCP_IP = getx1res["ip_address"]
                break
            else:
                logger.info(f"get x1 gateway or ip failed for {i} time")
                time.sleep(60)
        Assertion.assert_equal(flag, True, "ERR: get x1 default gateway and x1 dhcp ip failed")

    @repeat_method(3)
    def test_04_check_arp_reply(self):
        checkres = False
        logger.info(f'Parameter.X1_GW is:{Parameter.X1_GW}')
        logger.info(f'Parameter.X1_DHCP_IP is:{Parameter.X1_DHCP_IP}')
        if Parameter.X1_GW != Parameter.ALL0IP and Parameter.X1_DHCP_IP != Parameter.ALL0IP:
            stratres = packetmonitorapi.start_capture()
            logger.info(f'start packet monitor result: {stratres}')
            clearres = packetmonitorapi.clear_packets()
            logger.info(f'clear packet monitor result: {clearres}')
            flushres = arpapi.delete_arp_caches()
            if flushres:
                time.sleep(10)
                stopres = packetmonitorapi.stop_capture()
                logger.info(f'stop packet monitor result: {stopres}')
                resp = packetmonitorapi.export_captured_packets()
                checkres, output = arp_reply_check(resp, Parameter.X1_GW, Parameter.X1_DHCP_IP)
                logger.info(output)
            else:
                logger.error('flush arp entries failed')
        else:
            logger.error('get x1 default gateway or x1 dhcp ip failed')
        Assertion.assert_equal(checkres, True, "ERR: no arp reply received.")


# Excepted: x1 sends DHCP REQUEST for same IP address successful
class TestDHCPClient_TC02(Test):
    uuid = "SOSAIOT-TC-55838"
    description = show_testcase_info(Parameter.TESTPLAN, '02', description=True)['title']
    # dhcpconfres = False

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_change_dhcp_lease_time_on_pc2(self):
        res = config_dhcp_lease_time_on_pc2('60', '120')
        global dhcpconfres
        dhcpconfres = res
        Assertion.assert_equal(res, True, "ERR: change dhcp config failed")

    def test_03_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x1',
                'ether_types': 'ip',
                'ip_types': 'udp ',
                'destination_ports': '67,68'
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_04_check_dhcp_request_packet(self):
        checkres = False
        if dhcpconfres:
            getx1res = interfacev4api.get_interface_address('X1')
            curx1ip = getx1res["ip_address"]
            if curx1ip != Parameter.ALL0IP:
                clickres = interfacev4api.click_dhcp_release(name='X1')
                time.sleep(10)
                if clickres:
                    getx1res = interfacev4api.get_interface_address('X1')
                    newx1ip = getx1res["ip_address"]
                    packetmonitorapi.start_capture()
                    packetmonitorapi.clear_packets()
                    time.sleep(120)
                    packetmonitorapi.stop_capture()
                    resp = packetmonitorapi.export_captured_packets()
                    checkres, output = dhcp_request_check(resp, newx1ip, PC2_ETH1_IP)
                    logger.info(output)
                else:
                    logger.error('click dhcp release failed')
            else:
                logger.error('current x1 ip address is full zero')
        else:
            logger.error('change dhcp config on pc2 failed')
        Assertion.assert_equal(checkres, True, "ERR: check dhcp request with same ip before expire failed")

    def test_05_restore_dhcp_lease_time_on_pc2(self):
        output = config_dhcp_lease_time_on_pc2('21600', '43200')
        if output is False:
            logger.error('change dhcp lease failed')
        Assertion.assert_equal(True, True, "ERR: restore dhcp config failed")


# Excepted: X1 interface as primary wan can get dhcp lease from the dhcp server
class TestDHCPClient_TC15(Test):
    uuid = "SOSAIOT-TC-55833"
    description = show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_x3_as_secondary_wan_with_dhcp_mode(self):
        output = interfacev4api.config_interface(**x3_dhcp_dict)
        Assertion.assert_equal(output, True, "ERR: Configure X3 to DHCP mode failed")

    def test_03_primary_wan_x1_get_address(self):
        flag = False
        for i in range(3):
            getx1res = interfacev4api.get_interface_address('X1')
            x1ip = getx1res['ip_address']
            if x1ip != Parameter.ALL0IP:
                flag = True
                Parameter.X1_GW = getx1res['default_gateway']
                break
            else:
                logger.info(f"x1 has no ip : {x1_ip}")
                interfacev4api.click_dhcp_renew(name='X1')
                time.sleep(10)
        Assertion.assert_equal(flag, True, "ERR: X1 get dhcp address failed")

    def test_04_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        logger.info(Parameter.X1_GW)
        monitor_conf_dict = {
            'monitor_filter': {
                'destination_ips': Parameter.X1_GW,
                'interfaces': 'x0,x1',
                'ether_types': 'ip',
                'ip_types': 'icmp ',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_05_check_icmp_packets_from_lan_to_primary_wan(self):
        checkres = False
        if Parameter.X1_GW != Parameter.ALL0IP and PC1_ETH0_IP != Parameter.ALL0IP:
            packetmonitorapi.start_capture()
            packetmonitorapi.clear_packets()
            pc1login.ping_from_eth(ip=Parameter.X1_GW, eth='eth0')
            time.sleep(20)
            packetmonitorapi.stop_capture()
            resp = packetmonitorapi.export_captured_packets()
            checkres, output = icmp_request_check(resp, PC1_ETH0_IP, Parameter.X1_GW, 'X1')
            logger.info(output)
        else:
            logger.error('get x1 gateway or pc1 eth0 ip failed')
        Assertion.assert_equal(checkres, True, "ERR: check dhcp request with same ip before expire.")


# Excepted: x3 as secondary wan can get dhcp lease from the dhcp server, and traffic is working
class TestDHCPClient_TC16(Test):
    uuid = "SOSAIOT-TC-55833"
    description = show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_x3_as_secondary_wan(self):
        output = interfacev4api.config_interface(**x3_dhcp_dict)
        Assertion.assert_equal(output, True, "ERR: Configure X3 status to DHCP failed")

    def test_03_secondary_wan_x3_get_address(self):
        flag = False
        time.sleep(10)
        for i in range(3):
            getx3res = interfacev4api.get_interface_address('X3')
            if getx3res['ip_address'] != Parameter.ALL0IP:
                flag = True
                Parameter.X3_GW = getx3res['default_gateway']
                break
            else:
                logger.info(f"x3 has no ip address,try to click renew button for the {i} time")
                interfacev4api.click_dhcp_renew(name='X3')
                time.sleep(15)
        Assertion.assert_equal(flag, True, "ERR: get X3 dhcp address failed")

    def test_04_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'destination_ips': Parameter.X3_GW,
                'interfaces': 'x0,x3',
                'ether_types': 'ip',
                'ip_types': 'icmp ',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_05_check_icmp_packets_from_lan_to_secondary_wan(self):
        checkres = False
        if Parameter.X3_GW != Parameter.ALL0IP and PC1_ETH0_IP != Parameter.ALL0IP:
            packetmonitorapi.start_capture()
            packetmonitorapi.clear_packets()
            # pc1login.send_command(f"ping {Parameter.X3_GW} -c 5 -I eth0")
            pc1login.ping_from_eth(ip=Parameter.X3_GW, eth='eth0')
            time.sleep(20)
            packetmonitorapi.stop_capture()
            resp = packetmonitorapi.export_captured_packets()
            checkres, output = icmp_request_check(resp, PC1_ETH0_IP, Parameter.X3_GW, 'X3')
            logger.info(output)
        else:
            logger.error('get x3 gateway or pc1 eth0 ip failed')
        Assertion.assert_equal(checkres, True, "ERR: icmp traffic from lan to secondary wan failed")

    def test_06_unassign_seconday_wan(self):
        unassigres = interfacev4api.unassign_interface(interface='x3')
        if unassigres is False:
            logger.error('unassign secondary wan failed')
        Assertion.assert_equal(True, True, "ERR: unassign seconday wan x3 failed")


# Excepted:The Host Name of X1 can be changed successfully
class TestDHCPClient_TC18(Test):
    uuid = "SOSAIOT-TC-55836"
    description = show_testcase_info(Parameter.TESTPLAN, '18', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_input_x1_hostname(self):
        flag = False
        x1_dhcp_dict['dhcp_hostname'] = 'tc18_hostname_test01'
        res = interfacev4api.config_interface(**x1_dhcp_dict)
        getx1res = interfacev4api.get_interface_status('X1')
        try:
            if res and getx1res['interfaces'][0]:
                x1hostname = getx1res['interfaces'][0]['ipv4']['ip_assignment']['mode']['dhcp']['hostname']
                logger.info(x1hostname)
                if x1hostname == 'tc18_hostname_test01':
                    flag = True
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(flag, True, "ERR: input hostname succeeds")

    def test_03_check_hostname_on_pc2(self):
        time.sleep(30)
        checkres = check_dhcp_hostname_on_pc2('tc18_hostname_test01')
        Assertion.assert_equal(checkres, True, "ERR: check hostname failed on pc2")

    def test_04_inital_x1_dhcp_hostname(self):
        x1_dhcp_dict['dhcp_hostname'] = ''
        res = interfacev4api.config_interface(**x1_dhcp_dict)
        if res is False:
            logger.error('inital x1 dhcp hostname failed')
        Assertion.assert_equal(True, True, "ERR: inital x1 hostname failed ")


# Excepted:It is ok to manage X1 interface from http, https, ssh, and it is pingable
class TestDHCPClient_TC20(Test):
    uuid = "SOSAIOT-TC-55839"
    description = show_testcase_info(Parameter.TESTPLAN, '20', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_get_X1_address(self):
        flag = False
        for i in range(3):
            getx1res = interfacev4api.get_interface_address('X1')
            x1ip = getx1res['ip_address']
            if x1ip != Parameter.ALL0IP:
                flag = True
                Parameter.X1_DHCP_IP = x1ip
                break
            else:
                logger.info('x1 has no ip,try to click renew button')
                interfacev4api.click_dhcp_renew(name='X1')
                time.sleep(10)
        Assertion.assert_equal(flag, True, "ERR: X1 get dhcp address failed")

    def test_03_verify_ping_DUT_x1(self):
        time.sleep(20)
        flag = False
        if Parameter.X1_DHCP_IP != Parameter.ALL0IP:
            for i in range(3):
                flag = pc2login.ping_from_eth(ip=Parameter.X1_DHCP_IP, eth='eth1')
                if flag:
                    break
                else:
                    time.sleep(5)
        else:
            logger.error('not ip address in X1, skip ping step')
        Assertion.assert_equal(flag, True, "ERR: ERR: Ping X1 failed")

    def test_04_verify_ssh_DUT_x1(self):
        flag = False
        command = 'python3 ' + script_path + '/ssh_login_X1.py -i ' + Parameter.X1_DHCP_IP
        output = pc2login.send_command(command)
        if re.search(r'True', output):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ssh X1 ip failed")

    def test_05_verify_https_DUT_x1(self):
        fw.api_logout()
        flag = False
        command = 'python3 ' + script_path + 'login_logout_DUT_from_X1.py -i ' + Parameter.X1_DHCP_IP + ' -a login'
        output = pc2login.send_command(command)
        if re.search(r'True', output):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: https X1 ip failed")


# Excepted: X1 can release ip address succussfully
class TestDHCPClient_TC21(Test):
    uuid = "SOSAIOT-TC-55840"
    description = show_testcase_info(Parameter.TESTPLAN, '21', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_release_x1_ip(self):
        flag = False
        getx1res = interfacev4api.get_interface_address('X1')
        x1ipbefore = getx1res["ip_address"]
        if x1ipbefore != Parameter.ALL0IP:
            for i in range(3):
                time.sleep(10)
                clickres = interfacev4api.click_dhcp_release(name='X1')
                time.sleep(2)
                if clickres:
                    getx1res1 = interfacev4api.get_interface_address('X1')
                    x1ipafter = getx1res1["ip_address"]
                    if x1ipafter == Parameter.ALL0IP:
                        flag = True
                        break
                    else:
                        logger.info('x1 still has ip after click release button')
                else:
                    logger.info('click x1 release button failed')
        else:
            logger.error('x1 has no ip address')
        Assertion.assert_equal(flag, True, "ERR: release X1 DHCP ip failed")


# Excepted:X1 interface can get a new ip address after click the renew button
class TestDHCPClient_TC22(Test):
    uuid = "SOSAIOT-TC-55841"
    description = show_testcase_info(Parameter.TESTPLAN, '22', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_renew_x1_ip(self):
        time.sleep(15)
        flag = False
        getx1res1 = interfacev4api.get_interface_address('X1')
        logger.info(f"getx1res1:{getx1res1['lease_expires']}")
        if getx1res1["ip_address"] != Parameter.ALL0IP:
            for i in range(3):
                clickres = interfacev4api.click_dhcp_release(name='X1')
                time.sleep(5)
                clickres &= interfacev4api.click_dhcp_renew(name='X1')
                if clickres:
                    time.sleep(15)
                    getx1res2 = interfacev4api.get_interface_address('X1')
                    logger.info(f"getx1res2:{getx1res2['lease_expires']}")
                    if getx1res1['lease_expires'] != getx1res2['lease_expires']:
                        flag = True
                        break
                else:
                    logger.info('click x1 renew button failed')
        else:
            logger.error('not ip address in X1')
        Assertion.assert_equal(flag, True, "ERR: renew x1 dhcp ip failed")
