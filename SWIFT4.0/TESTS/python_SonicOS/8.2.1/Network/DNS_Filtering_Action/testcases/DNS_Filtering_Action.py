from definition.settings import *
from testcases import check_action


class TestCheck_dns_server_1(Test):
    uuid = 'NonTC'
    description= 'TestCheck_dns_server_1'
    goto_teardown = True

    @repeat_method(10)
    def test_01_check_dns_server(self):
        dns_server = '156.154.54.200'
        cmd = 'ping {} -c 5' .format(dns_server)
        rc = os.popen(cmd).read()
        out = os.popen('traceroute 156.154.54.200').read()
        logger.info(out)
        if '100% packet loss' not in rc:
            logger.info('Can access to dns server')
        else:
            Assertion.fail('Cannot access to dns server')


class TestDNS_Filtering_Action_001(Test):
    uuid = "SOSAIOT-TC-51423"
    description= show_testcase_info(Parameter.TESTPLAN, '001', description=True)['title']
    goto_teardown = True
    jira = 'Gen7-44568'

    def test_000_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '001')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_001_create_dns_rule(self):
        add_rule = {
            "dns_policies": [
                {
                    "name": "New_rule",
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

    def test_01_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    @repeat_method(10)
    def test_02_do_dig_baidu_to_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('www.baidu.com')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig_baidu failed")
        
    @repeat_method(10)
    def test_03_check_DNS_reply_from_Neustar(self):
        foundit = check_action.check_DNS_reply_from_Neustar()
        Assertion.assert_equal(foundit, 1, "ERR:failed to find expected packets")

    def test_04_check_related_logs(self):
        flag_log = check_action.check_related_logs('www.baidu.com')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")



class TestDNS_Filtering_Action_002(Test):
    uuid = "SOSAIOT-TC-51424"
    description= show_testcase_info(Parameter.TESTPLAN, '002', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '002')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_new_dns_profile(self):
        rc = dns_filtering_obj.add_dns_filtering_profile(**add_file)
        Assertion.assert_equal(rc, True, "ERR: Add_dns_filtering_profile failed")

    def test_02_add_dns_rule(self):
        rc = dnsrule_obj.add_dns_rule(**add_rule)
        Assertion.assert_equal(rc, True, "ERR: Create_dns_rule failed")

    ##################### Check adultswim.com ##############
    def test_03_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    @repeat_method(10)
    def test_04_do_dig_adultswim_to_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('adultswim.com')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig_adultswim failed")
        
    @repeat_method(10)
    def test_05_check_DNS_reply_from_Neustar(self):
        foundit = check_action.check_DNS_reply_from_Neustar()
        Assertion.assert_equal(foundit, 1, "ERR:failed to find expected packets")

    def test_06_check_related_logs(self):
        flag_log = check_action.check_related_logs('adultswim.com')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")
    
    ##################### Check www.ea.com ##############
    def test_07_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    @repeat_method(10)
    def test_08_do_dig_ea_to_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('www.ea.com')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig_www.ea failed")
        
    @repeat_method(10)
    def test_09_check_DNS_reply_from_Neustar(self):
        foundit = check_action.check_DNS_reply_from_Neustar()
        Assertion.assert_equal(foundit, 1, "ERR:failed to find expected packets")

    def test_10_check_related_logs(self):
        flag_log = check_action.check_related_logs('www.ea.com')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ################## Check www.gamblingsites.org ##############
    
    def test_11_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    @repeat_method(10)
    def test_12_do_dig_gamblingsites_to_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('www.gamblingsites.org')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig www.gamblingsites.org failed")
    
    @repeat_method(30)
    def test_13_check_DNS_reply_from_Neustar(self):
        foundit = check_action.check_DNS_reply_from_Neustar()
        Assertion.assert_equal(foundit, 1, "ERR:failed to find expected packets")

    def test_14_check_related_logs(self):
        flag_log = check_action.check_related_logs('www.gamblingsites.org')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ##################### Check www.hjaoopoa.top ##############
    def test_15_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    def test_16_do_dig_hjaoopoa_to_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('www.hjaoopoa.top')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig www.hjaoopoa.top failed")

    @repeat_method(10)  
    def test_17_check_DNS_reply_from_Neustar(self):
        foundit = check_action.check_DNS_reply_from_Neustar()
        Assertion.assert_equal(foundit, 1, "ERR:failed to find expected packets")

    def test_18_check_related_logs(self):
        flag_log = check_action.check_related_logs('www.hjaoopoa.top')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")



class TestDNS_Filtering_Action_003(Test):
    uuid = "SOSAIOT-TC-51425"
    description= show_testcase_info(Parameter.TESTPLAN, '003', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '003')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_new_dns_profile(self):
        rc = dns_filtering_obj.add_dns_filtering_profile(**add_file_003)
        Assertion.assert_equal(rc, True, "ERR: Add_dns_filtering_profile failed")

    def test_02_add_dns_rule(self):
        rc = dnsrule_obj.add_dns_rule(**add_rule_003)
        Assertion.assert_equal(rc, True, "ERR: Create_dns_rule failed")

    ##################### Check shibaswap.com ##############
    @repeat_method(10)
    def test_03_do_dig_iomovies_verify_DNS_query(self):
        rc = check_action.do_dig_verify_DNS_query_block('shibaswap.com')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = True if (out1 in rc or out2 in rc) else False 
        Assertion.assert_equal(output, True, "ERR: Dig shibaswap.com successfully.")

    def test_04_check_related_logs(self):
        flag_log = check_action.check_related_logs_block('shibaswap.com')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ##################### Check myfreecams.com ##############
    @repeat_method(10)
    def test_05_do_dig_iomovies_verify_DNS_query(self):
        rc = check_action.do_dig_verify_DNS_query_block('myfreecams.com')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = True if (out1 in rc or out2 in rc) else False 
        Assertion.assert_equal(output, True, "ERR: Dig myfreecams.com successfully.")

    def test_06_check_related_logs(self):
        flag_log = check_action.check_related_logs_block('myfreecams.com')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ##################### Check sitenable.ch ##############
    @repeat_method(10)
    def test_07_do_dig_iomovies_verify_DNS_query(self):
        rc = check_action.do_dig_verify_DNS_query_block('sitenable.ch')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = True if (out1 in rc or out2 in rc) else False 
        Assertion.assert_equal(output, True, "ERR: Dig sitenable.ch successfully.")

    def test_08_check_related_logs(self):
        flag_log = check_action.check_related_logs_block('sitenable.ch')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ##################### Check loveread.me ##############
    @repeat_method(10)
    def test_09_do_dig_iomovies_verify_DNS_query(self):
        rc = check_action.do_dig_verify_DNS_query_block('loveread.me')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = True if (out1 in rc or out2 in rc) else False 
        Assertion.assert_equal(output, True, "ERR: Dig loveread.me successfully.")

    def test_10_check_related_logs(self):
        flag_log = check_action.check_related_logs_block('loveread.me')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ##################### Check ultradnsfirewall-bots.neustar ##############
    @repeat_method(10)
    def test_11_do_dig_iomovies_verify_DNS_query(self):
        rc = check_action.do_dig_verify_DNS_query_block('ultradnsfirewall-bots.neustar')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = True if (out1 in rc or out2 in rc) else False 
        Assertion.assert_equal(output, True, "ERR: Dig ultradnsfirewall-bots.neustar successfully.")

    def test_12_check_related_logs(self):
        flag_log = check_action.check_related_logs_block('ultradnsfirewall-bots.neustar')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")



class TestDNS_Filtering_Action_004(Test):
    uuid = "SOSAIOT-TC-51426"
    description= show_testcase_info(Parameter.TESTPLAN, '004', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '001')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_new_dns_profile(self):
        rc = dns_filtering_obj.add_dns_filtering_profile(**add_file_004)
        Assertion.assert_equal(rc, True, "ERR: Add_dns_filtering_profile failed")

    def test_02_add_dns_rule(self):
        rc = dnsrule_obj.add_dns_rule(**add_rule_004)
        Assertion.assert_equal(rc, True, "ERR: Create_dns_rule failed") 

    #################### Check crackswall.com ##############
    def test_03_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    @repeat_method(10)
    def test_04_do_dig_iomovies_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('crackswall.com')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig crackswall.com successfully.")

    def test_05_check_DNS_reply_flag(self):
        rc = check_action.check_DNS_reply_flag()
        Assertion.assert_equal(rc, True, "ERR: Check the flag in DNS Reply failed.")

    def test_06_check_related_logs(self):
        flag_log = check_action.check_related_logs_reply('crackswall.com')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ##################### Check ultradnsfirewall-parked-domains.neustar ##############
    def test_07_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    def test_08_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")
    
    @repeat_method(10)
    def test_09_do_dig_iomovies_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('ultradnsfirewall-parked-domains.neustar')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig ultradnsfirewall-parked-domains.neustar successfully.")
    
    @repeat_method(3)
    def test_10_check_DNS_reply_flag(self):
        rc = check_action.check_DNS_reply_flag()
        Assertion.assert_equal(rc, True, "ERR: Check the flag in DNS Reply failed.")

    def test_11_check_related_logs(self):
        flag_log = check_action.check_related_logs_reply('ultradnsfirewall-parked-domains.neustar')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ##################### Check Bleacherreport.com ##############
    def test_12_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    @repeat_method(10)
    def test_13_do_dig_iomovies_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('bleacherreport.com')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig Bleacherreport.com successfully.")

    def test_14_check_DNS_reply_flag(self):
        rc = check_action.check_DNS_reply_flag()
        Assertion.assert_equal(rc, True, "ERR: Check the flag in DNS Reply failed.")

    def test_15_check_related_logs(self):
        flag_log = check_action.check_related_logs_reply('bleacherreport.com')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ##################### Check myegy.tv ##############
    def test_16_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    @repeat_method(10)
    def test_17_do_dig_iomovies_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('myegy.tv')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig myegy.tv successfully.")

    def test_18_check_DNS_reply_flag(self):
        rc = check_action.check_DNS_reply_flag()
        Assertion.assert_equal(rc, True, "ERR: Check the flag in DNS Reply failed.")

    def test_19_check_related_logs(self):
        flag_log = check_action.check_related_logs_reply('myegy.tv')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")

    ##################### Check grabagun.com ##############
    def test_20_config_packet_monitor(self):
        logger.info('Config packect monitor')
        out = check_action.config_packet_monitor()
        Assertion.assert_equal(out, 3, "ERR: Config packet monitor failed")

    @repeat_method(10)
    def test_21_do_dig_iomovies_verify_DNS_query(self):
        packet_obj.start_capture()
        time.sleep(3)
        rc = check_action.do_dig_verify_DNS_query('grabagun.com')
        out1 = 'no servers could be reached'
        out2 = 'connection timed out'
        output = False if (out1 in rc or out2 in rc) else True 
        Assertion.assert_equal(output, True, "ERR: Dig grabagun.com successfully.")
    
    def test_22_check_DNS_reply_flag(self):
        rc = check_action.check_DNS_reply_flag()
        Assertion.assert_equal(rc, True, "ERR: Check the flag in DNS Reply failed.")

    def test_23_check_related_logs(self):
        flag_log = check_action.check_related_logs_reply('grabagun.com')
        Assertion.assert_equal(flag_log, True, "ERR: Check related logs failed")    



class TestDNS_Filtering_Action_005(Test):
    uuid = "SOSAIOT-TC-51427"
    description= show_testcase_info(Parameter.TESTPLAN, '005', description=True)['title']

    def test_01_create_new_dns_profile(self):
        
        rc = dns_filtering_obj.add_dns_filtering_profile(**add_file_005)
        Assertion.assert_equal(rc, True, "ERR: Add_dns_filtering_profile failed")

    def test_02_add_dns_rule(self):
        rc = dnsrule_obj.add_dns_rule(**add_rule_005)
        Assertion.assert_equal(rc, True, "ERR: Create_dns_rule failed")

    def test_03_config_forged_ip(self):
        rc = dns_filtering_obj.config_whitelist(**fored_ip_settings)
        Assertion.assert_equal(rc, True, "ERR: Set IPV4 and IPV6 fored IP failed")

    ################ Check www.jiayuan.com ##############
    @repeat_method(10)
    def test_04_check_the_answer_address_in_DNS_reply(self):
        flag_log = check_action.check_DNS_reply_the_answer_address('www.jiayuan.com')
        Assertion.assert_equal(flag_log, True, "ERR: The address in DNS_reply is wrong")

    def test_05_check_related_logs(self):
        flag_log = check_action.check_related_logs_fored_ip('www.jiayuan.com')
        logger.info(flag_log)

    ##################### Check  heavengifts.com ##############
    def test_04_check_the_answer_address_in_DNS_reply(self):
        flag_log = check_action.check_DNS_reply_the_answer_address('heavengifts.com')
        Assertion.assert_equal(flag_log, True, "ERR: The address in DNS_reply is wrong")

    def test_05_check_related_logs(self):
        flag_log = check_action.check_related_logs_fored_ip('heavengifts.com')
        logger.info(flag_log)

    ##################### Check jiushang.cn ##############
    @repeat_method(10)
    def test_04_check_the_answer_address_in_DNS_reply(self):
        flag_log = check_action.check_DNS_reply_the_answer_address('jiushang.cn')
        Assertion.assert_equal(flag_log, True, "ERR: The address in DNS_reply is wrong")

    def test_05_check_related_logs(self):
        flag_log = check_action.check_related_logs_fored_ip('jiushang.cn')
        logger.info(flag_log)

    ##################### Check henrymakow.com ##############
    @repeat_method(10)
    def test_04_check_the_answer_address_in_DNS_reply(self):
        flag_log = check_action.check_DNS_reply_the_answer_address_v6('henrymakow.com')
        Assertion.assert_equal(flag_log, True, "ERR: The address in DNS_reply is wrong")

    def test_05_check_related_logs(self):
        flag_log = check_action.check_related_logs_fored_ip('henrymakow.com')
        logger.info(flag_log)

    ##################### Check ultradnsfirewall-ransomware.neustar ##############
    @repeat_method(10)
    def test_04_check_the_answer_address_in_DNS_reply(self):
        flag_log = check_action.check_DNS_reply_the_answer_address_v6('ultradnsfirewall-ransomware.neustar')
        Assertion.assert_equal(flag_log, True, "ERR: The address in DNS_reply is wrong")

    def test_05_check_related_logs(self):
        flag_log = check_action.check_related_logs_fored_ip('ultradnsfirewall-ransomware.neustar')
        logger.info(flag_log)






