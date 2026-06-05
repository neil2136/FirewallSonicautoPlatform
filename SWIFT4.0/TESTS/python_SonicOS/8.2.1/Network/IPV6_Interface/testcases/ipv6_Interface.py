from lib.settings import *


class Test_IPV6_Interface_00(Test):
    uuid = 'NonTC'
    logger.info("==================Setup Network==================")
    out = setup_network_service_ipv6()
    Assertion.assert_equal(out, True, "ERR: Setup ipv6 on PC1 failed!")


class Test_IPV6_Interface_01(Test):
    uuid = "SOSAIOT-TC-57214"
    description = show_testcase_info(Parameter.TESTPLAN, "4", description=True)['title']

    def test_01_00_show_testcase_info(self):
        utils.show_log('4')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    #assign a wrong format ipv6 address to X1
    def test_01_01_assign_X1_wrong_IP(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': '2001:111:10',   #wrong format
            'prefix_length': 64
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, False, "ERR: Wrong IP format can also be configured!")

    def test_01_02_assign_X1_wrong_PrefixLength(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': '2001:111::10',
            'prefix_length': 148   #wrong format
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, False, "ERR: Wrong prefix format can also be configured!")

    def test_01_03_ConfigX1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': '2001:111::10',
            'prefix_length': 64
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 Failed!")

    def test_01_04_Configure_X1_DNS_and_Gateway(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': '2001:111::10',
            'prefix_length': 64,
            'gateway':'2001:222::1',
            "dns": {
                    "primary": "2001:200::1",
                    "secondary": "2001:201::1",
                    "tertiary": "2001:202::1"
                        },
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 Failed!")

    def test_01_05_Configure_ChangeX1_mode(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'auto',
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 as auto Failed!")

    def test_01_06_Verify_assignedIP_nolonger_exists(self):
        rc =  not os.system('/bin/ping6 -c 4 2001:111::10')
        Assertion.assert_equal(rc, False, "ERR: Assigned static ip still exists!")

    def test_01_07_Unassign_ipv6X1(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_02(Test):
    uuid = "SOSAIOT-TC-57216"
    description = show_testcase_info(Parameter.TESTPLAN, "5", description=True)['title']

    def test_02_00_show_testcase_info(self):
        utils.show_log('5')
        Assertion.assert_equal(True, True, "ERR: show testcase's info failed")

    def test_02_01_Setup_RA_Server_on_PC1(self):
        out = setup_RA_Server()
        Assertion.assert_equal(out, True, "ERR: Open RA Server On PC1 Failed!")

    def test_02_02_ConfigureX1_auto(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'auto',
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 as auto Failed!")

    def test_02_03_VerifyX1_IP(self):
        ip_addr = interface_v4.get_interface_address(name='X1', version='v6')
        logger.info(ip_addr)
        msg = True
        if 'N/A(N/A)' in ip_addr['ip_address']:
            msg = False
        Assertion.assert_equal(msg, True, "ERR: X1 does not get ipv6 ip address!")

    @repeat_method(3)
    def test_02_04_Kill_RA_Server_on_PC1(self):
        out = kill_RA_Server()
        Assertion.assert_equal(out, True, "ERR: Can not kill RA Server on PC1!")

    def test_02_05_unassignX1(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_03(Test):
    uuid = "SOSAIOT-TC-57217"
    description = show_testcase_info(Parameter.TESTPLAN, "6", description=True)['title']
    jira = 'GEN8-9087'

    def test_03_00_show_testcase_info(self):
        utils.show_log('6')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_03_01_ConfigureX2_ipv4(self):
        x2_opt = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '3.3.3.3',
            'mask': '255.255.255.0',
        }
        out = interface_v4.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X2 as ipv4 DMZ Failed!")

    def test_03_02_ConfigureX2_ipv6(self):
        x2_opt = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': '2001:444::2',
        }
        out = interface.config_interface_ipv6(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X2 ipv6 Failed!")

    def test_03_03_UnassignX2_ipv4(self):
        out = interface_v4.unassign_interface(interface='X2')
        Assertion.assert_equal(out, True, "ERR: Unassign X2 Failed!")

    def test_03_04_CheckX2_Cannot_Configured_Ipv6(self):
        time.sleep(5) # wait for X2 being unassigned
        x2_opt = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': '2001:444::2',
        }
        out = interface.config_interface_ipv6(**x2_opt)
        Assertion.assert_equal(out, False, "ERR: X2 without ipv4 ip can still be configured with ipv6 ip!")

    def test_03_05_ConfigureX2_portshield_mode(self):
        x2_portshield_json = {
            "interfaces": [{
                "ipv4": {
                    "comment": "",
                    "shutdown_port": False,
                    "link_speed": {
                        "auto_negotiate": True
                        },
                    "name": "X2",
                    "ip_assignment": {
                        "zone": "LAN",
                        "mode": {
                            "portshield": "X0"
                            }
                        }
                    }
            }]
        }
        url = 'api/sonicos/interfaces/ipv4/name/X2'
        rc = fw.api_put(url, msg=False, data=x2_portshield_json)
        Assertion.assert_equal(rc, True, "ERR: Config X2 portshield mode failed!")

    def test_03_06_CheckX2_Cannot_Configured_Ipv6(self):
        x2_opt = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': '2001:444::2',
        }
        out = interface.config_interface_ipv6(**x2_opt)
        Assertion.assert_equal(out, False, "ERR: X2 in portshield mode can still be configured!")

    def test_03_07_UnassignX2_ipv4(self):
        out = interface_v4.unassign_interface(interface='X2')
        Assertion.assert_equal(out, True, "ERR: Unassign X2 Failed!")


class Test_IPV6_Interface_04(Test):
    uuid = "SOSAIOT-TC-57218"
    description = show_testcase_info(Parameter.TESTPLAN, "7", description=True)['title']

    def test_04_00_show_testcase_info(self):
        utils.show_log('7')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_04_01_SetPC_WANipv6_toNULL(self):
        out = shutDown_network_service_ipv6()
        Assertion.assert_equal(out, True, "ERR: Shut down ipv6 on PC1 failed!")

    def test_04_02_ConfigureX1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'router_adv': True
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 Failed!")

    def test_04_03_Configure_x1_Prefix(self):
        x1_prefix = {
            'name': 'X1',
            'prefix': '2001:333::',
            'valid_lt': 500,
            'prefer_lt': 400,
        }
        out = interface.config_ipv6_static_prefix(**x1_prefix)
        Assertion.assert_equal(out, True, "ERR: Configure X1 with Prefix Failed!")

    def test_04_04_Capture_X1_Ra_Packet(self):
        # To check eth2(WAN) configure router advertisement successfully
        out = utils.check_WAN_RA()
        Assertion.assert_equal(out, True, "ERR: Capture ra packet failed!")

    def test_04_05_Check_X1_prefix(self):
        #To check there is a prefix on WAN
        addr = '2001:333'
        out = checkCapturePacket(addr)
        Assertion.assert_equal(out, True, "ERR: PC Setup Failed!")

    def test_04_06_UnassignX1_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_05(Test):
    uuid = "SOSAIOT-TC-57219"
    description = show_testcase_info(Parameter.TESTPLAN, "8", description=True)['title']

    def test_05_00_show_testcase_info(self):
        utils.show_log('8')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_05_01_restore_PC_ipv6(self):
        out = shutDown_network_service_ipv6()
        Assertion.assert_equal(out, True, "ERR: set wan ipv6 addr to null failed!")

    def test_05_02_Configure_X1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'router_adv': True,
            'adv_pref': True  #enable subnet prefix
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 Failed!")

    def test_05_03_Capture_X1_Ra_Packet(self):
        out = utils.check_WAN_RA()
        Assertion.assert_equal(out, True, "ERR:  Capture ra packets in WAN failed!")

    def test_05_04_Check_X1_subnet_prefix(self):
        addr = '2001:222'
        #check subnet prefix
        out = checkCapturePacket(addr)
        Assertion.assert_equal(out, True, "ERR: Setup network service on PC1 failed!")


class Test_IPV6_Interface_06(Test):
    uuid = "SOSAIOT-TC-57220"
    jira = 'Gen7-24158'
    description = show_testcase_info(Parameter.TESTPLAN, "9", description=True)['title']

    def test_06_00_show_testcase_info(self):
        utils.show_log('9')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_06_01_ConfigX0_add_IPv6_Address_first(self):
        x0_opt1 = {
            'name': 'X0',
            'type': 'static',
            'ip': '2000:2222::1',
            'subnet_prefix_adv': False
        }
        out = interface.add_ipv6_extra_ip(**x0_opt1)
        Assertion.assert_equal(out, True, "ERR: Add a ipv6 address to X0 failed!")

    def test_06_02_ConfigureX0_add_IPv6_Address_second(self):
        x0_opt2 = {
            'name': 'X0',
            'type': 'static',
            'ip': '2000:3333::1',
            'subnet_prefix_adv': False
        }
        out = interface.add_ipv6_extra_ip(**x0_opt2)
        Assertion.assert_equal(out, True, "ERR: Add a ipv6 address to X0 failed!")

    #configure x0 ipv6 address with subnet prefix enable...
    def test_06_03_ConfigureX0_with_SubnetPrefix(self):
        x0_opt3 = {
            'name': 'X0',
            'type': 'static',
            'zone': 'LAN',
            'ip': '2000:4444::1',
            'subnet_prefix_adv': True
        }
        out = interface.add_ipv6_extra_ip(**x0_opt3)
        Assertion.assert_equal(out, True, "ERR: Add a ipv6 address to X0 failed!")

    def test_06_04_ConfigureX0_add_IPv6_Address_forth(self):
        x0_opt4 = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'prefix_length': 64
        }
        out = interface.config_interface_ipv6(**x0_opt4)
        Assertion.assert_equal(out, True, "ERR: Add a ipv6 address to X0 failed!")

    def test_06_05_VerifyX0_get_someIP(self):
        url = 'api/sonicos/interfaces/ipv6/extra-ip'
        json_output = fw.api_get(url)
        out = str(json_output["interfaces"][0]['ipv6']['ip_assignment']['mode']['static']['extra_ip'])
        logger.info(out)
        rc = True
        ip_addrs = ['2000:3333::1', '2000:4444::1', '2000:2222::1']
        for ip_addr in ip_addrs:
            if ip_addr not in out:
                rc = False
                break
        Assertion.assert_equal(rc, True, "ERR: X0 did not got some ip addresses!")

    def test_06_06_Verify_extraip_maximum_9(self):
        #already has three addresses, add 7 more addresses
        #the last address shouled not be configured
        extra_ips = ['2000:5555::1','2000:6666::1','2000:7777::1','2000:8888::1','2000:9999::1','2000:1010::1']
        for extra_ip in extra_ips:
            x0_extraip_opt = {
                'name': 'X0',
                'type': 'static',
                'ip': extra_ip,
                'subnet_prefix_adv': False
            }
            out = interface.add_ipv6_extra_ip(**x0_extraip_opt)
            Assertion.assert_equal(out, True, "ERR: Add a ipv6 address to X0 failed!")

    def test_06_07_Add_last_extraip_failed(self):
        x0_extraip_opt = {
            'name': 'X0',
            'type': 'static',
            'ip': '2000:1011::1',
            'subnet_prefix_adv': False
        }
        out = interface.add_ipv6_extra_ip(**x0_extraip_opt)
        Assertion.assert_equal(out, False, "ERR: ipv6 extra ip can added more than 9 addresses!")


    def test_06_08_UnasignX0(self):
        out = interface.unassign_ipv6_interface(interface='X0')
        Assertion.assert_equal(out, True, "ERR:     Unassign X0 Failed!    ")


class Test_IPV6_Interface_07(Test):
    uuid = "SOSAIOT-TC-57202"
    description = show_testcase_info(Parameter.TESTPLAN, "10", description=True)['title']

    def test_07_00_show_testcase_info(self):
        utils.show_log('10')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_07_01_ConfigureX0_enable_Traffic(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'mgmt_ping': True,
            'ipv6_traffic': True
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 Failed!")

    def test_07_02_ConfigureX1_disable_Traffic(self):
        x1_opt = {
            'name': 'X1',
            'ipv6_traffic': False,
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'mgmt_ping': True,
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 Failed!")

    def test_07_03_checkPing_X0toX1(self):
        rc1 = not os.system('/bin/ping6 -c 4 {}'.format(Parameter.x0_ipv6))
        rc2 = not os.system('/bin/ping6 -c 4 {}'.format(Parameter.x1_ipv6))
        rc = False
        logger.info('ping X0_v6:{}, ping X1_v6{}'.format(rc1,rc2))
        if rc1 == True and rc2 == False:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Disable and Enable ipv6 traffic failed!")

    def test_07_04_unassign_x0_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X0')
        Assertion.assert_equal(out, True, "ERR:     Unassign X0 Failed!    ")

    def test_07_05_unassign_x1_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_08(Test):
    uuid = "SOSAIOT-TC-57203"
    description = show_testcase_info(Parameter.TESTPLAN, "11", description=True)['title']

    def test_08_00_show_testcase_info(self):
        utils.show_log('11')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_08_01_ConfigureX1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': "::",
            'listen_router_advertisement': True,
            'stateless_address_autoconfig': True,
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 Failed!")

    def test_08_02_Setup_PC_Ra_Server(self):
        #Setup PC1 RA server
        out = setup_RA_Server()
        Assertion.assert_equal(out, True, "ERR: Open RA Server On PC1 Failed!")

    def test_08_03_check_X1_get_ip(self):
        #Check X1 get automous ip
        time.sleep(10)
        ip_addr = interface_v4.get_interface_address(name='X1', version='v6')
        rc = False
        if '2001:222' in ip_addr['ip_address']:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: X1 didn't get automous ip!")

    def test_08_04_ConfigureX1_disable_listenning_to_router(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': "::",
            # 'listen_router_advertisement': False,  #default = False
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 Failed!")

    def test_08_05_check_X1_not_get_ip(self):
        #Check X1 not get automous ip
        time.sleep(10)
        ip_addr = interface_v4.get_interface_address(name='X1', version='v6')
        rc = True
        if '2001:222' in ip_addr['ip_address']:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: X1 still can get automous ip!")

    def test_08_06_disable_PC_Ra_Server(self):
        out = kill_RA_Server()
        Assertion.assert_equal(out, True, "ERR: Disable ra server on PC1 failed!")

    def test_08_07_unassignX1_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_09(Test):
    uuid = "SOSAIOT-TC-57222"
    description = show_testcase_info(Parameter.TESTPLAN, "12", description=True)['title']

    def test_09_00_show_testcase_info(self):
        utils.show_log('12')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_09_01_ConfigureX1_ipv6(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': "::",
            'listen_router_advertisement': True,
            'stateless_address_autoconfig': True,
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR:       Configure X1 failed!   ")

    def test_09_02_Setup_PC_Ra_Server(self):
        out = setup_RA_Server()
        Assertion.assert_equal(out, True, "ERR: Open RA Server On PC1 Failed!")

    def test_09_03_check_X1_get_ip(self):
        time.sleep(10)
        # Check X1 get automous ip
        ip_addr = interface_v4.get_interface_address(name='X1', version='v6')
        logger.info(ip_addr)
        rc = False
        if '2001:222' in ip_addr['ip_address']:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: X1 didn't get automous ip!")

    def test_09_04_ConfigureX1_statless_false(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': "::",
            'listen_router_advertisement': True,
            'stateless_address_autoconfig': False,
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR:       Configure X1 failed!   ")

    def test_09_05_check_X1_not_get_ip(self):
        time.sleep(10)
        # Check X1 not get automous ip
        ip_addr = interface_v4.get_interface_address(name='X1', version='v6')
        logger.info(ip_addr)
        rc = True
        if '2001:222' in ip_addr['ip_address']:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: X1 still can get automous ip!")

    def test_09_06_disable_PC_Ra_Server(self):
        out = kill_RA_Server()
        Assertion.assert_equal(out, True, "ERR: Disable ra server on PC1 failed!")

    def test_09_07_unassignX1_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_10(Test):
    uuid = "SOSAIOT-TC-57223"
    description = show_testcase_info(Parameter.TESTPLAN, "13", description=True)['title']

    def test_10_00_show_testcase_info(self):
        utils.show_log('13')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_10_01_Start_to_capture_packets(self):
        # start to capture
        os.system("/usr/sbin/tcpdump -i eth2 -w /tmp/dump-file &")
        # setup PC ra
        rc = setup_RA_Server()
        Assertion.assert_equal(rc, True, "ERR: Setup PC RA failed!")

    def test_10_02_Configure_X1_ipv6(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'listen_router_advertisement': True,
            'stateless_address_autoconfig': True,
            'dad_transmit': 3,
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_10_03_Verify_X1_dad_packets(self):
        time.sleep(10)
        os.system("/usr/bin/pkill tcpdump")
        rc = utils.check_wan_dad()
        Assertion.assert_equal(rc, True, "ERR: Verify dad transmit failed!")

    def test_10_04_disable_PC_RA_server(self):
        rc = kill_RA_Server()
        Assertion.assert_equal(rc, True, "ERR: Kill PC RA Server Failed!")

    def test_10_05_unassignX1_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_11(Test):
    uuid = "SOSAIOT-TC-57204"
    description = show_testcase_info(Parameter.TESTPLAN, "14", description=True)['title']
    jira = 'GEN7-32420'

    def test_11_00_show_testcase_info(self):
        utils.show_log('14')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_11_01_restore_PC_network(self):
        out = shutDown_network_service_ipv6()
        Assertion.assert_equal(out, True, "ERR:    Set PC wan ipv6 addr to null failed!")

    def test_11_02_Configure_X1_ipv6(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'router_adv': True,
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_11_03_Configure_X1_Prefix(self):
        x1_prefix = {
            'name': 'X1',
            'prefix': '2001:888::',
            'valid_lt': 500,
            'prefer_lt': 400,
        }
        out = interface.config_ipv6_static_prefix(**x1_prefix)
        Assertion.assert_equal(out, True, "ERR: Configure X1 with Prefix Failed!")

    def test_11_04_Capture_ra_packets(self):
        out = utils.check_WAN_RA()
        Assertion.assert_equal(out, True, "ERR: Capture ra packet failed! ")

    def test_11_05_check_ra_packets(self):
        addr = '2001:888'
        out = checkCapturePacket(addr)
        Assertion.assert_equal(out, True, "ERR: Capture ra packet of ipv6 prefix failed!")

    def test_11_06_unassignX1_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_12(Test):
    uuid = "SOSAIOT-TC-57224"
    description = show_testcase_info(Parameter.TESTPLAN, "15", description=True)['title']

    def test_12_00_show_testcase_info(self):
        utils.show_log('15')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_12_01_ConfigureX1_ipv6(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'router_adv': True,
            'ra_min': 10,
            'ra_max': 20,
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_12_02_Verify_ra_range(self):
        rc = utils.check_wan_ra_range(10,20)
        Assertion.assert_equal(rc, True, "ERR: Verify ra time interval range failed!")

    def test_12_03_unassignX1_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_13(Test):
    uuid = "SOSAIOT-TC-57225"
    description = show_testcase_info(Parameter.TESTPLAN, "16", description=True)['title']

    def test_13_00_show_testcase_info(self):
        utils.show_log('16')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_13_01_ConfigureX0_ipv6(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'link_mtu': 0,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(3)
    def test_13_02_check_X0_MTU_packet(self):
        # out = utils.check_mtu_0_packet()
        out = utils.check_ipv6_config('mtu','0')
        Assertion.assert_equal(out, True, "ERR: MTU checked failed!")

    def test_13_03_ConfigX0_MTU1400(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'link_mtu': 1400,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 with MTU=1500 failed!")

    @repeat_method(3)
    def test_13_04_check_X0_MTU_packet(self):
        # out = utils.check_mtu_packet('1400')
        out = utils.check_ipv6_config('mtu', '1400')
        Assertion.assert_equal(out, True, "ERR: MTU checked failed!")

    def test_13_05_unassignX0_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X0')
        Assertion.assert_equal(out, True, "ERR:     Unassign X0 Failed!    ")


class Test_IPV6_Interface_14(Test):
    uuid = "SOSAIOT-TC-57205"
    description = show_testcase_info(Parameter.TESTPLAN, "17", description=True)['title']

    def test_14_00_show_testcase_info(self):
        utils.show_log('17')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_14_01_ConfigureX0_ipv6(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'router_adv': True,
            'ip': Parameter.x0_ipv6,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(3)
    def test_14_02_check_X0_ReachTime_0(self):
        out = utils.check_ipv6_config('reachable time', 0)
        Assertion.assert_equal(out, True, "ERR: Reach time check failed!")

    def test_14_03_Config_X0_ReachTime_40(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'reach_time': 40,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(3)
    def test_14_04_check_X0_ReachTime_40(self):
        # out = utils.check_reachableTimes(40)
        sleep(2)
        out = utils.check_ipv6_config('reachable time', 40)
        Assertion.assert_equal(out, True, "ERR: Reach time check failed!")

    def test_14_05_unassignX0_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X0')
        Assertion.assert_equal(out, True, "ERR:     Unassign X0 Failed!    ")


class Test_IPV6_Interface_15(Test):
    uuid = "SOSAIOT-TC-57226"
    description = show_testcase_info(Parameter.TESTPLAN, "18", description=True)['title']

    def test_15_00_show_testcase_info(self):
        utils.show_log('18')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_15_01_ConfigureX0_ipv6(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            # 'retrans_time': 0,   default = 0;
            'router_adv': True,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(5)
    def test_15_02_check_X0_RetransTime_0(self):
        sleep(1)
        out = utils.check_ipv6_config('retrans time', 0)
        Assertion.assert_equal(out, True, "ERR: Reach time check failed!")

    def test_15_03_Configure_X0_retransTime_40(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'retrans_time': 40,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(5)
    def test_15_04_check_X0_RetransTime_40(self):
        sleep(1)
        out = utils.check_ipv6_config('retrans time', 40)
        Assertion.assert_equal(out, True, "ERR: Reach time check failed!")

    def test_15_05_unassignX0_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X0')
        Assertion.assert_equal(out, True, "ERR:     Unassign X0 Failed!    ")


class Test_IPV6_Interface_16(Test):
    uuid = "SOSAIOT-TC-57227"
    description = show_testcase_info(Parameter.TESTPLAN, "19", description=True)['title']

    def test_16_00_show_testcase_info(self):
        utils.show_log('19')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_16_01_ConfigureX0_HopLimit_30(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'current_hop_limit': 30,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(3)
    def test_16_02_check_X0_HopLimit_30(self):
        out = utils.check_ipv6_config('hop limit','30')
        Assertion.assert_equal(out, True, "ERR: current_hop_limit check failed!")

    def test_16_03_ConfigureX0_HopLimit_64(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            # 'current_hop_limit': 64, default = 64,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(3)
    def test_16_04_check_X0_HopLimit_64(self):
        # out = utils.check_HopLimit('64')
        out = utils.check_ipv6_config('hop limit', '64')
        Assertion.assert_equal(out, True, "ERR: current_hop_limit check failed!")

    def test_16_05_unassignX0_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X0')
        Assertion.assert_equal(out, True, "ERR:     Unassign X0 Failed!    ")


class Test_IPV6_Interface_17(Test):
    uuid = "SOSAIOT-TC-57228"
    description = show_testcase_info(Parameter.TESTPLAN, "20", description=True)['title']

    def test_17_00_show_testcase_info(self):
        utils.show_log('20')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_17_01_ConfigureX0_LifeTime_1500(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'lifetime': 1500,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(5)
    def test_17_02_check_X0_Lifetime_1500(self):
        sleep(1)
        out = utils.check_ipv6_config('lifetime', 1500)
        Assertion.assert_equal(out, True, "ERR: Lifetime check failed!")

    def test_17_03_ConfigureX0_LifeTime_0(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'lifetime': 0,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(5)
    def test_17_04_check_X0_Lifetime_0(self):
        sleep(1)
        out = utils.check_ipv6_config('lifetime', 0)
        Assertion.assert_equal(out, True, "ERR: Lifetime check failed!")

    def test_17_05_unassignX0_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X0')
        Assertion.assert_equal(out, True, "ERR:     Unassign X0 Failed!    ")


class Test_IPV6_Interface_18(Test):
    uuid = "SOSAIOT-TC-57206"
    description = show_testcase_info(Parameter.TESTPLAN, "21", description=True)['title']

    def test_18_00_show_testcase_info(self):
        utils.show_log('21')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_18_01_ConfigureX0_Managed_False(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'managed': False
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(3)
    def test_18_02_check_X0_Managed_flag(self):
        out = utils.check_ipv6_config('Flags', 'none')
        Assertion.assert_equal(out, True, "ERR: Check Mangaed Failed!")

    def test_18_03_ConfigureX0_Managed_True(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'managed': True
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(3)
    def test_18_04_check_X0_Managed_flag(self):
        # out = utils.check_flags('managed')
        sleep(2)
        out = utils.check_ipv6_config('Flags', 'managed')
        Assertion.assert_equal(out, True, "ERR: Check Mangaed Failed!")

    def test_18_05_unassignX0_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X0')
        Assertion.assert_equal(out, True, "ERR:     Unassign X0 Failed!    ")


class Test_IPV6_Interface_19(Test):
    uuid = "SOSAIOT-TC-57229"
    description = show_testcase_info(Parameter.TESTPLAN, "22", description=True)['title']

    def test_19_00_show_testcase_info(self):
        utils.show_log('22')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_19_01_ConfigureX0_other_config_false(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(3)
    def test_19_02_check_X0_other_config_flag(self):
        out = utils.check_ipv6_config('Flags', 'none')
        Assertion.assert_equal(out, True, "ERR: Check Other Config Failed!")

    def test_19_03_ConfigureX0_other_config_true(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.x0_ipv6,
            'router_adv': True,
            'other_config': True
        }
        out = interface.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    @repeat_method(3)
    def test_19_04_check_X0_other_config_flag(self):
        # out = utils.check_flags('other stateful')
        out = utils.check_ipv6_config('Flags', 'other stateful')
        Assertion.assert_equal(out, True, "ERR: Check Other Config Failed!")

    def test_19_05_unassignX0_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X0')
        Assertion.assert_equal(out, True, "ERR:     Unassign X0 Failed!    ")


class Test_IPV6_Interface_20(Test):
    uuid = "SOSAIOT-TC-57230"
    description = show_testcase_info(Parameter.TESTPLAN, "23", description=True)['title']
    jira = 'GEN7-32420'

    def test_20_00_show_testcase_info(self):
        utils.show_log('23')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_20_01_ConfigureX1_static(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'router_adv': True,
            'listen_router_advertisement': True,
            'stateless_address_autoconfig': True,
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_20_02_ConfigureX1_invalid_lifetime(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'router_adv': True,
            'lifetime': 715827894684
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, False, "ERR: Invalid lifetime can be configured!")

    def test_20_03_Configure_wrong_prefix(self):
        x1_prefix = {
            'name': 'X1',
            'prefix': '100:1',
            'valid_lt': 500,
            'prefer_lt': 400,
        }
        out = interface.config_ipv6_static_prefix(**x1_prefix)
        Assertion.assert_equal(out, False, "ERR: Configure X1 with invalid Prefix!")

    def test_20_04_Configure_Prefix(self):
        x1_prefix = {
            'name': 'X1',
            'prefix': '2001:122::',
            'valid_lt': 500,
            'prefer_lt': 400,
        }
        out = interface.config_ipv6_static_prefix(**x1_prefix)
        Assertion.assert_equal(out, True, "ERR: Configure X1 with Prefix Failed!")

    def test_20_05_Verify_X1_get_prefix_ip(self):
        time.sleep(10)
        ip_addr = interface_v4.get_interface_address(name='X1', version='v6')
        logger.info(ip_addr)
        msg = False
        if '2001:122' in ip_addr['ip_address']:
            msg = True
        Assertion.assert_equal(msg, True, "ERR: X1 does not get ipv6 ip address from prefix!")

    def test_20_06_Configure_multiple_prefix(self):
        prefixes = ['2001:123::', '2001:124::', '2001:125::']
        for prefix in prefixes:
            x1_prefix = {
                'name': 'X1',
                'prefix': prefix,
                'valid_lt': 500,
                'prefer_lt': 400,
            }
            out = interface.config_ipv6_static_prefix(**x1_prefix)
            Assertion.assert_equal(out, True, "ERR: Configure X1 with multiple Prefix Failed!")


class Test_IPV6_Interface_21(Test):
    # mgmt_http only can be set when enable "Allow management via HTTP" in Administration tab
    uuid = "NonTC"
    description = show_testcase_info(Parameter.TESTPLAN, "25", description=True)['title']

    def test_21_00_show_testcase_info(self):
        utils.show_log('25')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_21_01_ConfigureX1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'mgmt_https': False
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_21_02_verify_Https_False(self):
        time.sleep(2)
        out = accessrule.show_ipv6_access_rule('https')
        Assertion.assert_equal(out, False, "ERR: Verify https management failed!")

    def test_21_03_ConfigureX1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'mgmt_https': True
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_21_04_verify_Https_True(self):
        time.sleep(2)
        out = accessrule.show_ipv6_access_rule('https')
        Assertion.assert_equal(out, True, "ERR: Verify https management failed!")

    def test_21_05_unassign_ipv6X1(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_22(Test):
    # mgmt_http only can be set when enable "Allow management via HTTP" in Administration tab
    uuid = "SOSAIOT-TC-57231"
    description = show_testcase_info(Parameter.TESTPLAN, "26", description=True)['title']

    def test_22_00_show_testcase_info(self):
        utils.show_log('26')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_22_01_ConfigureX1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'mgmt_ping': False
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_22_02_verify_ping_False(self):
        time.sleep(2)
        out = accessrule.show_ipv6_access_rule('ping')
        Assertion.assert_equal(out, False, "ERR: Verify Ping6 failed!")

    def test_22_03_test_ping_failed(self):
        rc = not os.system('/bin/ping6 -c 4 {}'.format(Parameter.x1_ipv6))
        Assertion.assert_equal(rc, False, "ERR: Can ping x1 {}!".format(Parameter.x1_ipv6))

    def test_22_04_ConfigureX1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'mgmt_ping': True
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_22_05_verify_ping_True(self):
        time.sleep(2)
        out = accessrule.show_ipv6_access_rule('ping')
        Assertion.assert_equal(out, True, "ERR: Verify Ping6 failed!")

    def test_22_06_test_ping_pass(self):
        rc = not os.system('/bin/ping6 -c 4 {} -I eth2'.format(Parameter.x1_ipv6))
        Assertion.assert_equal(rc, True, "ERR: Can not ping x1 {}!".format(Parameter.x1_ipv6))

    def test_22_07_unassign_ipv6X1(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_23(Test):
    # mgmt_http only can be set when enable "Allow management via HTTP" in Administration tab
    uuid = "SOSAIOT-TC-57232"
    description = show_testcase_info(Parameter.TESTPLAN, "27", description=True)['title']

    def test_23_00_show_testcase_info(self):
        utils.show_log('27')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_23_01_ConfigureX1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'mgmt_snmp': False
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_23_02_verify_snmp_False(self):
        time.sleep(2)
        out = accessrule.show_ipv6_access_rule('snmp')
        Assertion.assert_equal(out, False, "ERR: Verify snmp management failed!")

    def test_23_03_ConfigureX1(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.x1_ipv6,
            'mgmt_snmp': True
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_23_04_verify_snmp_True(self):
        time.sleep(2)
        out = accessrule.show_ipv6_access_rule('snmp')
        Assertion.assert_equal(out, True, "ERR: Verify snmp management failed!")

    def test_23_05_unassign_ipv6X1(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")


class Test_IPV6_Interface_24(Test):
    uuid = "SOSAIOT-TC-57233"
    jira = 'Gen7-20168'
    description = show_testcase_info(Parameter.TESTPLAN, "30", description=True)['title']

    def test_24_00_show_testcase_info(self):
        utils.show_log('30')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_24_01_ConfigureX1_ipv4(self):
        x1_opt = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '3.3.3.3',
            'mask': '255.255.255.0'
        }
        out = interface_v4.config_interface(**x1_opt)
        Assertion.assert_equal(out, True, "ERR:     Configure X1 Failed!    ")

    def test_24_02_ConfigureX1_ipv6(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.wan_ipv6,
        }
        out = interface.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR:     Configure X1 Failed!    ")

    def test_24_03_ConfigureX1_dhcp(self):
        x1_opt = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'dhcp',
        }
        out = interface_v4.config_interface(**x1_opt)
        Assertion.assert_equal(out, True, "ERR:     Configure X1 Failed!    ")

    
    @repeat_method(3)
    def test_24_04_Verify_X1ipv6_exist(self):
        time.sleep(30)
        ip_addr = interface_v4.get_interface_address(name='X1', version='v6')
        logger.info(ip_addr)
        msg = True
        if 'N/A(N/A)' in ip_addr['ip_address']:
            msg = False
        Assertion.assert_equal(msg, True, "ERR: X1 does not get ipv6 ip address!")

    def test_24_05_UnassignX1_ipv6(self):
        out = interface.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(out, True, "ERR:     Unassign X1 Failed!    ")
