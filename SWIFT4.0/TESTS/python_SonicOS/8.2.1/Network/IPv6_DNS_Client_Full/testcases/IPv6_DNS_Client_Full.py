from definition.settings import *


# Verify DNS Server 2 can inherit ipv6 dns setting from primary wan interface
class TestIPv6DNS_TC03(Test):
    uuid = "SOSAIOT-TC-51396"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_specify_ipv6_dns_server_inherit(self):
        logger.info('configure ipv6 dns server inherited from the wan interface...')
        dns_opt = copy.deepcopy(dns_dict)
        dns_opt["dns"]["server"]["ipv6"]["inherit"] = True
        rc = dns_api.set_dns(**dns_opt)
        Assertion.assert_equal(rc, True, "ERR: configure ipv6 dns server inherited from the wan interface Failed!")

    def test_02_config_interface_X1(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            "dns": {
                "primary": Parameter.IPV6_DNS1,
                "secondary": Parameter.IPV6_DNS2,
                "tertiary": "::"
            },
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_03_verify_DNS_Server2_can_inherit_ipv6_dns_setting_from_primary_wan_interface(self):
        logger.info('verify DNS server can inherit ipv6 dns setting from primary wan interface...')
        flag = False
        output = diag_api.get_tsr_part(func='Network', lab1='DNS')
        logger.info(output)
        if re.search(r"IPv6\s+DNS\s+Server\s+2:\s+{}".format(Parameter.IPV6_DNS2), str(output), re.S | re.I | re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify DNS server2 can inherit \
                                ipv6 dns setting from primary wan interface failed")


# Verify DNS Server 3 can inherit ipv6 dns setting from primary wan interface
class TestIPv6DNS_TC04(Test):
    uuid = "SOSAIOT-TC-51397"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_X1(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            "dns": {
                "primary": Parameter.IPV6_DNS1,
                "secondary": Parameter.IPV6_DNS2,
                "tertiary": Parameter.IPV6_DNS3
            },
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_verify_DNS_Server3_can_inherit_ipv6_dns_setting_from_primary_wan_interface(self):
        logger.info('verify DNS server3 can inherit ipv6 dns setting from primary wan interface...')
        flag = False
        output = diag_api.get_tsr_part(func='Network', lab1='DNS')
        logger.info(output)
        if re.search(r"IPv6\s+DNS\s+Server\s+3:\s+{}".format(Parameter.IPV6_DNS3), str(output), re.S | re.I | re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify DNS server2 can inherit \
                                ipv6 dns setting from primary wan interface failed")


# Verify DNS Server 2 can be specified manually
class TestIPv6DNS_TC08(Test):
    uuid = "SOSAIOT-TC-51399"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_specify_ipv6_dns_server2_manually(self):
        logger.info('specify ipv6 dns server2 manually...')
        dns_opt = copy.deepcopy(dns_dict)
        dns_opt["dns"]["server"]["ipv6"]["static"]["secondary"] = Parameter.IPV6_DNS2
        rc = dns_api.set_dns(**dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server1 manually Failed!")

    def test_03_check_DNS_server_settings(self):
        logger.info('check DNS server settings...')
        flag = False
        output = diag_api.get_tsr_part(func='Network', lab1='DNS')
        logger.info(output)
        if re.search(r"IPv6\s+DNS\s+Server\s+2:\s+{}".format(Parameter.IPV6_DNS2), str(output), re.S | re.I | re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check DNS server settings Failed!")


#  Verify DNS Server 3 can be specified manually
class TestIPv6DNS_TC09(Test):
    uuid = "SOSAIOT-TC-51400"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_specify_ipv6_dns_server3_manually(self):
        logger.info('specify ipv6 dns server1 manually...')
        dns_opt = copy.deepcopy(dns_dict)
        dns_opt["dns"]["server"]["ipv6"]["static"]["tertiary"] = Parameter.IPV6_DNS3
        rc = dns_api.set_dns(**dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server1 manually Failed!")

    def test_03_check_DNS_server_settings(self):
        logger.info('check DNS server settings...')
        flag = False
        output = diag_api.get_tsr_part(func='Network', lab1='DNS')
        logger.info(output)
        if re.search(r"IPv6\s+DNS\s+Server\s+3:\s+{}".format(Parameter.IPV6_DNS3), str(output), re.S | re.I | re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check DNS server settings Failed!")

    def test_04_export_exp_verify_tc110(self):
        res = set_api.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: export exp file failed")


# Verify DNSv6 server settings can be inherited from the wan interface if the wan interface is in DHCPv6 mode.
class TestIPv6DNS_TC06(Test):
    uuid = "SOSAIOT-TC-51398"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']
    res_for_tsr = ContextVar('res_for_tsr')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_specify_ipv6_dns_server_inherit(self):
        logger.info('configure ipv6 dns server inherited from the wan interface...')
        dns_opt = copy.deepcopy(dns_dict)
        dns_opt["dns"]["server"]["ipv6"]["inherit"] = True
        rc = dns_api.set_dns(**dns_opt)
        Assertion.assert_equal(rc, True, "ERR: configure ipv6 dns server inherited from the wan interface Failed!")

    @repeat_method(5)
    def test_02_config_interface_X1(self):
        flag = False
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'zone': 'WAN',
            "dhcpv6": {
                "mode": "auto",
                "rapid_commit": True,
                "info_only": False
            },
            'listen_router_advertisement': True,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc1 = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        logger.info(f"config x1 ipv6 as dhcpv6 auto mode : {rc1}")
        rc2 = if_v4_api.click_dhcp_renew(name='X1', version='v6')
        logger.info(f"renew x1 ipv6 : {rc2}")
        time.sleep(10)
        ip_addr = if_v4_api.get_interface_address(name='X1', version='v6')
        if type(ip_addr) is dict :
            if '2001:2011:2:3::' in ip_addr['ip_address'] and 'DHCPv6' in ip_addr['ip_address']:
                flag = True
                dns_tupple = (ip_addr['primary_dns'],ip_addr['secondary_dns'],ip_addr['tertiary_dns'])
                logger.info(f"DNSv6 server inherited from interface which in wan DHCPv6 mode is {dns_tupple}")
        Assertion.assert_equal(flag, True,  "ERR: config client X1 IPv6 failed")

    def test_03_check_DNS_server_settings(self):
        logger.info('check DNS server settings...')
        flag = False
        output = diag_api.get_tsr_part(func='Network', lab1='DNS')
        logger.info(output)
        checkres = [x in str(output) for x in dns_tupple]
        if all(checkres):
            flag = True
        self.res_for_tsr.set(flag)
        Assertion.assert_equal(flag, True, "ERR: check DNS server settings Failed!")


# Prefs Import and Export
class TestIPv6DNS_TC15(Test):
    uuid = "SOSAIOT-TC-51395"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_import_exp(self):
        res = set_api.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_02_check_DNS_server_settings(self):
        logger.info('check DNS server settings...')
        flag = False
        output = diag_api.get_tsr_part(func='Network', lab1='DNS')
        logger.info(output)
        if re.search(r"IPv6\s+DNS\s+Server\s+3:\s+{}".format(Parameter.IPV6_DNS3), str(output), re.S | re.I | re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check DNS server settings Failed!")


# The DNSv6 Server settings are intact after firewall reboot
class TestIPv6DNS_TC13(Test):
    uuid = "SOSAIOT-TC-51393"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']
    res_for_tsr = ContextVar('res_for_tsr')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_specify_ipv6_dns_server2_manually(self):
        logger.info('specify ipv6 dns server2 manually...')
        dns_opt = copy.deepcopy(dns_dict)
        dns = {
            "primary": Parameter.IPV6_DNS1,
            "secondary":Parameter.IPV6_DNS2,
            "tertiary": Parameter.IPV6_DNS3
        },
        dns_opt["dns"]["server"]["ipv6"]["static"] = dns
        rc = dns_api.set_dns(**dns_opt)
        Assertion.assert_equal(rc, True, "ERR: specify ipv6 dns server1 manually Failed!")

    def test_02_reboot(self):
        rc = set_api.boot_fw(1)
        Assertion.assert_equal(rc, True, f"ERR: reboot failed.")

    def test_03_check_DNS_server_settings(self):
        logger.info('check DNS server settings...')
        flag = False
        output = diag_api.get_tsr_part(func='Network', lab1='DNS')
        logger.info(output)
        manual_dns_tupple = (Parameter.IPV6_DNS1, Parameter.IPV6_DNS2, Parameter.IPV6_DNS3)
        checkres = [x in str(output) for x in manual_dns_tupple]
        if all(checkres):
            flag = True
        self.res_for_tsr.set(flag)
        Assertion.assert_equal(flag, True, "ERR: check DNS server settings Failed!")


# TSR support
class TestIPv6DNS_TC14(Test):
    uuid = "SOSAIOT-TC-51394"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_tsr(self):
        res_manual = TestIPv6DNS_TC13().res_for_tsr.get()
        res_inherited  = TestIPv6DNS_TC06().res_for_tsr.get()
        logger.info('check tsr: {}'.format(res_manual&res_inherited))
        Assertion.assert_equal(res_manual&res_inherited, True, "ERR: check tsr failed")
