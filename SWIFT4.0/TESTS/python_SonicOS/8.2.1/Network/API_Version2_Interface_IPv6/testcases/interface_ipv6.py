from parameter import *


class Test_API_Interface_IPv6_Smoke_01(Test):
    """
    1) get all interface ipv6 interface ip
    """
    uuid = "SOSAIOT-TC-47189"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "01", description=True)['title']

    def test_01_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_get_ipv6_interfaces(self):
        output = interface_ipv6.get_interface_address()
        for item in output:
            logger.info(item)
        Assertion.assert_not_equal(output, False, "ERR: can not get base info")


class Test_API_Interface_IPv6_Smoke_02(Test):
    """
    Retrieve configuration of a specified wlan tunnel interface
    bound to physical interface
    """
    uuid = "SOSAIOT-TC-47190"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "02", description=True)['title']

    def test_02_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_add_wlan_tunner_interface(self):
        wlan_tunnel = {
            'type': 'wlan-tunnel',
            'tunnel-id': 1,
            'tunnel-if': 'x1',
            'zone': 'wlan',
            'ip': '2.2.2.2',
            'netmask': '255.255.255.0',
            'sp-limit': 2
        }
        output = interface_ipv4.add_interface(**wlan_tunnel)
        Assertion.assert_equal(output, True, "ERR: can not add tunnel interface")

    def test_02_02_get_ipv6_tunnel(self):
        output = interface_ipv6.get_interface_address('wt1')
        Assertion.assert_equal(output['interface_name'], 'WT1', "ERR: can not get tunnel ipv6 interface")

    def test_02_03_delete_ipv4_tunnel(self):
        wlan_tunnel_static = {
            'type': 'wlan-tunnel',
            'tunnel-name': 'wt1'
        }
        output = interface_ipv4.del_interface(**wlan_tunnel_static)
        Assertion.assert_equal(output, True, "ERR: can not delete tunnel interface")


class Test_API_Interface_IPv6_Smoke_03(Test):
    """
    1) set auto mode
    """
    uuid = "SOSAIOT-TC-47191"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "03", description=True)['title']

    def test_03_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_config_ipv6_interfaces_auto(self):
        auto_mode = {
            'name': 'X1',
            'mode': 'auto'
        }
        output = interface_ipv6.config_interface_ipv6(**auto_mode)
        Assertion.assert_equal(output, True, "ERR: set ipv6 auto mode fail")

    def test_03_02_check_interface(self):
        output = interface_ipv6.get_interface_address('x1')
        Assertion.assert_equal(output['ip_mode'], 'Auto', "ERR: check ipv6 auto mode fail")


class Test_API_Interface_IPv6_Smoke_04(Test):
    """
    1) enable router advertisement  
    """
    uuid = "SOSAIOT-TC-47192"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "04", description=True)['title']

    def test_04_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_enable_route_advertisment(self):
        interface_ipv6_x1 = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': '1::1',
            'router_adv': True,
            'ra_min': 20,
            'ra_max': 60
        }
        output = interface_ipv6.config_interface_ipv6(**interface_ipv6_x1)
        Assertion.assert_equal(output, True, "ERR: enable ipv6 router advertisement fail")

    def test_04_02_check_interface(self):
        output = interface_ipv6.get_ipv6_interface_base('x1')
        result = output['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement']['enable']
        Assertion.assert_equal(result, True, "ERR: enable ipv6 roouter advertisment fail")


class Test_API_Interface_IPv6_Smoke_05(Test):
    """
    1) set ipv6 dhcpv6 mode  
    """
    uuid = "SOSAIOT-TC-47193"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "05", description=True)['title']

    def test_05_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_set_ipv6_dhcpv6_mode(self):
        interface_ipv6_dhcpv6 = {
            'name': 'X2',
            'mode': 'dhcpv6',
            'listen_router_advertisement': True
        }
        output = interface_ipv6.config_interface_ipv6(**interface_ipv6_dhcpv6)
        Assertion.assert_equal(output, True, "ERR: set dhcpv6 mode fail")

    def test_05_02_check_interface(self):
        output = interface_ipv6.get_ipv6_interface_base('x2')
        result = output['interfaces'][0]['ipv6']['ip_assignment']['mode']
        Assertion.assert_regular(str(result.keys()), 'dhcpv6', "ERR: set dhcpv6 failed")
