from definition.settings import *


# Check FQDN objects show in drop-down list of Original Source in IPv4/IPv6
class TestUI_TC01(Test):
    uuid = "SOSAIOT-TC-56026"
    description = show_testcase_info(TESTPLAN, 'UI_TC01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'UI_TC01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_goto_add_net_policy_page_via_UI(self):
        # clean firefox process
        PC1_login.send_command('pkill firefox')
        output = FWPage_login.login_fw_ui()
        logger.info(f'login fw result is {output}')
        if output:
            logger.info('start go to nat rules page...')
            res = FWPage_login.navigate_to_nat_rules_page()
            logger.info(f'start go to nat rules page: {res}')
            logger.info('click Add net button...')
            res = FWPage_login.click_the_add_net_button()
            logger.info(f'click add net button: {res}')
            output_v4 = FWPage_login.click_original_translated_option()
            logger.info(f'click original source option: {output_v4}')
            CaseParams.ui_test_v4 = output_v4
            output_v6 = FWPage_login.click_original_translated_option_v6()
            logger.info(f'click original source option in ipv6: {output_v6}')
            CaseParams.ui_test_v6 = output_v6
            output = True if output_v4 and output_v6 else False
        else:
            logger.info('login fw via UI failed.')
            output = False
        Assertion.assert_equal(output, True, "ERR: goto add net policy page failed")

    def test_02_check_fqdn_in_original_source_option(self):
        if CaseParams.ui_test_v4 and CaseParams.ui_test_v6:
            logger.info(
                f'ui test v4: {CaseParams.ui_test_v4["tc1_res"]}, ui test v6: {CaseParams.ui_test_v6["tc1v6_res"]}')
            res = CaseParams.ui_test_v4['tc1_res'] & CaseParams.ui_test_v6['tc1v6_res']
        else:
            res = False
            logger.info('check fqdn in ui failed.')
        Assertion.assert_equal(res, True, "ERR: check fqdn in original source option failed")


# Check FQDN objects show in drop-down list of Original Destination in IPv4/IPv6
class TestUI_TC02(Test):
    uuid = "SOSAIOT-TC-56027"
    description = show_testcase_info(TESTPLAN, 'UI_TC02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'UI_TC02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_fqdn_in_original_destination_option(self):
        if CaseParams.ui_test_v4 and CaseParams.ui_test_v6:
            logger.info(
                f'ui test v4: {CaseParams.ui_test_v4["tc2_res"]}, ui test v6: {CaseParams.ui_test_v6["tc2v6_res"]}')
            res = CaseParams.ui_test_v4['tc2_res'] & CaseParams.ui_test_v6['tc2v6_res']
        else:
            res = False
            logger.info('check fqdn in ui failed.')
        Assertion.assert_equal(res, True, "ERR: check fqdn in original Destination option failed")


# Check FQDN objects not show in drop-down list of translated source in IPv4/IPv6
class TestUI_TC03(Test):
    uuid = "SOSAIOT-TC-56028"
    description = show_testcase_info(TESTPLAN, 'UI_TC03', description=True)['title']
    jira='GEN7-47274'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'UI_TC03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_fqdn_in_translated_source_option(self):
        if CaseParams.ui_test_v4 and CaseParams.ui_test_v6:
            logger.info(
                f'ui test v4: {CaseParams.ui_test_v4["tc3_res"]}, ui test v6: {CaseParams.ui_test_v6["tc3v6_res"]}')
            res = CaseParams.ui_test_v4['tc3_res'] & CaseParams.ui_test_v6['tc3v6_res']
        else:
            res = True
            logger.info('check fqdn in ui failed.')
        Assertion.assert_equal(res, False, "ERR: check fqdn not in translated source option failed")


# Check FQDN objects not show in drop-down list of Translated destination in IPv4/IPv6
class TestUI_TC04(Test):
    uuid = "SOSAIOT-TC-56029"
    description = show_testcase_info(TESTPLAN, 'UI_TC04', description=True)['title']
    jira='GEN7-47274'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'UI_TC04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_fqdn_in_translated_destinationoption(self):
        if CaseParams.ui_test_v4 and CaseParams.ui_test_v6:
            logger.info(
                f'ui test v4: {CaseParams.ui_test_v4["tc4_res"]}, ui test v6: {CaseParams.ui_test_v6["tc4v6_res"]}')
            res = CaseParams.ui_test_v4['tc4_res'] & CaseParams.ui_test_v6['tc4v6_res']
        else:
            res = True
            logger.info('check fqdn in ui failed.')
        Assertion.assert_equal(res, False, "ERR: check fqdn not in translated destination option failed")


# Check anther FQDN object show in drop-down list of Original Source/Destination in IPv4/IPv6
class TestUI_TC11(Test):
    uuid = "SOSAIOT-TC-56030"
    description = show_testcase_info(TESTPLAN, 'UI_TC11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'UI_TC11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_fqdn_in_original_source_destination_option(self):
        if CaseParams.ui_test_v4 and CaseParams.ui_test_v6:
            logger.info(
                f'ui test v4: {CaseParams.ui_test_v4["tc11_res"]}, ui test v6: {CaseParams.ui_test_v6["tc11v6_res"]}')
            res = CaseParams.ui_test_v4['tc11_res'] & CaseParams.ui_test_v6['tc11v6_res']
        else:
            res = False
            logger.info('check fqdn in ui failed.')
        Assertion.assert_equal(res, True, "ERR: check fqdn in original source/destination option failed")


class TestNegtive_TC12(Test):
    uuid = "SOSAIOT-TC-56031"
    description = show_testcase_info(TESTPLAN, 'Negtive_TC12', description=True)['title']
    TC12_nat_name = 'auto_nat_test_3'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Negtive_TC12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ao_group(self):
        aogroup_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "fqdn": [
                                {"name": "A.dns.baidu.com"}
                            ],
                            "ipv4": [
                                {"name": PC4_ETH1_IP}
                            ]
                        },
                        "name": CaseParams.fqdn_group1
                    }
                }
            ]
        }
        (aogres, aogmsg) = aogroupapi.add_addressgroup(msg=True, **aogroup_dict)
        if not aogres:
            aogres = True if 'already exists' in str(aogmsg) else False
        Assertion.assert_equal(aogres, True, 'ERR: add ao group failed')

    def test_02_add_fqdn_nat_policy(self):
        output, msg = natpolicyapi.add_nat_policy(msg=True, **negtive_nat_dict)
        if output is False:
            output = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(output, True, "ERR:add nat policy failed")

    def test_03_del_fqdn_in_ao_group(self):
        output, msg = aogroupapi.del_addressgroup(CaseParams.fqdn_group1, version='v6', msg=True)
        error_msg = 'Object is in use by a NAT Policy'
        Assertion.assert_regular(str(msg), error_msg, "ERR: check error msg failed")


class TestTSR_TC34(Test):
    uuid = "SOSAIOT-TC-56044"
    description = show_testcase_info(TESTPLAN, 'TSR_TC34', description=True)['title']
    nat_name_1 = tsr_nat_dict['nat_policies'][0]['ipv4']['name']
    nat_name_2 = 'auto_nat_test_2'
    nat_name_3 = 'auto_nat_test_3'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TSR_TC34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_fqdn_nat_policy1(self):
        output, msg = natpolicyapi.add_nat_policy(msg=True, **tsr_nat_dict)
        if output is False:
            output = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(output, True, "ERR:add nat policy failed")

    def test_02_add_fqdn_nat_policy2(self):
        nat_json = {
            'name': self.nat_name_2,
            "translated_source": {
                "name": CaseParams.in_wan_range1
            }
        }
        tsr_nat_dict['nat_policies'][0]['ipv4'].update(nat_json)
        output, msg = natpolicyapi.add_nat_policy(msg=True, **tsr_nat_dict)
        if output is False:
            output = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(output, True, "ERR:add nat policy failed")

    def test_03_check_nat_infos_in_tsr(self):
        logger.info('waiting for 10s to make sure nat policies added.')
        time.sleep(10)
        res = []
        nat1_info = [self.nat_name_1, 'X1 IP', CaseParams.domain_dns_baidu]
        nat2_info = [self.nat_name_2, '12.12.1.30-40', CaseParams.domain_dns_baidu]
        nat3_info = [self.nat_name_3, CaseParams.fqdn_group1, 'X1']
        getcontents = tsrfromlanapi.get_tsr_part2('Network : NAT Policies')
        logger.info(f'get x2 info in tsr: \n{getcontents}')
        if getcontents:
            for checkinfo in [nat1_info, nat2_info, nat3_info]:
                for natinfo in getcontents.split('UUID'):
                    checkres = [x in natinfo for x in checkinfo]
                    logger.info(f'check nat info result: {checkres}')
                    if all(checkres):
                        res += checkres
                        break
                else:
                    logger.info(f'can not find nat info: {checkinfo}')
                    res += [False, False, False]
        logger.info(f'check nat policies reslut: {res}')
        # make sure res is exist valid value
        if res:
            res = all(res)
        Assertion.assert_equal(res, True, "ERR: check cfs policy settings failed")


class TestCLI_TC37(Test):
    uuid = "SOSAIOT-TC-56047"
    description = show_testcase_info(TESTPLAN, 'CLI_TC37', description=True)['title']
    add_cli_nat_name = 'auto_cli_nat_1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'CLI_TC37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_fqdn_nat_policy_via_cli(self):
        add_nat = {
            'version': 'ipv4',
            'name': self.add_cli_nat_name,
            'comment': 'auto_add_nat',
            'orig_source_type': 'any',
            'trans_source_type': 'name',
            'trans_source': PC4_ETH1_IP,
            'orig_dest_type': 'fqdn',
            'orig_dest': CaseParams.domain_pc3_baidu,
            'trans_dest_type': 'original',
        }
        output = natpolicycli.add_natpolicy(**add_nat)
        Assertion.assert_equal(output, True, "ERR: add fqdn nat policy via cli failed")

    def test_02_check_fqdn_nat_policy_via_cli(self):
        show_nat = {
            'version': 'ipv4',
            'entries': 'all',
            'type': 'custom',
        }
        output = natpolicycli.show_natpolicy(**show_nat)
        Assertion.assert_regular(output, self.add_cli_nat_name, "ERR:check fqdn nat policy via cli failed")


class TestCLI_TC39(Test):
    uuid = "SOSAIOT-TC-56049"
    description = show_testcase_info(TESTPLAN, 'CLI_TC39', description=True)['title']
    add_cli_nat_name = 'auto_cli_nat_1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'CLI_TC39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_fqdn_nat_policy_via_cli(self):
        output = natpolicycli.del_natpolicy(f'ipv4:name:{self.add_cli_nat_name}')
        Assertion.assert_equal(output, True, "ERR: del fqdn nat policy via cli failed")


class TestLog_TC40(Test):
    uuid = "SOSAIOT-TC-56050"
    description = show_testcase_info(TESTPLAN, 'Log_TC40', description=True)['title']
    nat_name = 'auto_nat_test_3'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Log_TC40')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_nat_policy_lo_and_clear_log(self):
        log_settings = {
            "log": {
                "group": [
                    {
                        "id": 94,
                        "name": "NAT Policy",
                        "priority_level": "inform",
                        "log_email": {},
                        "log_monitor": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "email_alert": {},
                        "syslog": {},
                        "trap": {},
                        "ipfix": {
                            "type": "enabled",
                            "redundancy_interval": {
                                "value": 60
                            }
                        },
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {},
                        "color": {
                            "hex": "0x00000000"
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        output = logcategoryapi.edit_log_category_groups_by_id(id=94, **log_settings)
        clearlog = logmonitorapi.clear_log()
        time.sleep(5)
        logger.info(f'clear log result: {clearlog}')
        Assertion.assert_equal(output, True, "ERR: del fqdn nat policy failed")

    def test_02_del_fqdn_nat_policy(self):
        output = natpolicyapi.del_nat_policy_by_name(name=self.nat_name)
        Assertion.assert_equal(output, True, "ERR: del fqdn nat policy failed")

    def test_03_check_del_nat_log(self):
        fw_logs = logmonitorapi.get_log(1315)
        msg = 'NAT policy deleted'
        Assertion.assert_regular(str(fw_logs), msg, "ERR: check del nat log failed.")

    def test_04_add_fqdn_nat_policy(self):
        output, msg = natpolicyapi.add_nat_policy(msg=True, **negtive_nat_dict)
        if output is False:
            output = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(output, True, "ERR:add nat policy failed")

    def test_05_check_add_nat_log(self):
        logger.info('waiting for 5s to make sure configure invalid...')
        time.sleep(5)
        fw_logs = logmonitorapi.get_log(1313)
        msg = 'NAT policy added'
        Assertion.assert_regular(str(fw_logs), msg, "ERR: check add nat log failed.")

    def test_06_modify_fqdn_nat_policy(self):
        nat_json = {
            "inbound": "any",
            "outbound": "X1",
        }
        negtive_nat_dict['nat_policies'][0]['ipv4'].update(nat_json)
        output = natpolicyapi.edit_nat_policy_by_name(name=self.nat_name, **negtive_nat_dict)
        Assertion.assert_equal(output, True, "ERR: modify fqdn nat policy failed")

    def test_07_check_add_nat_log(self):
        logger.info('waiting for 5s to make sure configure invalid...')
        time.sleep(5)
        fw_logs = logmonitorapi.get_log(1314)
        msg = 'NAT policy modified'
        Assertion.assert_regular(str(fw_logs), msg, "ERR: check add nat log failed.")
