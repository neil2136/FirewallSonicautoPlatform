from settings import *

fw = Firewall(Parameter.DUT_X0_IP, user='admin', password='password', supported_config_mode='api')
interface = network.InterfaceIPv4Api(fw)
inter_v6_obj = network.InterfaceIPv6Api(fw)
route_obj = network.RoutePolicyApi(fw)
ao_obj = network.AddressobjectsApi(fw)
cdrouter = cdrouter_test.CDRTest(Parameter.NTA1000,path=Parameter.TESTPATH, case=Parameter.CASE1, conf=Parameter.CONF, log=Parameter.LOG)
cdrouter_new = cdrouter_test.CDRTest(Parameter.NTA1000,path=Parameter.TESTPATH, case=Parameter.CASE1, conf=Parameter.CONF_NEW, log=Parameter.LOG)


class Test_009_Check_Route(Test):
    uuid = "SOSAIOT-TC-56380"
    description= show_testcase_info(Parameter.TESTPLAN, '009', description=True)['title']
    # cdrouter = cdrouter_test.CDRTest(Parameter.NTA1000,path=Parameter.TESTPATH, case=Parameter.CASE1, conf=Parameter.CONF, log=Parameter.LOG)

    def test_009_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '009')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_009_01_config_X2_dhcp_PD(self):
        X2_ipv6_dhcp = {
            'name': 'X2',
            'mode': 'dhcpv6',
            'dhcpv6': {
                'prefix_delegation': True, 
            }
        }
        rc = inter_v6_obj.config_interface_ipv6(**X2_ipv6_dhcp)
        Assertion.assert_equal(rc, True, "ERR: config X2 ipv6 to dhcp fail .")

    # def test_009_02_config_X3_IPv6(self):
    #     x3_pd = {
    #         'name': 'X3',
    #         'mode': 'static',
    #         'type': 'prefix_delegation',
    #         'preferred_ip': Parameter.EXTRA_IP,
    #         'delegated_prefix': 'X2 Delegated Prefix',
    #         'prefix_length': 64,
    #     }
    #     rc = inter_v6_obj.add_ipv6_extra_ip(**x3_pd)
    #     Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 failed")

    def test_009_03_run_cdrouter(self):
        cdrouter.run_case(backend=True)
        logger.info('Click renew.')
        interface.click_dhcp_renew('X2',version='v6')
        time.sleep(20)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_009_04_check_X2_got_ip(self):
        output= inter_v6_obj.get_interface_address('X2')
        ip = output['ip_address'].split(',')[0]
        if ip != '3001::1/64(DHCPv6)':
            time.sleep(10)
        Assertion.assert_equal(ip, '3001::1/64(DHCPv6)', "ERR: X2 get ip from dhcpv6 server fail.")

    def test_009_05_check_route_policy(self):
        routes = route_obj.show_route_policy(version='ipv6')
        foundit = 0

        try:
            for route in routes['route_policies']:
                try:
                    if route['ipv6']['destination']['name'] == 'X2 Delegated Prefix' and route['ipv6']['interface'] == 'Drop_TunnelIf' \
                        and route['ipv6']['metric'] == 255:
                        logger.info('Found route for delegated prefix.')
                        foundit = 1
                        break
                except:
                    pass
        except Exception as e:
            logger.info(f'Error: {e}')
        Assertion.assert_equal(foundit, 1, "ERR: pd route not in PBR table.")

    def test_009_06_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        interface.click_dhcp_release('X2',version='v6')
        time.sleep(20)
        Assertion.assert_equal(rc, True, "ERR: stop cdrotuer test fail.")

    # def test_009_07_config_X3_IPv6(self):
    #     x3_pd = {
    #         'name': 'X3',
    #         'mode': 'static',
    #         'type': 'prefix_delegation',
    #         'preferred_ip': Parameter.EXTRA_IP,
    #         'delegated_prefix': 'X2 Delegated Prefix',
    #         'prefix_length': 64,
    #     }
    #     rc = inter_v6_obj.delete_ipv6_extra_ip(**x3_pd)
    #     Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 failed")


class Test_010_Add_Address(Test):
    uuid = "SOSAIOT-TC-56384"
    description= show_testcase_info(Parameter.TESTPLAN, '010', description=True)['title']
    # cdrouter = cdrouter_test.CDRTest(Parameter.NTA1000,path=Parameter.TESTPATH, case=Parameter.CASE1, conf=Parameter.CONF, log=Parameter.LOG)

    def test_010_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '010')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    @repeat_method(5)
    def test_010_01_config_X2_dhcp_PD(self):
        X2_ipv6_dhcp = {
            'name': 'X2',
            'mode': 'dhcpv6',
            'dhcpv6': {
                'prefix_delegation': True, 
            }
        }
        rc = inter_v6_obj.config_interface_ipv6(**X2_ipv6_dhcp)
        Assertion.assert_equal(rc, True, "ERR: config X2 ipv6 to dhcp fail .")

    # def test_010_02_config_cdrouter_IPv6(self):
    #     x0_pd = {
    #         'name': 'X3',
    #         'mode': 'static',
    #         'type': 'prefix_delegation',
    #         'preferred_ip': Parameter.EXTRA_IP,
    #         'delegated_prefix': 'X2 Delegated Prefix',
    #         'prefix_length': 64,
    #     }
    #     rc = inter_v6_obj.add_ipv6_extra_ip(**x0_pd)
    #     Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 failed")

    def test_010_03_run_cdrouter(self):
        cdrouter.run_case(backend=True)
        logger.info('Click renew.')
        interface.click_dhcp_renew('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_010_04_check_X2_got_ip(self):
        output= inter_v6_obj.get_interface_address('X2')
        ip = output['ip_address'].split(',')[0]
        if ip != '3001::1/64(DHCPv6)':
            time.sleep(10)
        Assertion.assert_equal(ip, '3001::1/64(DHCPv6)', "ERR: X2 get ip from dhcpv6 server fail.")

    @parameterized.expand([
        ('LAN'), ('DMZ'),
    ])   
    def test_010_05_check_X3_got_ip(self, zone):
        x3_static_v4 = {
            'if': 'x3',
            'zone': zone,
            'mode': 'static',
            'ip': Parameter.DUT_X3_IP,
            'netmask': Parameter.NETMASK,
            'mgmt-https': True,
        }
        rc = interface.config_interface(**x3_static_v4)
        # x3_pd = {
        #     'name': 'X3',
        #     'mode': 'static',
        #     'type': 'prefix_delegation',
        #     'preferred_ip': Parameter.EXTRA_IP,
        #     'delegated_prefix': 'X2 Delegated Prefix',
        #     'prefix_length': 64,
        # }
        # rc &= inter_v6_obj.add_ipv6_extra_ip(**x3_pd)
        Assertion.assert_equal(rc, True, "ERR: Config X3 failed.")
        for i in range(0,5):
            output= inter_v6_obj.get_interface_address('X3')
            ip = output['ip_address'].split(',')[0]
            expect_id = Parameter.PD_PREFIX + Parameter.EXTRA_IP + '/64'
            if ip == expect_id+'(PD)':
                break
            else:
                time.sleep(10)
        Assertion.assert_equal(ip, expect_id+'(PD)', "ERR: x3 not get delegated IP.")
        # rc = inter_v6_obj.delete_ipv6_extra_ip(**x3_pd)
        # Assertion.assert_equal(rc, True, "ERR: Delete pd address.")

    def test_010_06_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        interface.click_dhcp_release('X2',version='v6')
        time.sleep(20)
        Assertion.assert_equal(rc, True, "ERR: stop cdrotuer test fail.")


class Test_019_Check_AO(Test):
    uuid = "SOSAIOT-TC-56385"
    description= show_testcase_info(Parameter.TESTPLAN, '019', description=True)['title']
    # cdrouter = cdrouter_test.CDRTest(Parameter.NTA1000,path=Parameter.TESTPATH, case=Parameter.CASE1, conf=Parameter.CONF, log=Parameter.LOG)
    # cdrouter_new = cdrouter_test.CDRTest(Parameter.NTA1000,path=Parameter.TESTPATH, case=Parameter.CASE1, conf=Parameter.CONF_NEW, log=Parameter.LOG)

    def test_019_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '019')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    @repeat_method(5)
    def test_019_01_config_X2_dhcp_PD(self):
        X2_ipv6_dhcp = {
            'name': 'X2',
            'mode': 'dhcpv6',
            'dhcpv6': {
                'prefix_delegation': True, 
            }
        }
        rc = inter_v6_obj.config_interface_ipv6(**X2_ipv6_dhcp)
        Assertion.assert_equal(rc, True, "ERR: config X2 ipv6 to dhcp fail .")

    def test_019_03_run_cdrouter(self):
        cdrouter.run_case(backend=True)
        logger.info('Click renew.')
        interface.click_dhcp_renew('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_019_04_check_X2_got_ip(self):
        output= inter_v6_obj.get_interface_address('X2')
        ip = output['ip_address'].split(',')[0]
        if ip != '3001::1/64(DHCPv6)':
            # logger.info('Click renew.')
            # interface.click_dhcp_renew('X2',version='v6')
            time.sleep(10)
        Assertion.assert_equal(ip, '3001::1/64(DHCPv6)', "ERR: X2 get ip from dhcpv6 server fail.")

    # def test_019_05_config_X3_IPv6(self):
    #     x3_pd = {
    #         'name': 'X3',
    #         'mode': 'static',
    #         'type': 'prefix_delegation',
    #         'preferred_ip': Parameter.EXTRA_IP,
    #         'delegated_prefix': 'X2 Delegated Prefix',
    #         'prefix_length': 64,
    #     }
    #     rc = inter_v6_obj.add_ipv6_extra_ip(**x3_pd)
    #     Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 failed")

    def test_019_06_Check_AO(self):
        output = ao_obj.get_addressobject_by_name(name='X2 Delegated Prefix',version='ipv6')
        subnet= output['address_objects'][0]['ipv6']['network']['subnet']
        Assertion.assert_regular(subnet, Parameter.PD_PREFIX, "ERR: Check AO failed")

    def test_019_07_stop_cdrouter(self):
        rc= cdrouter.terminate_case()
        interface.click_dhcp_release('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(rc, True, "ERR: stop cdrotuer test fail.")

    def test_019_08_run_cdrouter_with_new_prefix(self):
        cdrouter_new.run_case(backend=True)
        logger.info('Click renew.')
        interface.click_dhcp_renew('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_019_09_check_X2_got_ip(self):
        # interface.click_dhcp_renew('X2',version='v6')
        time.sleep(10)
        output= inter_v6_obj.get_interface_address('X2')
        ip = output['ip_address'].split(',')[0]
        Assertion.assert_equal(ip, '3002::1/64(DHCPv6)', "ERR: X2 get ip from dhcpv6 server fail.")

    def test_019_10_Check_new_AO(self):
        output = ao_obj.get_addressobject_by_name(name='X2 Delegated Prefix',version='ipv6')
        subnet= output['address_objects'][0]['ipv6']['network']['subnet']
        Assertion.assert_regular(subnet, Parameter.PD_PREFIX_NEW, "ERR: Check AO failed")

    # def test_019_11_config_X3_IPv6(self):
    #     x0_pd = {
    #         'name': 'X3',
    #         'mode': 'static',
    #         'type': 'prefix_delegation',
    #         'preferred_ip': Parameter.EXTRA_IP,
    #         'delegated_prefix': 'X2 Delegated Prefix',
    #         'prefix_length': 64,
    #     }
    #     rc = inter_v6_obj.delete_ipv6_extra_ip(**x3_pd)
    #     Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 failed")

    def test_019_12_stop_cdrouter(self):
        rc = cdrouter_new.terminate_case()
        interface.click_dhcp_release('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(True, True, "ERR: stop cdrotuer test fail.")


class Test_020_Check_Address_Update(Test):
    uuid = "SOSAIOT-TC-56386"
    description= show_testcase_info(Parameter.TESTPLAN, '020', description=True)['title']

    def test_020_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '020')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    @repeat_method(5)
    def test_020_01_config_X2_dhcp_PD(self):
        X2_ipv6_dhcp = {
            'name': 'X2',
            'mode': 'dhcpv6',
            'dhcpv6': {
                'prefix_delegation': True, 
            }
        }
        rc = inter_v6_obj.config_interface_ipv6(**X2_ipv6_dhcp)
        Assertion.assert_equal(rc, True, "ERR: config X2 ipv6 to dhcp fail .")

    def test_020_02_run_cdrouter(self):
        cdrouter.run_case(backend=True)
        logger.info('Click renew.')
        interface.click_dhcp_renew('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_020_03_check_X2_got_ip(self):
        output= inter_v6_obj.get_interface_address('X2')
        ip = output['ip_address'].split(',')[0]
        if ip != '3001::1/64(DHCPv6)':
            # logger.info('Click renew.')
            # interface.click_dhcp_renew('X2',version='v6')
            time.sleep(10)
        Assertion.assert_equal(ip, '3001::1/64(DHCPv6)', "ERR: X2 get ip from dhcpv6 server fail.")

    @parameterized.expand([
        ("LAN"),("WAN"),("DMZ"),
    ])
    def test_020_04_config_X3_IPv6(self, zone):
        X3_assign = {
            'if': 'X3',
            'zone': zone, 
            'mode': 'static',
            'ip': Parameter.DUT_X3_IP,
            'gateway': Parameter.DUT_X3_GW,
        }
        rc = interface.config_interface(**X3_assign)
        # x3_pd= {
        #     'name': 'X3',
        #     'mode': 'static',
        #     'type': 'prefix_delegation',
        #     'preferred_ip': Parameter.EXTRA_IP,
        #     'delegated_prefix': 'X2 Delegated Prefix',
        #     'prefix_length': 64,
        # }
        # rc &= inter_v6_obj.add_ipv6_extra_ip(**x3_pd)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 failed")
        output= inter_v6_obj.get_interface_address('X3')
        for i in range(0,5):
            output= inter_v6_obj.get_interface_address('X3')
            ip = output['ip_address'].split(',')[0]
            expect_id = Parameter.PD_PREFIX + Parameter.EXTRA_IP + '/64'
            if ip == expect_id+'(PD)':
                break
            else:
                time.sleep(10)
        Assertion.assert_equal(ip, expect_id+'(PD)', "ERR: x3 not get delegated IP.")
        # rc = inter_v6_obj.delete_ipv6_extra_ip(**x3_pd)
        # Assertion.assert_equal(rc, True, "ERR: Delete pd address.")

    def test_020_05_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        interface.click_dhcp_release('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(rc, True, "ERR: stop cdrotuer test fail.")

    def test_020_06_run_cdrouter_with_new_prefix(self):
        cdrouter_new.run_case(backend=True)
        logger.info('Click renew.')
        interface.click_dhcp_renew('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_020_07_check_X2_got_ip(self):
        output= inter_v6_obj.get_interface_address('X2')
        ip = output['ip_address'].split(',')[0]
        if ip != '3002::1/64(DHCPv6)':
            # logger.info('Click renew.')
            # interface.click_dhcp_renew('X2',version='v6')
            time.sleep(10)
        Assertion.assert_equal(ip, '3002::1/64(DHCPv6)', "ERR: X2 get ip from dhcpv6 server fail.")


    @parameterized.expand([
        ("LAN"),("WAN"),("DMZ"),
    ])
    def test_020_08_config_X3_IPv6(self, zone):
        X3_assign = {
            'if': 'X3',
            'zone': zone, 
            'mode': 'static',
            'ip': Parameter.DUT_X3_IP,
            'gateway': Parameter.DUT_X3_GW,
        }
        rc = interface.config_interface(**X3_assign)
        # x3_pd= {
        #     'name': 'X3',
        #     'mode': 'static',
        #     'type': 'prefix_delegation',
        #     'preferred_ip': Parameter.EXTRA_IP,
        #     'delegated_prefix': 'X2 Delegated Prefix',
        #     'prefix_length': 64,
        # }
        # rc &= inter_v6_obj.add_ipv6_extra_ip(**x3_pd)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 failed")
        output= inter_v6_obj.get_interface_address('X3')
        for i in range(0,5):
            output= inter_v6_obj.get_interface_address('X3')
            ip = output['ip_address'].split(',')[0]
            expect_id = Parameter.PD_PREFIX_NEW + Parameter.EXTRA_IP + '/64'
            if ip == expect_id+'(PD)':
                break
            else:
                time.sleep(10)
        Assertion.assert_equal(ip, expect_id+'(PD)', "ERR: x3 not get delegated IP.")
        # rc = inter_v6_obj.delete_ipv6_extra_ip(**x3_pd)
        # Assertion.assert_equal(rc, True, "ERR: Delete pd address.")

    def test_020_09_stop_cdrouter(self):
        rc = cdrouter_new.terminate_case()
        interface.click_dhcp_release('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(rc, True, "ERR: stop cdrotuer test fail.")


class Test_021_Check_Route_Update(Test):
    uuid = "SOSAIOT-TC-56390"
    description= show_testcase_info(Parameter.TESTPLAN, '021', description=True)['title']

    def test_021_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '021')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    @repeat_method(5)
    def test_021_01_config_X2_dhcp_PD(self):
        X2_ipv6_dhcp = {
            'name': 'X2',
            'mode': 'dhcpv6',
            'dhcpv6': {
                'prefix_delegation': True, 
            }
        }
        rc = inter_v6_obj.config_interface_ipv6(**X2_ipv6_dhcp)
        Assertion.assert_equal(rc, True, "ERR: config X2 ipv6 to dhcp fail .")

    def test_021_02_run_cdrouter(self):
        cdrouter.run_case(backend=True)
        logger.info('Click renew.')
        interface.click_dhcp_renew('X2',version='v6')
        time.sleep(20)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_021_03_check_X2_got_ip(self):
        output= inter_v6_obj.get_interface_address('X2')
        ip = output['ip_address'].split(',')[0]
        if ip != '3001::1/64(DHCPv6)':
            time.sleep(10)
        Assertion.assert_equal(ip, '3001::1/64(DHCPv6)', "ERR: X2 get ip from dhcpv6 server fail.")

    def test_021_04_check_route_policy(self):
        routes = route_obj.show_route_policy(version='ipv6')
        foundit = 0

        try:
            for route in routes['route_policies']:
                try:
                    if route['ipv6']['destination']['name'] == 'X2 Delegated Prefix' and route['ipv6']['interface'] == 'Drop_TunnelIf' \
                        and route['ipv6']['metric'] == 255:
                        logger.info('Found route for delegated prefix.')
                        foundit = 1
                        break
                except:
                    pass
        except Exception as e:
            logger.info(f'Error: {e}')
        Assertion.assert_equal(foundit, 1, "ERR: pd route not in PBR table.")
        output = ao_obj.get_addressobject_by_name(name='X2 Delegated Prefix',version='ipv6')
        subnet= output['address_objects'][0]['ipv6']['network']['subnet']
        Assertion.assert_regular(subnet, Parameter.PD_PREFIX, "ERR: Check AO failed")

    def test_021_05_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        interface.click_dhcp_release('X2',version='v6')
        time.sleep(20)
        Assertion.assert_equal(rc, True, "ERR: stop cdrotuer test fail.")

    def test_021_06_run_cdrouter_with_new_prefix(self):
        cdrouter_new.run_case(backend=True)
        logger.info('Click renew.')
        interface.click_dhcp_renew('X2',version='v6')
        time.sleep(20)
        Assertion.assert_equal(True, True, "ERR: start cdrotuer test fail.")

    @repeat_method(5)
    def test_021_07_check_X2_got_ip(self):
        # interface.click_dhcp_renew('X2',version='v6')
        time.sleep(10)
        output= inter_v6_obj.get_interface_address('X2')
        ip = output['ip_address'].split(',')[0]
        Assertion.assert_equal(ip, '3002::1/64(DHCPv6)', "ERR: X2 get ip from dhcpv6 server fail.")

    def test_021_08_Check_new_Route_Policy(self):
        routes = route_obj.show_route_policy(version='ipv6')
        foundit = 0

        try:
            for route in routes['route_policies']:
                try:
                    if route['ipv6']['destination']['name'] == 'X2 Delegated Prefix' and route['ipv6']['interface'] == 'Drop_TunnelIf' \
                        and route['ipv6']['metric'] == 255:
                        logger.info('Found route for delegated prefix.')
                        foundit = 1
                        break
                except:
                    pass
        except Exception as e:
            logger.info(f'Error: {e}')
        Assertion.assert_equal(foundit, 1, "ERR: pd route not in PBR table.")
        output = ao_obj.get_addressobject_by_name(name='X2 Delegated Prefix',version='ipv6')
        subnet= output['address_objects'][0]['ipv6']['network']['subnet']
        Assertion.assert_regular(subnet, Parameter.PD_PREFIX_NEW, "ERR: Check AO failed")

    def test_021_09_stop_cdrouter(self):
        rc = cdrouter_new.terminate_case()
        interface.click_dhcp_release('X2',version='v6')
        time.sleep(30)
        Assertion.assert_equal(rc, True, "ERR: stop cdrotuer test fail.")