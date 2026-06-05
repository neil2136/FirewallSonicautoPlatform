from asyncio.log import logger
from definition.settings import *
import re


class TestDNS_Filtering_Log_04(Test):
    uuid = "SOSAIOT-TC-51529"
    description= show_testcase_info(Parameter.TESTPLAN, '004', description=True)['title']
    goto_teardown = True
    jira = 'Gen7-44568'

    def test_000_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '004')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_001_create_dns_rule(self):
        add_rule = {
            "dns_policies": [
                {
                    "name": "New_dns_rule",
                    "priority": {
                        "manual": 1
                    },
                    "enable": True,
                    "source": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "name": "DNS (Name Service) UDP"
                    },
                    "from": "X0",
                    "action": {
                        "filter_profile": "Default Profile"
                    }
                }
            ]
        }
        rc = dnsrule_obj.add_dns_rule(**add_rule)
        Assertion.assert_equal(rc, True, "ERR: Create_dns_rule failed")

    def test_01_do_dig_verify_logs_related_to_check_DNS_Packet_Allowed(self):
        flag_log = False
        logger.info('Clear logs...')
        log_monitor.clear_log()
        logger.info('Dig www.ea.com to verify dns Response')
        diag_command = 'dig www.ea.com @'+ Parameter.FIREWALL
        for i in range(3):
            rc = os.popen(diag_command).read()
        logger.info(rc)
        time.sleep(5)
        logger.info('Export logs')
        rc = log_monitor.export_log_txt(log_switch=False)
        logger.info(rc)
        start = "DNS Security"
        end ='DNS Packet Allowed'
        match1 = re.search(r'' + start + '(.*?)' + end + '', rc, re.I|re.S)
        if match1:
            output1 = match1.group(0)
            logger.info(output1)
            match2 = re.search('www.ea.com', output1, re.I|re.S)
            if match2:
                flag_log = True
            else:
                logger.error('No related logs.')
        else:
            logger.error('Related logs were not included.')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")
        
    def test_02_check_DNS_Query_Received(self):
        logger.info('Export logs')
        rc = log_monitor.export_log_txt(log_switch=False)
        logger.info(rc)
        start = "DNS Security"
        end ='www.ea.com'
        match1 = re.search(r'' + start + '(.*?)' + end + '', rc, re.I|re.S)
        if match1:
            output1 = match1.group(0)
            logger.info(output1)
            match2 = re.search('DNS Filtering - DNS Query Received', output1, re.I|re.S)
            if match2:
                flag_log = True
            else:
                logger.error('No related logs.')
        else:
            logger.error('Related logs were not included.')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    def test_03_edit_dns_filtering_profile(self):
        edit_file = {  
            "dns_security": {
                "dns_filtering": {
                    "profile": [
                        {
                            "name": "Default Profile",
                            "actions": "{\"1\":1,\"2\":1,\"3\":1,\"4\":1,\"5\":1}"

                        }
                    ]
                }
            }
        }
        rc = dns_filtering_obj.config_dns_filtering_profile(**edit_file)
        Assertion.assert_equal(rc, True, "ERR: Edit_dns_filtering_profile failed")      

    def test_04_do_dig_verify_logs_related_to_check_DNS_Packet_block(self):
        flag_log = False
        logger.info('Clear logs...')
        log_monitor.clear_log()
        logger.info('Dig www.ea.com to verify dns Response')
        diag_command = 'dig www.ea.com @'+ Parameter.FIREWALL
        for i in range(3):
            rc = os.popen(diag_command).read()
        logger.info(rc)
        time.sleep(5)
        logger.info('Export logs')
        rc = log_monitor.export_log_txt(log_switch=False)
        logger.info(rc)
        start = "DNS Security"
        end ='DNS Packet Blocked'
        match1 = re.search(r'' + start + '(.*?)' + end + '', rc, re.I|re.S)
        if match1:
            output1 = match1.group(0)
            logger.info(output1)
            match2 = re.search('www.ea.com', output1, re.I|re.S)
            if match2:
                flag_log = True
            else:
                logger.error('No related logs.')
        else:
            logger.error('Related logs were not included.')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")
        
    def test_05_check_DNS_Query_Received_after_Game_block(self):
        logger.info('Export logs')
        rc = log_monitor.export_log_txt(log_switch=False)
        logger.info(rc)
        start = "DNS Filtering - DNS Query ReceivedStandard Message String"
        end ='DNS Filtering - DNS Query Received'
        match1 = re.search(r'' + start + '(.*?)' + end + '', rc, re.I|re.S)
        if match1:
            output1 = match1.group(0)
            logger.info(output1)
            match2 = re.search('www.ea.com', output1, re.I|re.S)
            if match2:
                flag_log = True
            else:
                logger.error('No related logs.')
        else:
            logger.error('Related logs were not included.')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")


class TestDNS_Filtering_Config_File_014(Test):
    uuid = "SOSAIOT-TC-51507"
    description= show_testcase_info(Parameter.TESTPLAN, '014', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '014')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dns_filtering_profile(self):
        edit_file = {  
            "dns_security": {
                "dns_filtering": {
                    "profile": [
                        {
                            "name": "Test"
                        }
                    ]
                }
            }
        }
        rc = dns_filtering_obj.add_dns_filtering_profile(**edit_file)
        Assertion.assert_equal(rc, True, "ERR: Add_dns_filtering_profile failed")

    def test_02_edit_some_categories_to_blcok(self):
        edit_file = {  
            "dns_security": {
                "dns_filtering": {
                    "profile": [
                        {
                            "name": "Test",
                            "actions": "{\"1\":1,\"2\":1,\"3\":1,\"4\":1,\"5\":1}"

                        }
                    ]
                }
            }
        }
        rc = dns_filtering_obj.config_dns_filtering_profile(**edit_file)
        Assertion.assert_equal(rc, True, "ERR: Edit_dns_filtering_profile failed") 

    def test_023_vefiry_dns_profiles_in_tsr(self):
        flag = False
        tsr_content = down_tsr_obj.get_tsr_part('Network', lab1='DNS Security')
        logger.info(tsr_content)
        match1 = re.search('DNS Filtering Profile Default Profile', tsr_content, re.I|re.S)
        if match1:
            logger.info(match1)
            logger.error('DNS Filtering Profile Default Profile is in TSR')
            match2 = re.search('DNS Filtering Profile Test', tsr_content, re.I|re.S)
            if match2:
                logger.info(match2)
                logger.error('DNS Filtering Profile Test is in TSR')
                flag = True
            else:
                logger.error('DNS Filtering Profiles are not in TSR')
        else:
            logger.info("Not found the target tsr content part")
        Assertion.assert_equal(flag, True, "ERR: Verify DNS Filtering Profiles in tsr failed") 


class TestDNS_Filtering_Config_File_015(Test):
    uuid = "SOSAIOT-TC-51440"
    description= show_testcase_info(Parameter.TESTPLAN, '015', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '015')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_profile_use_CLI(self):
        cmds = [
            'con',
            'dns-security',
            'dns-filtering',
            'profile test',
            'commit',
            'exit',
            'profile test1',
            'commit',
            'exit',
            'profile test2',
            'commit',
            'end',
            'exit',
        ]
        rc = fw_cli.do_cli_commands(cmds, tag=1)
        logger.info(rc)
        Assertion.assert_regular(str(rc), 'Changes made', "ERR: Add_profile_use_CLI failed.")


class TestDNS_Filtering_Config_File_016(Test):
    uuid = "SOSAIOT-TC-51441"
    description= show_testcase_info(Parameter.TESTPLAN, '016', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '016')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_profile_use_CLI(self):
        cmds = [
            'con',
            'dns-security',
            'dns-filtering',
            'profile test1',
            'name testEdit',
            'category 1.\ Adult forge-ip-reply',
            'commit',
            'end',
            'exit'
        ]
        rc = fw_cli.do_cli_commands(cmds, tag=1)
        logger.info(rc)
        Assertion.assert_regular(str(rc), 'Changes made', "ERR: Edit_profile_use_CLI failed.")


class TestDNS_Filtering_Config_File_019(Test):
    uuid = "SOSAIOT-TC-51444"
    description= show_testcase_info(Parameter.TESTPLAN, '019', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '019')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_dns_policy_bound_to_profile_test(self):
        add_rule = {
            "dns_policies": [
                {
                    "name": "Test",
                    "priority": {
                        "manual": 1
                    },
                    "enable": True,
                    "source": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "name": "DNS (Name Service) UDP"
                    },
                    "from": "X0",
                    "action": {
                        "filter_profile": "test"
                    }
                }
            ]
        }
        rc = dnsrule_obj.add_dns_rule(**add_rule)
        Assertion.assert_equal(rc, True, "ERR: Create_dns_rule failed")
    
    def test_02_del_profile_test_use_CLI(self):
        cmds = [
            'con',
            'dns-security',
            'dns-filtering',
            'no profile test',
            'commit',
            'end',
            'exit',
            'no'
        ]
        rc = fw_cli.do_cli_commands(cmds, tag=1)
        match = re.search(r'The target DNS Filtering Object test is in used by a DNS policy', str(rc).replace('\\n' ,'').replace('\\r' ,''), re.I|re.S)
        if match:
            logger.info('Del_profile_use_CLI succeed.')
        else:
            Assertion.fail('Del_profile_use_CLI failed.')


class TestDNS_Filtering_Config_File_018(Test):
    uuid = "SOSAIOT-TC-51443"
    description= show_testcase_info(Parameter.TESTPLAN, '018', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '018')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_del_profile_use_CLI(self):
        cmds = [
            'con',
            'dns-security',
            'dns-filtering',
            'no profile test2',
            'commit',
            'end',
            'exit'
        ]
        rc = fw_cli.do_cli_commands(cmds, tag=1)
        logger.info(rc)
        match = re.search(r'Changes made', str(rc).replace('\\n' ,'').replace('\\r' ,''), re.I|re.S)
        if match:
            logger.info('Del_profile_use_CLI succeed.')
        else:
            Assertion.fail('Del_profile_use_CLI failed.')


class TestDNS_Filtering_Config_File_021(Test):
    uuid = "SOSAIOT-TC-51446"
    description= show_testcase_info(Parameter.TESTPLAN, '021', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '021')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_02_del_all_profiles_use_CLI(self):
        logger.info('Del dns policy')
        dnsrule_obj.del_dns_rule_by_name('Test')
        cmds = [
            'con',
            'dns-security',
            'dns-filtering',
            'no profiles',
            'commit',
            'end',
            'exit'
        ]
        rc = fw_cli.do_cli_commands(cmds, tag=1)
        logger.info(rc)
        Assertion.assert_regular(str(rc), 'Changes made', "ERR: Del_all_profiles_use_CLI failed.")




