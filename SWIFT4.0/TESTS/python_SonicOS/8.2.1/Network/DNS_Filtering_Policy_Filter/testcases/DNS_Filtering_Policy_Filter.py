from definition.settings import *
from definition.utils import *


class TestCheck_and_change_dns_server(Test):
    uuid = 'NonTC'
    description = 'TestCheck_and_change_dns_server'
    goto_teardown = True

    def test_01_check_dns_server(self):
        dns_server = Parameter.Neustar_server
        cmd = f'ping {dns_server} -c 5'
        out = PC1_LOGIN.send_command(cmd)
        logger.info(out)
        if '100% packet loss' not in out:
            logger.info(f'Can access to dns server {dns_server}')
        else:
            Assertion.fail('Cannot access to dns server')

    def test_02_change_dns_server(self):
        test_option = {
            'primary': Params.G_DNS1,
            'secondary': Params.G_DNS2,
            'tertiary': Params.G_DNS3
        }
        rc = dnsSett_api.edit_ipv4_dns(**test_option)
        Assertion.assert_equal(rc, True, "ERR: Change dns servers failed")


# Expected: enable the DNS Policy works
class TestSettings_01(Test):
    uuid = "SOSAIOT-TC-51401"
    # uuid = '61789D9C-4CFC-11EC-B737-3362918F55E4'
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_rule(self):
        rc = dnsRule_api.add_dns_rule(**add_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_rule failed")

    def test_02_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = config_packet_monitor()
        Assertion.assert_equal(out, True, "ERR: Config packet monitor failed")
    
    @repeat_method(3)
    def test_03_do_dig_ea_to_verify_DNS_query(self):
        packet_api.start_capture()
        rc = do_dig_verify_DNS_query('www.ea.com')
        Assertion.assert_equal(rc[0], True, "ERR: Dig_www.ea failed")

    def test_04_check_DNS_reply_from_Neustar(self):
        found = check_DNS_reply_from_Server()
        Assertion.assert_equal(found, True, "ERR:failed to find expected packets")

    def test_05_delete_added_dns_rule(self):
        rc = dnsRule_api.del_dns_rule_by_name(add_rule_dict['dns_policies'][0]['name'])
        Assertion.assert_equal(rc, True, "ERR: Delete_dns_rule failed")


# Expected: disable the DNS Policy works
class TestSettings_02(Test):
    uuid = "SOSAIOT-TC-51402"
    # uuid = '617B9D8A-4CFC-11EC-B737-3362918F55E4'
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_rule(self):
        dis_rule = copy.deepcopy(add_rule_dict)
        dis_rule['dns_policies'][0].update({'enable': False})
        rc = dnsRule_api.add_dns_rule(**dis_rule)
        Assertion.assert_equal(rc, True, "ERR: add_dns_rule failed")

    def test_02_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = config_packet_monitor()
        Assertion.assert_equal(out, True, "ERR: Config packet monitor failed")

    def test_03_do_dig_ea_to_verify_DNS_query(self):
        packet_api.start_capture()
        rc = do_dig_verify_DNS_query('www.ea.com', block=True)
        Assertion.assert_equal(rc[0], True, "ERR: Dig_www.ea should fail")

    def test_04_delete_added_dns_rule(self):
        rc = dnsRule_api.del_dns_rule_by_name(add_rule_dict['dns_policies'][0]['name'])
        Assertion.assert_equal(rc, True, "ERR: Delete_dns_rule failed")


# Expected: the Profile of DNS Policy works
class TestSettings_03(Test):
    uuid = "SOSAIOT-TC-51403"
    # uuid = '617D696C-4CFC-11EC-B737-3362918F55E4'
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_new_dns_profile(self):
        rc = dnsFilter_api.add_dns_filtering_profile(**add_file_dict)
        Assertion.assert_equal(rc, True, "ERR: Add_dns_filtering_profile failed")

    def test_02_add_dns_rule(self):
        pro_name = add_file_dict['dns_security']['dns_filtering']['profile'][0]['name']
        pro_rule = copy.deepcopy(add_rule_dict)
        pro_rule['dns_policies'][0]['action'].update({'filter_profile': pro_name})
        rc = dnsRule_api.add_dns_rule(**pro_rule)
        Assertion.assert_equal(rc, True, "ERR: add_dns_rule failed")

    def test_03_config_packet_monitor(self):
        out = config_packet_monitor()
        Assertion.assert_equal(out, True, "ERR: Config packet monitor failed")

    def test_04_do_dig_ea_to_verify_DNS_query(self):
        packet_api.start_capture()
        out = do_dig_verify_DNS_query('www.ea.com')
        target = 'SERVFAIL'
        rc = target in out[1] if out[0] else False
        Assertion.assert_equal(rc, True, "ERR: Dig_www.ea failed")

    def test_05_delete_added_dns_rule(self):
        rc = dnsRule_api.del_dns_rule_by_name(add_rule_dict['dns_policies'][0]['name'])
        Assertion.assert_equal(rc, True, "ERR: Delete_dns_rule failed")


# Expected: the DNS Policy works on LAN/DMZ/Custom Zone
class TestBaseFun_04(Test):
    uuid = "SOSAIOT-TC-51404"
    # uuid = '617FA236-4CFC-11EC-B737-3362918F55E4'
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']
    TC04_zone = 'DMZ'
    TC04_ifc = 'X0'
    TC04_ifc_ip = Parameter.FIREWALL
    TC04_host = PC1_LOGIN

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    ##################### Check on LAN Zone ##############
    def test_01_add_dns_rule(self):
        logger.info(f"{f' Check on LAN zone':=^70}")
        rc = dnsRule_api.add_dns_rule(**add_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_rule failed")

    def test_02_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = config_packet_monitor()
        Assertion.assert_equal(out, True, "ERR: Config packet monitor failed")

    def test_03_do_dig_ea_to_verify_DNS_query(self):
        packet_api.start_capture()
        time.sleep(3)
        rc = do_dig_verify_DNS_query('www.ea.com', host=self.TC04_host, server=self.TC04_ifc_ip)
        Assertion.assert_equal(rc[0], True, "ERR: Dig_www.ea failed")

    def test_04_check_DNS_reply_from_Neustar(self):
        found = check_DNS_reply_from_Server(ifc=self.TC04_ifc)
        Assertion.assert_equal(found, True, "ERR:failed to find expected packets")

    ##################### Check on DMZ Zone ##############
    def test_05_config_DMZ_interface(self):
        logger.info(f"{f' Config DMZ interface ':=^60}")
        rc = interface_api.config_interface(**config_X2_dict)
        Assertion.assert_equal(rc, True, "ERR: Config DMZ interface on X2 failed!")

    def test_06_add_dns_rule_on_multi_zone(self):
        logger.info(f"{f' Create DNS Rule on {self.TC04_zone} ':=^60}")
        add_rule_zone = copy.deepcopy(add_rule_dict)
        zone = {
            "name": self.TC04_zone,
            "from": self.TC04_zone,
        }
        add_rule_zone["dns_policies"][0].update(zone)
        rc = dnsRule_api.add_dns_rule(**add_rule_zone)
        Assertion.assert_equal(rc, True, "ERR: Create DNS Rule on DMZ failed!")

    def test_07_config_packet_monitor(self):
        self.test_02_config_packet_monitor()

    def test_08_do_dig_ea_to_verify_DNS_query(self):
        self.TC04_ifc_ip = Parameter.DUT_X2
        self.TC04_host = PC2_LOGIN
        self.test_03_do_dig_ea_to_verify_DNS_query()

    def test_09_check_DNS_reply_from_Neustar(self):
        self.TC04_ifc = 'X2'
        self.test_04_check_DNS_reply_from_Neustar()

    ##################### Check on Custom Zone ##############
    def test_10_config_custom_zone_interface(self):
        logger.info(f"{f' Config custom_zone interface ':=^60}")
        config_x3 = copy.deepcopy(config_X2_dict)
        x3 = {
            'if': 'X3',
            'zone': custom_zone_dict["zones"][0]['name'],
            'ip': Parameter.DUT_X3
        }
        config_x3.update(x3)
        rc = interface_api.config_interface(**config_x3)
        Assertion.assert_equal(rc, True, "ERR: Config custom zone interface on X3 failed!")

    def test_11_check_dns_filter_on_custom_zone(self):
        self.TC04_zone = custom_zone_dict["zones"][0]['name']
        self.test_06_add_dns_rule_on_multi_zone()

    def test_12_config_packet_monitor(self):
        self.test_02_config_packet_monitor()

    def test_13_do_dig_ea_to_verify_DNS_query(self):
        self.TC04_ifc_ip = Parameter.DUT_X3
        self.TC04_host = PC2_LOGIN
        self.test_03_do_dig_ea_to_verify_DNS_query()

    def test_14_check_DNS_reply_from_Neustar(self):
        self.TC04_ifc = 'X3'
        self.test_04_check_DNS_reply_from_Neustar()

    def test_15_delete_added_dns_rules(self):
        rc1 = dnsRule_api.del_dns_rule_by_name(add_rule_dict['dns_policies'][0]['name'])
        rc2 = dnsRule_api.del_dns_rule_by_name('DMZ')
        rc3 = dnsRule_api.del_dns_rule_by_name(custom_zone_dict["zones"][0]['name'])
        logger.info(f'=====> Delete LAN-DMZ-custom_zone dns rules Results: {rc1}-{rc2}-{rc3}')
        Assertion.assert_equal(rc1 & rc2 & rc3, True, "ERR: Delete added dns rule failed")


# Expected: the Priority of DNS Policy works
class TestSettings_11(Test):
    uuid = "SOSAIOT-TC-51405"
    # uuid = '618F62D4-4CFC-11EC-B737-3362918F55E4'
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_filter_rule(self):
        rc = dnsRule_api.add_dns_rule(**add_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_rule failed")

    def test_02_add_dns_proxy_rule(self):
        proxy = {
            "name": 'proxy',
            "action": {
                "proxy": True
            },
            "proxy_mode": "ipv4-ipv4"
        }
        add_proxy_rule = copy.deepcopy(add_rule_dict)
        add_proxy_rule["dns_policies"][0].update(proxy)
        rc = dnsRule_api.add_dns_rule(**add_proxy_rule)
        Assertion.assert_equal(rc, True, "ERR: add_dns_proxy_rule failed")

    # ##################### proxy top #####################
    def test_03_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = config_packet_monitor()

    def test_04_do_dig_ea_to_verify_DNS_query(self):
        packet_api.start_capture()
        rc = do_dig_verify_DNS_query('www.ea.com')
        Assertion.assert_equal(rc[0], True, "ERR: Dig_www.ea failed")

    def test_05_check_DNS_reply_from_Default_Server(self):
        found = False
        for dns in [Params.G_DNS1, Params.G_DNS2, Params.G_DNS3]:
            found = check_DNS_reply_from_Server(server=dns)
            if found:
                break
        Assertion.assert_equal(found, True, "ERR: failed to find expected packets")

     # ##################### filter top #####################
    def test_06_change_filter_rule_to_top(self):
        priority = {
            "name": add_rule_dict['dns_policies'][0]['name'],
            "priority": {
                "manual": 1
            }
        }
        rc = dnsRule_api.edit_dns_rule(**priority)
        Assertion.assert_equal(rc, True, "ERR: Change_proxy_rule_to_top failed")

    def test_07_config_packet_monitor(self):
        self.test_03_config_packet_monitor()

    def test_08_do_dig_ea_to_verify_DNS_query(self):
        self.test_04_do_dig_ea_to_verify_DNS_query()

    def test_09_check_DNS_reply_from_Neustar(self):
        foundit = check_DNS_reply_from_Server()
        Assertion.assert_equal(foundit, True, "ERR:failed to find expected packets")

    def test_10_delete_added_dns_rules(self):
        rc1 = dnsRule_api.del_dns_rule_by_name(add_rule_dict['dns_policies'][0]['name'])
        rc2 = dnsRule_api.del_dns_rule_by_name('proxy')
        logger.info(f'=====> Delete filter-proxy dns rules Results: {rc1}-{rc2}')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Delete added dns rule failed")


# Expected: the Address of DNS Policy works
class TestSettings_12(Test):
    uuid = "SOSAIOT-TC-51406"
    # uuid = '61916DAE-4CFC-11EC-B737-3362918F55E4'
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_rule(self):
        address = {
            "source": {
                "address": {
                    "name": ao_dict['name']
                }
            }
        }
        addr_rule = copy.deepcopy(add_rule_dict)
        addr_rule['dns_policies'][0].update(address)
        rc = dnsRule_api.add_dns_rule(**addr_rule)
        Assertion.assert_equal(rc, True, "ERR: add_dns_rule failed")

    def test_02_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = config_packet_monitor()
        Assertion.assert_equal(out, True, "ERR: Config packet monitor failed")

    def test_03_do_dig_ea_to_verify_DNS_query(self):
        packet_api.start_capture()
        rc = do_dig_verify_DNS_query('www.ea.com')
        Assertion.assert_equal(rc[0], True, "ERR: Dig_www.ea failed")

    def test_04_check_DNS_reply_from_Neustar(self):
        found = check_DNS_reply_from_Server()
        Assertion.assert_equal(found, True, "ERR:failed to find expected packets")

    def test_05_change_dns_rule_with_new_address(self):
        address = {
            "name": add_rule_dict['dns_policies'][0]['name'],
            "source": {
                "address": {
                    "name": "New"
                }
            }
        }
        rc = dnsRule_api.edit_dns_rule(**address)
        Assertion.assert_equal(rc, True, "ERR: Edit_dns_rule failed")

    def test_06_config_packet_monitor(self):
        self.test_02_config_packet_monitor()

    def test_07_do_dig_ea_to_verify_DNS_query(self):
        packet_api.start_capture()
        rc = do_dig_verify_DNS_query('www.ea.com', block=True)
        Assertion.assert_equal(rc[0], True, "ERR: Dig_www.ea should be failed")

    def test_08_delete_added_dns_rules(self):
        rc = dnsRule_api.del_dns_rule_by_name(add_rule_dict['dns_policies'][0]['name'])
        Assertion.assert_equal(rc, True, "ERR: Delete added dns rule failed")


# Expected: the Service of DNS Policy works
class TestSettings_13(Test):
    uuid = "SOSAIOT-TC-51407"
    # uuid = '61934980-4CFC-11EC-B737-3362918F55E4'
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_rule(self):
        rc = dnsRule_api.add_dns_rule(**add_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_rule failed")

    def test_02_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = config_packet_monitor()
        Assertion.assert_equal(out, True, "ERR: Config packet monitor failed")

    def test_03_do_dig_ea_to_verify_DNS_query(self):
        packet_api.start_capture()
        rc = do_dig_verify_DNS_query('www.ea.com')
        Assertion.assert_equal(rc[0], True, "ERR: Dig_www.ea failed")

    def test_04_do_dig_ea_to_verify_DNS_query_tcp(self):
        packet_api.start_capture()
        time.sleep(3)
        out = do_dig_verify_DNS_query('www.ea.com', opt='+tcp')
        target = 'connection refused'
        rc = target in out[1] if out[0] else False
        Assertion.assert_equal(rc, True, "ERR: Dig_www.ea should fail")

    def test_05_delete_added_dns_rules(self):
        rc = dnsRule_api.del_dns_rule_by_name(add_rule_dict['dns_policies'][0]['name'])
        Assertion.assert_equal(rc, True, "ERR: Delete added dns rule failed")
