from definition.settings import *
import unittest

class TestCheck_dns_server_1(Test):
    uuid = 'NonTC'
    description= 'TestCheck_dns_server_1'
    goto_teardown = True

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


class TestDNS_Filtering_Forged_IP_FC_010(Test):
    uuid = "SOSAIOT-TC-51563"
    description= show_testcase_info(Parameter.TESTPLAN, '010', description=True)['title']
    goto_teardown = True
    jira = 'Gen7-44568'

    def test_000_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '010')
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
                        "filter_profile": "test"
                    }
                }
            ]
        }
        rc = dnsrule_obj.add_dns_rule(**add_rule)
        Assertion.assert_equal(rc, True, "ERR: Create_dns_rule failed")

    def test_01_config_ipv4_forged_ip(self):
        fored_ip_settings = {
            "dns_security": {
                "dns_filtering": {
                    "useWhiteList": True,
                    "forged_ip": {
                        "ipv4": "10.0.0.1",
                        "ipv6": "::1"
                    }
                }
            }
        }
        rc = config_forged_ip_obj.config_whitelist(**fored_ip_settings)
        Assertion.assert_equal(rc, True, "ERR: Set IPV4 fored IP failed")

    @repeat_method(5)
    def test_02_Verify_when_the_DNS_reply_with_type_A(self):
        diag_command = 'dig www.ea.com -t A @'+ Parameter.DUT_X0_IP
        logger.info(diag_command)
        rc = os.popen(diag_command).read()
        Assertion.assert_regular(rc, Parameter.Forged_ip_ipv4, "ERR: Verify when the DNS reply with type A failed")


class TestDNS_Filtering_Forged_IP_FC_011(Test):
    uuid = "SOSAIOT-TC-51564"
    description= show_testcase_info(Parameter.TESTPLAN, '011', description=True)['title']
    goto_teardown = True
    jira = "GEN7-32658"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '011')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ipv6_forged_ip(self):
        fored_ip_settings = {
            "dns_security": {
                "dns_filtering": {
                    "useWhiteList": True,
                    "forged_ip": {
                        "ipv4": "127.0.0.1",
                        "ipv6": "1001::1"
                    }
                }
            }
        }
        rc = config_forged_ip_obj.config_whitelist(**fored_ip_settings)
        Assertion.assert_equal(rc, True, "ERR: Set IPV4 fored IP failed")

    @repeat_method(5)
    def test_02_Verify_when_the_DNS_reply_with_type_AAAAA(self):
        diag_command = 'dig www.ea.com -t AAAA @'+ Parameter.DUT_X0_IP
        logger.info(diag_command)
        rc = os.popen(diag_command).read()
        Assertion.assert_regular(rc, Parameter.Forged_ip_ipv6, "ERR: Verify when the DNS reply with type AAAA failed")


class TestDNS_Filtering_Forged_IP_FC_012(Test):
    uuid = "SOSAIOT-TC-51565"
    description= show_testcase_info(Parameter.TESTPLAN, '012', description=True)['title']
    goto_teardown = True
    jira = "GEN7-32658"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '012')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ipv4_ipv6_forged_ip(self):
        fored_ip_settings = {
            "dns_security": {
                "dns_filtering": {
                    "useWhiteList": True,
                    "forged_ip": {
                        "ipv4": "10.0.0.1",
                        "ipv6": "1001::1"
                    }
                }
            }
        }
        rc = config_forged_ip_obj.config_whitelist(**fored_ip_settings)
        Assertion.assert_equal(rc, True, "ERR: Set IPV4 fored IP failed")

    @repeat_method(5)
    def test_02_Verify_when_the_DNS_reply_with_type_CNAME(self):
        diag_command = 'dig www.ea.com -t CNAME @'+ Parameter.DUT_X0_IP
        logger.info(diag_command)
        result = os.popen(diag_command).read()
        logger.info(result)
        try:
            if Parameter.Forged_ip_ipv4 in result or Parameter.Forged_ip_ipv6 in result:
                rc = False
            else:
                rc = True
        except:
            logger.error("May get  www.ea.com information failed.")
        Assertion.assert_equal(rc, True, "ERR: Verify when the DNS reply with type CNAME failed")


class TestDNS_Filtering_Forged_IP_FC_005(Test):
    uuid = "SOSAIOT-TC-51558"
    description= show_testcase_info(Parameter.TESTPLAN, '005', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '005')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_download_tsr(self):
        rc = False
        down_tsr_obj.download_tsr()
        try:
            if os.path.exists("/tmp/techSupport"):
                rc = True
            else:
                logger.info("Not found the target tsr content part")
        except:
            logger.error("Download TSR failed.")
        Assertion.assert_equal(rc, True, "ERR: Download TSR failed")

    def test_02_vefiry_forged_ip_in_tsr(self):
        flag = False
        tsr_content = down_tsr_obj.get_tsr_part('Network', lab1='DNS Security')
        match1 = re.search(Parameter.Forged_ip_ipv4, tsr_content, re.I|re.S)
        if match1:
            logger.info(match1)
            logger.error('Fored IP of IPV4 info are in TSR')
            match2 = re.search(Parameter.Forged_ip_ipv6_in_tsr, tsr_content, re.I|re.S)
            if match2:
                logger.info(match2)
                logger.error('Fored IP of IPV6 info are in TSR')
                flag = True
            else:
                logger.error('Fored IP of IPV6 info are not in TSR')
        else:
            logger.info("Not found the target tsr content part")
        Assertion.assert_equal(flag, True, "ERR: Verify forged ip in tsr failed") 


class TestDNS_Filtering_Forged_IP_FC_006(Test):
    uuid = "SOSAIOT-TC-51560"
    description= show_testcase_info(Parameter.TESTPLAN, '006', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '006')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ipv4_ipv6_forged_ip_use_cli(self):
        forged_dict = {
            'forged-ip': '10.0.0.2 1001::3'
        }
        rc = forged_ip_cli.config_dns_filtering_base(**forged_dict)
        Assertion.assert_equal(rc, True, "ERR: Config forged ip use cli failed")  
    
    def test_02_verify_forged_ip_info(self):
        flag = False
        rc = config_forged_ip_obj.check_dns_filtering_global_settings()
        logger.info(rc)
        try:
            if rc['dns_security']['dns_filtering']['forged_ip']['ipv4'] == '10.0.0.2' and \
               rc['dns_security']['dns_filtering']['forged_ip']['ipv6'] == '1001::3':
               flag = True
            else:
                logger.error(rc)
        except:
            logger.error("May get forged ip info failed.")
        Assertion.assert_equal(flag, True, "ERR: Verify_forged_ip info failed")





