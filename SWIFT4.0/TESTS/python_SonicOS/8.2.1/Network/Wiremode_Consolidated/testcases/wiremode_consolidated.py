from definition.settings import *
from definition.utils import *


# Configure interface to lan/wan/dmz in Wire Mode - Bypass mode successful.
class TestGUI_TC1(Test):
    uuid = "SOSAIOT-TC-57448"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2(self):
        tag = []
        zones = ['LAN', 'WAN', 'DMZ']
        for zone in zones:
            X2_wiremode_dict['zone'] = zone
            output = interfaceapi.config_interface(**X2_wiremode_dict)
            tag.append(output)
            logger.info(f'config wire mode zone {zone} result: {output}')

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(all(tag), True, "ERR: Config X2 to bypass mode failed")


# Configure interface to lan/wan/dmz in Wire Mode - Inspect mode successful.
class TestGUI_TC2(Test):
    uuid = "SOSAIOT-TC-57455"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2(self):
        tag = []
        zones = ['LAN', 'WAN', 'DMZ']
        X2_wiremode_dict['type'] = 'inspect'
        for zone in zones:
            X2_wiremode_dict['zone'] = zone
            output = interfaceapi.config_interface(**X2_wiremode_dict)
            tag.append(output)
            logger.info(f'config wire mode zone {zone} result: {output}')

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(all(tag), True, "ERR: Config X2 to inspect mode failed")


# Configure interface to lan/wan/dmz in Wire Mode - Secure mode successful.
class TestGUI_TC3(Test):
    uuid = "SOSAIOT-TC-57464"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2(self):
        tag = []
        zones = ['LAN', 'WAN', 'DMZ']
        X2_wiremode_dict['type'] = 'secure'
        for zone in zones:
            X2_wiremode_dict['zone'] = zone
            output = interfaceapi.config_interface(**X2_wiremode_dict)
            tag.append(output)
            logger.info(f'config wire mode zone {zone} result: {output}')

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(all(tag), True, "ERR: Config X2 to secure mode failed")


# Configure interface to lan/wan/dmz in TAP Mode successful.
# skip.   configure tap mode in openstack will reboot fw.
# class TestGUI_TC4(Test):
#     uuid = '1511458'
#     description = show_testcase_info(TESTPLAN, '4', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '4')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_config_x2(self):
#         tag = []
#         zones = ['DMZ', 'WAN', 'LAN']
#         for zone in zones:
#             X2_wiremode_dict['zone'] = zone
#             output = interfaceapi.config_interface(**x2_tapmode_dict)
#             tag.append(output)
#             logger.info(f'config tap mode zone {zone} result: {output}')
#
#         interfaceapi.unassign_interface(interface='X2')
#         Assertion.assert_equal(all(tag), True, "ERR: check zones from X2 failed")


# ping/http/ftp traffic passed between PC1 and PC2 Server in Wiremode- Bypass mode
class TestBaseFun_TC20(Test):
    # duplicate by WireMode_2580
    uuid = ''
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_wiremode(self):
        X2_wiremode_dict['type'] = 'bypass'
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to bypass mode failed")

    def test_02_restart_fw(self):
        output = restartapi.restart_now()
        Assertion.assert_equal(output, True, "ERR: restart fw failed")

    def test_03_check_wiremode_settings(self):
        output = interfaceapi.get_interface_status(name='X2')
        res = True if ('zone\': \'LAN' and 'type\': \'bypass') in str(output) else False

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(res, True, "ERR: check wiremode configure failed")


# ping/http/ftp traffic passed between PC1 and PC2 Server in Wiremode- Bypass mode
class TestBaseFun_TC22(Test):
    uuid = "SOSAIOT-TC-57457"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2(self):
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to bypass mode failed")

    def test_02_verify_ping_traffic(self):
        time.sleep(5)
        output = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 5)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_03_verify_http_traffic(self):
        output = http_send.Http_get()
        Assertion.assert_equal(output, True, "ERR: verify http traffic failed.")

    def test_04_verify_ftp_traffic(self):
        my_ftp.login()
        output = my_ftp.download_file(localfile, remotefile)

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')


# ping/http/ftp traffic passed between PC1 and PC2 Server in Wiremode- inspect mode
class TestBaseFun_TC23(Test):
    uuid = "SOSAIOT-TC-57458"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2(self):
        X2_wiremode_dict['type'] = 'inspect'
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    @repeat_method(3)
    def test_02_verify_ping_traffic(self):
        time.sleep(60)
        output = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 5)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_03_verify_http_traffic(self):
        output = http_send.Http_get()
        Assertion.assert_equal(output, True, "ERR: verify http traffic failed.")

    def test_04_verify_ftp_traffic(self):
        my_ftp.login()
        output = my_ftp.download_file(localfile, remotefile)

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')


# ping/http/ftp traffic passed between PC1 and PC2 Server in Wiremode- secure mode
class TestBaseFun_TC24(Test):
    uuid = "SOSAIOT-TC-57459"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_and_pc2_ip(self):
        X2_wiremode_dict['type'] = 'secure'
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        command = 'ifconfig eth0 ' + Parameter.PC2_ETH0_NewIP
        PC2_login.send_command(command)

        # restartapi.restart_now()
        Assertion.assert_equal(output, True, "ERR: Config X2 to secure mode failed")

    @repeat_method(3)
    def test_02_verify_ping_traffic(self):
        time.sleep(20)
        output = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_03_verify_http_traffic(self):
        output = http_send.Http_get()
        Assertion.assert_equal(output, True, "ERR: verify http traffic failed.")

    def test_04_verify_ftp_traffic(self):
        my_ftp.login()
        output = my_ftp.download_file(localfile, remotefile)

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')


# Because of erratic FTP downloads, replace it with an ICMP test
# ping traffic blocked after set icmp app rule in Wiremode- inspect mode
class TestBaseFun_TC33(Test):
    uuid = "SOSAIOT-TC-57468"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']
    TC33_march_obj = 'tc33_icmp'
    TC33_app_rules = 'tc33_icmp_block'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_wiremode_to_inspect(self):
        X2_wiremode_dict['type'] = 'inspect'
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    def test_02_config_apprule(self):
        enable_app_rules_dict = {
            'enable': True,
            'log_redundancy': {}
        }
        output = apprulesapi.config_apprule_setting(**enable_app_rules_dict)
        Assertion.assert_equal(output, True, "ERR: enable app rules failed")

    def test_03_add_match_object_for_icmp(self):
        logger.info('add match object and app rule...')
        match_opt_dict['name'] = self.TC33_march_obj
        res = matchobjapi.config_matchobject(**match_opt_dict)
        Assertion.assert_equal(res, True, "ERR:config icmp match object failed")

    def test_04_add_app_rule_for_icmp(self):
        apprule_dict['app_rules']['policy'][0]['match_object']['object'] = self.TC33_march_obj
        apprule_dict['app_rules']['policy'][0]['name'] = self.TC33_app_rules
        res = apprulesapi.add_apprule(**apprule_dict)
        Assertion.assert_equal(res, True, "ERR: add app rule for icmp block failed")

    # @repeat_method(5)
    def test_05_verify_ping_traffic_and_log(self):
        fw_time = timeapi.show_time()
        time.sleep(20)
        output1 = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 3)
        logger.info(f'ping to pc2 eth0 result: {output1}')
        output = False if output1 else True
        fw_logs = logapi.get_log(793)
        output2 = check_log_by_time(fw_time, fw_logs, log_id=793)
        logger.info(f'check log event result: {output2}')
        Assertion.assert_equal(output & output2, True, "ERR: verify ping traffic and app rule log failed")

    def test_06_init_objects_rules(self):
        res = apprulesapi.delete_apprule_object_byname(name=self.TC33_app_rules)
        res &= matchobjapi.del_match_object_by_name(name=self.TC33_march_obj)
        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(res, True, "ERR: init match object and app rules failed")


# gav file will be blocked via ftp download between PC1 and PC2 Server in Wiremode- secure mode
class TestBaseFun_TC38(Test):
    # duplicate by WireMode_2580
    uuid = ''
    description = show_testcase_info(TESTPLAN, '38', description=True)['title']
    jira = 'GEN7-26371'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_wire_mode(self):
        X2_wiremode_dict['type'] = 'secure'
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    def test_02_enable_GAV(self):
        gav_dict = {
            'enable_GAV': True,
            'inbound_ftp': True,
        }
        res = gav.config_gav(**gav_dict)
        Assertion.assert_equal(res, True, "ERR: enable GAV failed")

    def test_03_verify_ftp_gav_blocked(self):
        fw_time = timeapi.show_time()
        time.sleep(20)
        my_ftp.login()
        output1 = my_ftp.download_file(localgavfile, remotegavfile)
        logger.info(f'download gav file result: {output1}')
        output3 = False if output1 else True

        fw_logs = logapi.get_log(809)
        output2 = check_log_by_time(fw_time, fw_logs, log_id=809)
        logger.info(f'check log event result: {output2}')

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(output2 & output3, True, "ERR: the FW block the Anti-Virus failed")


# check restrict_analysis configure in x2 wire mode
class TestGUI_TC66(Test):
    uuid = "SOSAIOT-TC-57493"
    description = show_testcase_info(TESTPLAN, '66', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '66')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_wire_mode(self):
        interfaceapi.unassign_interface(interface='X2')
        X2_wiremode_dict['type'] = 'inspect'
        X2_wiremode_dict['restrict_analysis'] = True
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    def test_03_check_wiremode_settings(self):
        output = interfaceapi.get_interface_status(name='X2')
        res = True if ('restrict_analysis\': True' and 'type\': \'inspect') in str(output) else False

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(res, True, "ERR: check wiremode configure failed")


# check traffic after config restrict_analysis true in x2
class TestGUI_TC67(Test):
    uuid = "SOSAIOT-TC-57494"
    description = show_testcase_info(TESTPLAN, '67', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '67')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_wire_mode(self):
        X2_wiremode_dict['type'] = 'inspect'
        X2_wiremode_dict['restrict_analysis'] = True
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    @repeat_method(3)
    def test_02_verify_ping_traffic(self):
        time.sleep(10)
        output = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_03_verify_http_traffic(self):
        output = http_send.Http_get()
        Assertion.assert_equal(output, True, "ERR: verify http traffic failed.")

    def test_04_verify_ftp_traffic(self):
        my_ftp.login()
        output = my_ftp.download_file(localfile, remotefile)

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')


# only check the ftp gav file download after restart FW
class TestBaseFun_TC76(Test):
    uuid = "SOSAIOT-TC-57501"
    description = show_testcase_info(TESTPLAN, '76', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '76')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_wire_mode(self):
        X2_wiremode_dict['type'] = 'secure'
        X2_wiremode_dict['restrict_analysis'] = False
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    def test_02_restart_fw(self):
        output = restartapi.restart_now()
        Assertion.assert_equal(output, True, "ERR: restart fw failed")

    def test_03_config_x2_wire_mode(self):
        X2_wiremode_dict['type'] = 'bypass'
        X2_wiremode_dict['restrict_analysis'] = False
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    def test_04_verify_ftp_gav_passed(self):
        time.sleep(20)
        my_ftp.login()
        output = my_ftp.download_file(localgavfile, remotegavfile)
        logger.info(f'download gav file result: {output}')

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(output, True, "ERR: the ftp download gav file failed")


# X3 will not link after set wire_link_propagation to True in X2
class TestBaseFun_TC80(Test):
    uuid = "SOSAIOT-TC-57505"
    description = show_testcase_info(TESTPLAN, '80', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '80')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_wire_mode(self):
        X2_wiremode_dict['type'] = 'bypass'
        X2_wiremode_dict['wire_link_propagation'] = True
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    def test_02_unplug_x2_interface(self):
        output = os_obj.set_node_interface_state('UTM', 'X2', 'disable')
        Assertion.assert_equal(output, True, "ERR: unplug X2 failed")

    def test_03_check_link_down_for_x3(self):
        output = interfacecli.show_interface_status(interface='X3 status')
        res = True if 'No link' in output else False
        Assertion.assert_equal(res, True, "ERR: check link down for x3 failed")


# use the TC80 setting to test.
# X3 will link up after plug X2
class TestBaseFun_TC82(Test):
    uuid = "SOSAIOT-TC-57506"
    description = show_testcase_info(TESTPLAN, '82', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '82')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_plug_x2_interface(self):
        output = os_obj.set_node_interface_state('UTM', 'X2', 'enable')
        Assertion.assert_equal(output, True, "ERR: plug X2 failed")

    def test_02_check_link_up_for_x3(self):
        res = False
        for i in range(3):
            time.sleep(10)
            output = interfacecli.show_interface_status(interface='X3 status')
            if 'No link' not in output:
                res = True
                break

        interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(res, True, "ERR: check link up for x3 failed")


# ping/http/ftp traffic passed after set Wiremode- inspect mode in x2
class TestEnhancements_TC12(Test):
    uuid = "SOSAIOT-TC-57521"
    description = show_testcase_info(TESTPLAN, 'enh12', description=True)['title']
    TCenh12_march_obj = 'tcenh12_icmp'
    TCenh12_app_rules = 'tcenh12_icmp_block'
    jira = 'GEN7-26371'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'enh12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_wire_modenfig_x2_and_pc1_eth1(self):
        X2_wiremode_dict['type'] = 'inspect'
        X2_wiremode_dict['wire_paired_zone'] = 'DMZ'
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    def test_02_config_apprule(self):
        enable_app_rules_dict = {
            'enable': True,
            'log_redundancy': {}
        }
        output = apprulesapi.config_apprule_setting(**enable_app_rules_dict)
        Assertion.assert_equal(output, True, "ERR: enable app rules failed")

    def test_03_add_match_object_for_icmp(self):
        logger.info('add match object and app rule...')
        match_opt_dict['name'] = self.TCenh12_march_obj
        res = matchobjapi.config_matchobject(**match_opt_dict)
        Assertion.assert_equal(res, True, "ERR:config icmp match object failed")

    def test_04_add_app_rule_for_icmp(self):
        apprule_dict['app_rules']['policy'][0]['match_object']['object'] = self.TCenh12_march_obj
        apprule_dict['app_rules']['policy'][0]['name'] = self.TCenh12_app_rules
        res = apprulesapi.add_apprule(**apprule_dict)
        Assertion.assert_equal(res, True, "ERR: add app rule for icmp block failed")

    def test_05_verify_http_traffic(self):
        output = http_send.Http_get()
        Assertion.assert_equal(output, True, "ERR: verify http traffic failed.")

    @repeat_method(5)
    def test_06_verify_ping_traffic_and_log(self):
        fw_time = timeapi.show_time()
        time.sleep(20)
        output1 = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 3)
        logger.info(f'ping to pc2 eth0 result: {output1}')

        fw_logs = logapi.get_log(793)
        output2 = check_log_by_time(fw_time, fw_logs, log_id=793)
        logger.info(f'check log event result: {output2}')
        # output2 = False if output2 else True
        Assertion.assert_equal(output1 & output2, True, "ERR: verify ping traffic and app rule log failed")

    def test_08_init_objects_rules(self):
        res = apprulesapi.delete_apprule_object_byname(name=self.TCenh12_app_rules)
        res &= matchobjapi.del_match_object_by_name(name=self.TCenh12_march_obj)
        interfaceapi.unassign_interface(interface='X2')
        X2_wiremode_dict['wire_paired_zone'] = 'LAN'
        X2_wiremode_dict['type'] = 'bypass'
        command = 'ifconfig eth1 ' + Parameter.PC1_ETH1_IP
        PC1_login.send_command(command)
        Assertion.assert_equal(res, True, "ERR: init match object and app rules failed")


# ping/http/ftp traffic passed between lan to custom zone
class TestEnhancements_TC27(Test):
    uuid = "SOSAIOT-TC-57526"
    description = show_testcase_info(TESTPLAN, 'enh27', description=True)['title']
    TCenh27_czname = 'tcenh27_custom_zone'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'enh27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_public_custom_zone(self):
        base_dict = {
            'name': self.TCenh27_czname,
            'security_type': 'public',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**trusted_dict)
        Assertion.assert_equal(output, True, "ERR: add customer zone failed")

    def test_02_config_x2_wiremode(self):
        X2_wiremode_dict['type'] = 'inspect'
        X2_wiremode_dict['wire_paired_zone'] = self.TCenh27_czname
        output = interfaceapi.config_interface(**X2_wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to inspect mode failed")

    def test_03_verify_ping_traffic(self):
        time.sleep(10)
        output = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 3)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_04_verify_http_traffic(self):
        output = http_send.Http_get()
        Assertion.assert_equal(output, True, "ERR: verify http traffic failed.")

    def test_05_verify_ftp_gav_pass(self):
        my_ftp.login()
        output = my_ftp.download_file(localgavfile, remotegavfile)
        logger.info(f'download gav file result: {output}')

        interfaceapi.unassign_interface(interface='X2')
        zonesapi.delete_zone_object(name=self.TCenh27_czname)
        Assertion.assert_equal(output, True, "ERR: the FW pass the Anti-Virus failed")


# ping/http/ftp traffic passed between PC1 and PC2 Server in Wiremode- secure mode
# ping can be blocked by app rule
class TestEnhancements_TC47(Test):
    uuid = "SOSAIOT-TC-57529"
    description = show_testcase_info(TESTPLAN, 'enh47', description=True)['title']
    TCenh47_czname = 'TCenh47_Trusted'
    TCenh47_march_obj = 'tcenh47_icmp'
    TCenh47_app_rules = 'tcenh47_icmp_block'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'enh47')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_trust_custom_zone(self):
        base_dict = {
            'name': self.TCenh47_czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**trusted_dict)
        Assertion.assert_equal(output, True, "ERR: add customer zone failed")

    def test_02_config_x2_and_pc2_ip(self):
        wiremode_dict = {
            'if': 'X2',
            'zone': self.TCenh47_czname,
            'mode': 'wire-mode',
            'type': 'secure',
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        output = interfaceapi.config_interface(**wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to secure mode failed")

    @repeat_method(3)
    def test_03_verify_ping_traffic(self):
        time.sleep(30)
        output = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 3)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_04_verify_http_traffic(self):
        output = http_send.Http_get()
        Assertion.assert_equal(output, True, "ERR: verify http traffic failed.")

    def test_05_verify_ftp_traffic(self):
        my_ftp.login()
        output = my_ftp.download_file(localfile, remotefile)
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')

    def test_06_add_match_object_for_icmp(self):
        logger.info('add match object and app rule...')
        match_opt_dict['name'] = self.TCenh47_march_obj
        res = matchobjapi.config_matchobject(**match_opt_dict)
        Assertion.assert_equal(res, True, "ERR:config icmp match object failed")

    def test_07_add_app_rule_for_icmp(self):
        apprule_dict['app_rules']['policy'][0]['match_object']['object'] = self.TCenh47_march_obj
        apprule_dict['app_rules']['policy'][0]['name'] = self.TCenh47_app_rules
        res = apprulesapi.add_apprule(**apprule_dict)
        Assertion.assert_equal(res, True, "ERR: add app rule for icmp block failed")

    # @repeat_method(5)
    # def test_08_verify_ping_traffic_and_log(self):
    #     fw_time = timeapi.show_time()
    #     time.sleep(20)
    #     output1 = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 3)
    #     logger.info(f'ping to pc2 eth0 result: {output1}')
    #     output3 = False if output1 else True
    #
    #     fw_logs = logapi.get_log(793)
    #     output2 = check_log_by_time(fw_time, fw_logs, log_id=793)
    #     logger.info(f'check log event result: {output2}')
    #     Assertion.assert_equal(output2 & output3, True, "ERR: verify ping traffic and app rule log failed")

    def test_10_init_objects_rules(self):
        res = apprulesapi.delete_apprule_object_byname(name=self.TCenh47_app_rules)
        res &= matchobjapi.del_match_object_by_name(name=self.TCenh47_march_obj)
        res &= interfaceapi.unassign_interface(interface='X2')
        res &= zonesapi.delete_zone_object(name=self.TCenh47_czname)
        Assertion.assert_equal(res, True, "ERR: init match object and app rules failed")


# ping/http/ftp traffic passed between PC1 and PC2 Server in Wiremode- secure mode
# ping can be blocked by app rule
class TestEnhancements_TC72(Test):
    uuid = "SOSAIOT-TC-57534"
    description = show_testcase_info(TESTPLAN, 'enh72', description=True)['title']
    TCenh72_Trusted = 'TCenh72_Trusted'
    TCenh72_Public = 'TCenh72_Public'
    TCenh72_march_obj = 'tcenh72_icmp'
    TCenh72_app_rules = 'tcenh72_icmp_block'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'enh72')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_custom_zones(self):
        base_dict = {
            'name': self.TCenh72_Trusted,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**trusted_dict)
        base_dict = {
            'name': self.TCenh72_Public,
            'security_type': 'public',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        output &= zonesapi.add_zone_object(**trusted_dict)
        Assertion.assert_equal(output, True, "ERR: add trusted and public zones failed")

    def test_02_config_x2_to_wan_secure(self):
        wiremode_dict = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'wire-mode',
            'type': 'secure',
            'wire_paired_interface': 'X3',
            'wire_paired_zone': self.TCenh72_Trusted,
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        output = interfaceapi.config_interface(**wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to secure mode failed")

    def test_03_change_x3_to_lan_inspect(self):
        wiremode_dict = {
            'if': 'X3',
            'zone': self.TCenh72_Public,
            'mode': 'wire-mode',
            'type': 'inspect',
            'wire_paired_interface': 'X2',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        output = interfaceapi.config_interface(**wiremode_dict)
        Assertion.assert_equal(output, True, "ERR: Config X3 to secure mode failed")

    @repeat_method(3)
    def test_04_verify_ping_traffic(self):
        time.sleep(30)
        output = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_05_verify_http_traffic(self):
        output = http_send.Http_get()
        Assertion.assert_equal(output, True, "ERR: verify http traffic failed.")

    def test_06_verify_ftp_traffic(self):
        my_ftp.login()
        output = my_ftp.download_file(localfile, remotefile)
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')

    def test_07_add_match_object_for_icmp(self):
        logger.info('add match object and app rule...')
        match_opt_dict['name'] = self.TCenh72_march_obj
        res = matchobjapi.config_matchobject(**match_opt_dict)
        Assertion.assert_equal(res, True, "ERR:config icmp match object failed")

    def test_08_add_app_rule_for_icmp(self):
        apprule_dict['app_rules']['policy'][0]['match_object']['object'] = self.TCenh72_march_obj
        apprule_dict['app_rules']['policy'][0]['name'] = self.TCenh72_app_rules
        res = apprulesapi.add_apprule(**apprule_dict)
        Assertion.assert_equal(res, True, "ERR: add app rule for icmp block failed")

    @repeat_method(3)
    def test_09_verify_ping_traffic_block(self):
        time.sleep(20)
        output = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 3)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_10_verify_ftp_gav_pass(self):
        my_ftp.login()
        output = my_ftp.download_file(localgavfile, remotegavfile)
        logger.info(f'download gav file result: {output}')
        Assertion.assert_equal(output, True, "ERR: the FW pass the Anti-Virus failed")

    def test_11_init_objects_rules(self):
        res = apprulesapi.delete_apprule_object_byname(name=self.TCenh72_app_rules)
        res &= matchobjapi.del_match_object_by_name(name=self.TCenh72_march_obj)
        res &= interfaceapi.unassign_interface(interface='X2')
        res &= zonesapi.delete_zone_object(name=self.TCenh72_Trusted)
        res &= zonesapi.delete_zone_object(name=self.TCenh72_Public)
        Assertion.assert_equal(res, True, "ERR: init match object and app rules failed")

# openstack do no support tab mode
# ping/http/ftp traffic passed between PC1 and PC2 Server in Wiremode- tap mode
# class Test_TC25(Test):
#     uuid = '1511454'
#     description = show_testcase_info(TESTPLAN, '25', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '25')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_config_x2_to_tap_mode(self):
#         output = interfaceapi.config_interface(**x2_tapmode_dict)
#         Assertion.assert_equal(output, True, "ERR: Config X2 to secure mode failed")
#
#     def test_02_config_x2_to_lan_mode(self):
#         x3_lan_dict = {
#             'if': 'x3',
#             'zone': 'lan',
#             'mode': 'static',
#             'ip': Parameter.X2_IP,
#             'mgmt_https': True,
#             'mgmt_ssh': True,
#             'mgmt_ping': True,
#         }
#         output = interfaceapi.config_interface(**x3_lan_dict)
#         Assertion.assert_equal(output, True, "ERR: Config X2 to secure mode failed")
#
#     def test_03_verify_ping_traffic(self):
#         time.sleep(5)
#         output = PC1_login.ping_from_eth(Parameter.PC2_ETH0_NewIP, 'eth1', 5)
#
#         interfaceapi.unassign_interface(interface='X2')
#         interfaceapi.unassign_interface(interface='X3')
#         Assertion.assert_equal(output, False, "ERR: verify ping traffic failed")

# def test_03_verify_http_traffic(self):
#     output = http_send.Http_get()
#     Assertion.assert_equal(output, True, "ERR: verify http traffic failed.")
#
# def test_04_verify_ftp_traffic(self):
#     my_ftp.login()
#     output = my_ftp.download_file(localfile, remotefile)
#     Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')
