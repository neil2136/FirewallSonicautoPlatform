from definition.settings import *
from definition.utils import *


# Verify 'Enable DNS Sinkhole' is disabled by default
class TestSettings_1503271(Test):
    uuid = "SOSAIOT-TC-51701"
    description = show_testcase_info(TESTPLAN, '1503271', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503271')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_default_status_disable(self):
        rc = False
        res = dnsSecurity_api.show_dns_sinkhole()
        if res.get('dns_security') and res['dns_security'].get('dns_sinkhole'):
            rc = res['dns_security']['dns_sinkhole'].get('enable') is False
        Assertion.assert_equal(rc, True, "ERR: check_default_status_disable failed!!")


# Enable/Disable 'Enable DNS Sinkhole'
class TestSettings_1503272(Test):
    uuid = "SOSAIOT-TC-51702"
    description = show_testcase_info(TESTPLAN, '1503272', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503272')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs', 'use_whitelist': True})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    def test_02_disable_dns_sinkhole(self):
        rc = dnsSecurity_api.disable_dns_sinkhole()
        Assertion.assert_equal(rc, True, "ERR: disable_dns_sinkhole failed!!")


# [GUI] IPV4 and IPV6 addresses can be set for Reply with Forged IP
class TestSettings_1503240(Test):
    uuid = "SOSAIOT-TC-51677"
    description = show_testcase_info(TESTPLAN, '1503240', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503240')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_set_dns_sinkhole_forged_ips(self):
        forged_ips = {
            'action': 'dropping_with_dns_reply_of_forged_ip',
            'ipv4': '127.0.0.1',
            'ipv6': '::1'
        }
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **forged_ips)
        Assertion.assert_equal(rc, True, "ERR: set_dns_sinkhole_forged_ips failed!!")


# Verify invalid IP address can't be set for Forged IP, error message will be printed
class TestError_1503242(Test):
    uuid = "SOSAIOT-TC-51678"
    description = show_testcase_info(TESTPLAN, '1503242', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503242')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_set_invalid_dns_sinkhole_forged_ipv4(self):
        forged_ips = {
            'action': 'dropping_with_dns_reply_of_forged_ip',
            'ipv6': '::1'
        }
        for ipv4 in ['10', '10.1', '10.1.1', '10.1.1.256']:
            forged_ips['ipv4'] = ipv4
            res = dnsSecurity_api.enable_dns_sinkhole(msg=True, **forged_ips)
            rc = re.search('invalid format|Invalid IP', json.dumps(res)) if res else False
            if not rc:
                logger.error(f'Set DNS Sinkhole forged ipv4 <{ipv4}> should be failed!!')
                break
        Assertion.assert_equal(bool(rc), True, "ERR: set_invalid_dns_sinkhole_forged_ipv4 failed!!")

    def test_02_set_invalid_dns_sinkhole_forged_ipv6(self):
        forged_ips = {
            'action': 'dropping_with_dns_reply_of_forged_ip',
            'ipv4': '127.0.0.1'
        }
        for ipv6 in ['10', '1001:1', '1001::g']:
            forged_ips['ipv6'] = ipv6
            res = dnsSecurity_api.enable_dns_sinkhole(msg=True, **forged_ips)
            rc = re.search('invalid format|Invalid IP', json.dumps(res)) if res else False
            if not rc:
                logger.error(f'Set DNS Sinkhole forged ipv6 <{ipv6}> should be failed!!')
                break
        Assertion.assert_equal(bool(rc), True, "ERR: set_invalid_dns_sinkhole_forged_ipv6 failed!!")


# Log only:FW will drop the DNS query and log only
class TestFunc_1503243(Test):
    uuid = "SOSAIOT-TC-51679"
    description = show_testcase_info(TESTPLAN, '1503243', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503243')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_dns_sinkhole_drop_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        rc, _ = check_dns_query_result(CParam.Domain, block=True)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_drop_result failed!!")

    def test_03_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Negative Reply:FW will log and send DNS reply with negative answer
class TestFunc_1503244(Test):
    uuid = "SOSAIOT-TC-51680"
    description = show_testcase_info(TESTPLAN, '1503244', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503244')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_negative_dns_reply_to_source'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_dns_sinkhole_negative_reply_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        qry_res, output = check_dns_query_result(CParam.Domain)
        rc = 'SERVFAIL' in str(output) if qry_res else False
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_negative_reply_result failed!!")

    def test_03_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Reply with Forged IP:FW will log and send DNS reply with fake IPV4 address for A query
class TestFunc_1503245(Test):
    uuid = "SOSAIOT-TC-51681"
    description = show_testcase_info(TESTPLAN, '1503245', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503245')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **forged_reply_dict)
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_dns_sinkhole_forged_ip_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        qry_res, output = check_dns_query_result(CParam.Domain)
        rc = forged_reply_dict['ipv4'] in str(output) if qry_res else False
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_forged_ip_result failed!!")

    def test_03_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Reply with Forged IP:FW will log and send DNS reply with fake IPV6 address for AAAA query
class TestFunc_1503246(Test):
    uuid = "SOSAIOT-TC-51682"
    description = show_testcase_info(TESTPLAN, '1503246', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503246')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **forged_reply_dict)
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_dns_sinkhole_forged_ip_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        qry_res, output = check_dns_query_result(CParam.Domain, opt='AAAA')
        rc = forged_reply_dict['ipv6'] in str(output) if qry_res else False
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_forged_ip_result failed!!")

    def test_03_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Verify log can record the infected host's IP who try to connect to forged IP
class TestFunc_1503247(Test):
    uuid = "SOSAIOT-TC-51683"
    description = show_testcase_info(TESTPLAN, '1503247', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503247')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **forged_reply_dict)
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_dns_sinkhole_forged_ip_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        output = PC2_LOGIN.send_command(f'ping {CParam.Domain} -c 3')
        rc = '100% packet loss' in str(output)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_forged_ip_result failed!!")

    def test_03_check_dns_sinkhole_logs(self):
        target = ('Drop DNS Sinkhole Forged IP Packets', f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Query malicious domains with types : CNAME, TXT, MX, NS with action 3 (Reply with Forged IP), forged IP takes effect only when type is A and AAAA
class TestFunc_1503248(Test):
    uuid = "SOSAIOT-TC-51684"
    description = show_testcase_info(TESTPLAN, '1503248', description=True)['title']
    query_type = 'CNAME'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503248')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **forged_reply_dict)
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_dns_sinkhole_forged_ip_result_CNAME(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        _, output = check_dns_query_result(CParam.Domain, block=True, opt=self.query_type)
        forged_res = forged_reply_dict['ipv6'] not in str(output) and forged_reply_dict['ipv4'] not in str(output)
        logger.info(f'Check NO forged-ip result...... {forged_res}')
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        logger.info(f'Check hit malicious logs...... {rc}')
        Assertion.assert_equal(forged_res & rc, True,
                               f"ERR: check_query_type_{self.query_type}_forged_ip_result failed!!")

    def test_03_check_dns_sinkhole_forged_ip_result_TXT(self):
        self.query_type = 'TXT'
        self.test_02_check_dns_sinkhole_forged_ip_result_CNAME()

    def test_04_check_dns_sinkhole_forged_ip_result_MX(self):
        self.query_type = 'MX'
        self.test_02_check_dns_sinkhole_forged_ip_result_CNAME()

    def test_05_check_dns_sinkhole_forged_ip_result_NS(self):
        self.query_type = 'NS'
        self.test_02_check_dns_sinkhole_forged_ip_result_CNAME()


# Query malicious domains with types : CNAME, TXT, MX, NS with action 2 and 1 as it only cares domain not types.
class TestFunc_1503249(Test):
    uuid = "SOSAIOT-TC-51685"
    description = show_testcase_info(TESTPLAN, '1503249', description=True)['title']
    query_type = 'CNAME'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503249')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_negative_dns_reply_to_source'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_negative_reply_result_CNAME(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        _, output = check_dns_query_result(CParam.Domain, opt=self.query_type)
        negative_res = 'SERVFAIL' in str(output)
        logger.info(f'Check negative reply result...... {negative_res}')
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        logger.info(f'Check hit malicious logs...... {rc}')
        Assertion.assert_equal(negative_res & rc, True, f"ERR: check_negative_reply_result_{self.query_type} failed!!")

    def test_03_check_dns_sinkhole_forged_ip_result_TXT(self):
        self.query_type = 'TXT'
        self.test_02_check_negative_reply_result_CNAME()

    def test_04_check_dns_sinkhole_forged_ip_result_MX(self):
        self.query_type = 'MX'
        self.test_02_check_negative_reply_result_CNAME()

    def test_05_check_dns_sinkhole_forged_ip_result_NS(self):
        self.query_type = 'NS'
        self.test_02_check_negative_reply_result_CNAME()

    def test_06_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_07_check_drop_result_CNAME(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        res, _ = check_dns_query_result(CParam.Domain, block=True, opt=self.query_type)
        logger.info(f'Check drop result...... {res}')
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        logger.info(f'Check hit malicious logs...... {rc}')
        Assertion.assert_equal(res & rc, True, f"ERR: check_drop_result_{self.query_type} failed!!")

    def test_08_check_drop_result_TXT(self):
        self.query_type = 'TXT'
        self.test_07_check_drop_result_CNAME()

    def test_09_check_drop_result_MX(self):
        self.query_type = 'MX'
        self.test_07_check_drop_result_CNAME()

    def test_10_check_drop_result_NS(self):
        self.query_type = 'NS'
        self.test_07_check_drop_result_CNAME()


# [GUI]Add/Delete custom malicious domains
class TestSettings_1503251(Test):
    uuid = "SOSAIOT-TC-51687"
    description = show_testcase_info(TESTPLAN, '1503251', description=True)['title']
    domains = [CParam.Custom_Domain_1, CParam.Custom_Domain_2]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503251')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_custom_malicious_domains(self):
        for domain in self.domains:
            rc = dnsSecurity_api.add_dns_custom_list(domain=domain)
            if not rc:
                logger.error(f'Add Domain <{domain}> failed!')
        Assertion.assert_equal(rc, True, "ERR: add_custom_malicious_domains failed!!")

    def test_02_delete_custom_malicious_domains(self):
        rc = dnsSecurity_api.delete_dns_custom_list(domains=self.domains)
        Assertion.assert_equal(rc, True, "ERR: delete_custom_malicious_domains failed!!")


# Verify packet will be dropped if dns query a custom malicious domain
class TestFunc_1503252(Test):
    uuid = "SOSAIOT-TC-51688"
    description = show_testcase_info(TESTPLAN, '1503252', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503252')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    def test_02_add_custom_malicious_domains(self):
        rc_1 = dnsSecurity_api.add_dns_custom_list(domain=CParam.Custom_Domain_1)
        rc_2 = dnsSecurity_api.add_dns_custom_list(domain=CParam.Custom_Domain_2)
        logger.info(f'Add custom domains result...... {rc_1}, {rc_2}')
        Assertion.assert_equal(rc_1 & rc_2, True, "ERR: add_custom_malicious_domains failed!!")

    @repeat_method(3)
    def test_03_check_drop_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        for domain in [CParam.Custom_Domain_1, CParam.Custom_Domain_2]:
            output = PC2_LOGIN.send_command(f'ping {domain} -c 3')
            rc = 'Name or service not known' in str(output)
            if not rc:
                logger.error(f'Query Domain <{domain}> should be dropped')
                break
        Assertion.assert_equal(rc, True, "ERR: check_drop_result failed!!")

    def test_04_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Custom_Domain_1}',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Custom_Domain_2}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Verify packet will not be dropped if custom malicious domain removed
class TestFunc_1503253(Test):
    uuid = "SOSAIOT-TC-51689"
    description = show_testcase_info(TESTPLAN, '1503253', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503253')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    def test_02_delete_custom_malicious_domains(self):
        domains = [CParam.Custom_Domain_1, CParam.Custom_Domain_2]
        rc = dnsSecurity_api.delete_dns_custom_list(domains=domains)
        Assertion.assert_equal(rc, True, "ERR: delete_custom_malicious_domains failed!!")

    @repeat_method(3)
    def test_03_check_allow_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        for domain in [CParam.Custom_Domain_1, CParam.Custom_Domain_2]:
            output = PC2_LOGIN.send_command(f'ping {domain} -c 3')
            rc = 'Name or service not known' not in str(output)
            if not rc:
                logger.error(f'Query Domain <{domain}> should be allowed')
                break
        Assertion.assert_equal(rc, True, "ERR: check_allow_result failed!!")

    def test_04_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Custom_Domain_1}',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Custom_Domain_2}')
        rc = not check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Duplicated malicious domain can't be allowed to be added
class TestError_1503254(Test):
    uuid = "SOSAIOT-TC-51690"
    description = show_testcase_info(TESTPLAN, '1503254', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503254')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_custom_malicious_domain(self):
        rc = dnsSecurity_api.add_dns_custom_list(domain=CParam.Custom_Domain_1)
        Assertion.assert_equal(rc, True, "ERR: add_custom_malicious_domains failed!!")

    def test_02_add_duplicate_custom_domain_failed(self):
        res = dnsSecurity_api.add_dns_custom_list(msg=True, domain=CParam.Custom_Domain_1)
        rc = 'already exist' in json.dumps(res).lower() if res else False
        Assertion.assert_equal(rc, True, "ERR: add_duplicate_custom_domain should fail!!")

    def test_03_delete_added_custom_domains(self):
        rc = dns_cli.del_custom_malicious_entry(*('all',))
        Assertion.assert_equal(rc, True, "ERR: delete_added_custom_domains failed!!")


# Max 128 custom malicious domains can be added
class TestBoundary_1503255(Test):
    uuid = "SOSAIOT-TC-51691"
    description = show_testcase_info(TESTPLAN, '1503255', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503255')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_max_count_custom_malicious_domains(self):
        for count in range(128):
            rc = dnsSecurity_api.add_dns_custom_list(domain=f'{count+1}.com')
            if not rc:
                logger.error(f'Add domain <{count+1}> failed!')
                break
        Assertion.assert_equal(rc, True, "ERR: add_custom_malicious_domains failed!!")

    def test_02_add_one_more_custom_malicious_domain(self):
        res = dnsSecurity_api.add_dns_custom_list(msg=True, domain='129.com')
        rc = 'Custom Malicious Domain List is Full' in json.dumps(res) if res else False
        Assertion.assert_equal(rc, True, "ERR: add_one_more_custom_malicious_domain should fail!!")

    def test_03_delete_added_custom_domains(self):
        rc = dns_cli.del_custom_malicious_entry(*('all',))
        Assertion.assert_equal(rc, True, "ERR: delete_added_custom_domains failed!!")


# [GUI]Add/Delete domain name in white list
class TestSettings_1503256(Test):
    uuid = "SOSAIOT-TC-51692"
    description = show_testcase_info(TESTPLAN, '1503256', description=True)['title']
    domains = [domain_pool[0], domain_pool[1], domain_pool[2], domain_pool[3]]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503256')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_white_list_domains(self):
        for domain in self.domains:
            rc = dnsFil_api.add_dns_whitelist(name=domain)
            if not rc:
                logger.error(f'Add Domain <{domain}> in white list failed!')
        Assertion.assert_equal(rc, True, "ERR: add_white_list_domains failed!!")

    def test_02_delete_white_list_domains(self):
        rc = dnsFil_api.del_dns_whitelist(name_list=(self.domains[0],))
        Assertion.assert_equal(rc, True, "ERR: delete_white_list_domains failed!!")

    def test_03_delete_all_white_list_domains(self):
        self.domains.pop(0)
        rc = dnsFil_api.del_dns_whitelist(name_list=self.domains)
        Assertion.assert_equal(rc, True, "ERR: delete_all_white_list_domains failed!!")


# Verify packet will not be dropped if dns query a malicious domain which is in white list
class TestFunc_1503257(Test):
    uuid = "SOSAIOT-TC-51693"
    description = show_testcase_info(TESTPLAN, '1503257', description=True)['title']
    domains = [CParam.Domain, domain_pool[0]]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503257')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_white_list_domains(self):
        for domain in self.domains:
            rc = dnsFil_api.add_dns_whitelist(name=domain)
            if not rc:
                logger.error(f'Add Domain <{domain}> in white list failed!')
        Assertion.assert_equal(rc, True, "ERR: add_white_list_domains failed!!")

    @repeat_method(3)
    def test_02_check_allow_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        for domain in self.domains:
            initial_packet_monitor()
            start = packet_api.start_capture()
            logger.info(f'Start Capture...... {start}')
            PC2_LOGIN.send_command(f'ping {domain} -c 3')
            cmd_client = f'dns.qry.name=={domain} and ip.src=={PC2_ETH0_IP} and ip.dst=={Parameter.X1_DNS1}'
            rc = check_dns_packets_not_in_wireshark(cmd_client, 'Dropped')
            if not rc:
                logger.error('Find expected packets Failed!')
                break
        Assertion.assert_equal(rc, True, "ERR: check allow result failed!!")

    def test_03_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Custom_Domain_1}',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Custom_Domain_2}')
        rc = not check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Verify packet will be dropped if the malicious domain being removed from white list
class TestFunc_1503258(Test):
    uuid = "SOSAIOT-TC-51694"
    description = show_testcase_info(TESTPLAN, '1503258', description=True)['title']
    domains = [CParam.Domain, domain_pool[0]]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503258')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_remove_white_list_domains(self):
        rc = dnsFil_api.del_dns_whitelist(name_list=self.domains)
        Assertion.assert_equal(rc, True, "ERR: remove_white_list_domains failed!!")

    @repeat_method(3)
    def test_02_check_drop_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        for domain in self.domains:
            output = PC2_LOGIN.send_command(f'ping {domain} -c 3')
            rc = 'Name or service not known' in str(output)
            if not rc:
                logger.error(f'Query Domain <{domain}> should be dropped!')
                break
        Assertion.assert_equal(rc, True, "ERR: check_drop_result failed!!")

    def test_03_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {self.domains[0]}',
                  f'Dropped by DNS sinkhole.Domain: {self.domains[1]}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Duplicated white domain can't be allowed to be added
class TestError_1503259(Test):
    uuid = "SOSAIOT-TC-51695"
    description = show_testcase_info(TESTPLAN, '1503259', description=True)['title']
    jira = 'GEN7-48515'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503259')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_white_list_domain(self):
        rc = dnsFil_api.add_dns_whitelist(name=CParam.Domain)
        Assertion.assert_equal(rc, True, "ERR: add_white_list_domains failed!!")

    def test_02_add_duplicate_white_list_domain_failed(self):
        res = dnsFil_api.add_dns_whitelist(msg=True, name=CParam.Domain)
        rc = 'already exist' in json.dumps(res).lower() if res else False
        Assertion.assert_equal(rc, True, "ERR: add_duplicate_white_list_domain should fail!!")

    def test_03_delete_added_white_list_domain(self):
        rc = dns_cli.del_white_list_domains()
        Assertion.assert_equal(rc, True, "ERR: delete_added_white_list_domain failed!!")


# Expected: Max 128 white lists can be added
class TestBoundary_1503260(Test):
    uuid = "SOSAIOT-TC-51696"
    description = show_testcase_info(TESTPLAN, '1503260', description=True)['title']
    jira = 'GEN7-48515'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503260')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_sinkhole_white_list_with_max_count(self):
        rc = False
        for count in range(128):
            rc = dnsFil_api.add_dns_whitelist(name=f'domain-{count+1}.com')
            if not rc:
                logger.error(f'Add white list <{count+1}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: add_sinkhole_white_list_with_max_count failed!!")

    def test_02_add_sinkhole_white_list_over_max_count_failed(self):
        res = dnsFil_api.add_dns_whitelist(msg=True, name='domain-129.com')
        rc = 'White Entry List is Full' in json.dumps(res[1]) if res and not res[0] else False
        Assertion.assert_equal(rc, True, "ERR: add_sinkhole_white_list_over_max_count should be failed!!")

    def test_03_delete_added_sinkhole_white_list(self):
        rc = dns_cli.del_white_list_domains()
        Assertion.assert_equal(rc, True, "ERR: delete_added_sinkhole_white_list failed!!")


# If same domain added in both malicious and white list, white list has higher priority
class TestFunc_1503262(Test):
    uuid = "SOSAIOT-TC-51697"
    description = show_testcase_info(TESTPLAN, '1503262', description=True)['title']
    jira = 'GEN7-48515'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503262')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_white_list_domain(self):
        rc = dnsFil_api.add_dns_whitelist(name=CParam.Custom_Domain_1)
        Assertion.assert_equal(rc, True, "ERR: add_white_list_domains failed!!")

    def test_02_add_custom_malicious_domain(self):
        rc = dnsSecurity_api.add_dns_custom_list(domain=CParam.Custom_Domain_1)
        Assertion.assert_equal(rc, True, "ERR: add_custom_malicious_domains failed!!")

    @repeat_method(3)
    def test_03_check_dns_query_allow(self):
        rc, _ = check_dns_query_result(CParam.Custom_Domain_1)
        Assertion.assert_equal(rc, True, "ERR: check_dns_query_allow failed!!")

    def test_04_delete_added_domains(self):
        rc_w = dns_cli.del_white_list_domains()
        logger.info(f'Delete added white list domain result...... {rc_w}')
        rc_c = dns_cli.del_custom_malicious_entry(*('all',))
        logger.info(f'Delete added malicious domain result...... {rc_c}')
        Assertion.assert_equal(rc_w & rc_c, True, "ERR: delete_added_domains failed!!")


# Verify CLI support for DNS Sinkhole
class TestSettings_1503264(Test):
    uuid = "SOSAIOT-TC-51698"
    description = show_testcase_info(TESTPLAN, '1503264', description=True)['title']
    jira = 'GEN7-48515'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503264')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_dns_sinkhole_service_cli(self):
        for cmd in sinkhole_service_cmds_list:
            rc = dns_cli.dns_sinkhole_service(**cmd)
            if not rc:
                logger.error(f'Config cmd <{cmd}> failed!')
                break
        Assertion.assert_equal(rc, True, "ERR: config_dns_sinkhole_service_cli failed!!")

    def test_02_add_domains_cli(self):
        domains = [CParam.Custom_Domain_1, CParam.Custom_Domain_2]
        rc_w = dns_cli.add_white_list_domains(*domains)
        logger.info(f'Add white list domains result...... {rc_w}')
        rc_c = dns_cli.add_custom_malicious_entry(*domains)
        logger.info(f'Add malicious domains result...... {rc_c}')
        Assertion.assert_equal(rc_w & rc_c, True, "ERR: config_dns_sinkhole_service_cli failed!!")

    def test_03_show_sinkhole_cli(self):
        for cmd, target in show_check_cli_dict.items():
            out = dns_cli.show_dns(text=cmd)
            rc = target in str(out)
            if not rc:
                logger.error(f'show cmd <{cmd}> failed!')
                break
        Assertion.assert_equal(rc, True, "ERR: show_sinkhole_cli failed!!")

    def test_04_delete_domains_cli(self):
        rc_w = dns_cli.del_white_list_domains()
        logger.info(f'Delete white list domains result...... {rc_w}')
        rc_c = dns_cli.del_custom_malicious_entry(*('all',))
        logger.info(f'Delete malicious domains result...... {rc_c}')
        Assertion.assert_equal(rc_w & rc_c, True, "ERR: delete_domains_cli failed!!")


# Verify packet will be dropped if dns query a malicious domain
class TestFunc_1503230(Test):
    uuid = "SOSAIOT-TC-51668"
    description = show_testcase_info(TESTPLAN, '1503230', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503230')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_drop_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        rc, _ = check_dns_query_result(domain=CParam.Domain, block=True)
        Assertion.assert_equal(rc, True, "ERR: check_drop_result failed!!")

    def test_03_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Verify DNS sinkhole has no effect on normal dns query
class TestFunc_1503231(Test):
    uuid = "SOSAIOT-TC-51669"
    description = show_testcase_info(TESTPLAN, '1503231', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503231')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_allow_result(self):
        rc, _ = check_dns_query_result(domain=CParam.Custom_Domain_1)
        Assertion.assert_equal(rc, True, "ERR: check_allow_result failed!!")


# Verify DNS sinkhole can work for both IPV4 and IPV6 DNS query(A and AAAA)
class TestFunc_1503232(Test):
    uuid = "SOSAIOT-TC-51670"
    description = show_testcase_info(TESTPLAN, '1503232', description=True)['title']
    qry_type = 'A'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503232')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    @repeat_method(3)
    def test_02_check_drop_result_ipv4(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        qry_res, _ = check_dns_query_result(domain=CParam.Domain, block=True, opt=self.qry_type)
        logger.info(f'Check dns query result...... {qry_res}')
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_drop_result failed!!")

    def test_03_check_drop_result_ipv6(self):
        self.qry_type = 'AAAA'
        self.test_02_check_drop_result_ipv4()


# Test build-in malicious database, dns querying for the domains in database will be dropped
class TestFunc_1503233(Test):
    uuid = "SOSAIOT-TC-51671"
    description = show_testcase_info(TESTPLAN, '1503233', description=True)['title']
    filepath = "/tmp/sinkhole_log"
    jira = 'GEN7-47858'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503233')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_negative_dns_reply_to_source'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    def test_02_load_database_list(self):
        with open(f"{script_path}Database", "r", encoding='UTF-8') as f:
            CParam.Database_list = f.readlines()
        Assertion.assert_not_equal(len(CParam.Database_list), 0, "ERR: load_database_list failed!!")

    def test_03_check_drop_logs(self):
        rc = False
        check_part = len(CParam.Database_list) / 800 + 1
        for i in range(int(check_part)):
            logger.info(f"{f' Run for part {i}':=>70}")
            logger.info(f"{'  Clear log  ':-^50}")
            _ = logMonitor_api.clear_log()

            logger.info(f"{'  Query from PC2  ':-^50}")
            if i < check_part-1:
                domains = CParam.Database_list[i*800:(i+1)*800-1]
            else:
                domains = CParam.Database_list[i*800:]
            domain_list = str(domains).replace(r'\n', '').replace(', ', ',')
            out = PC2_LOGIN.send_command(f'python3 /tmp/PC2_query.py {domain_list}')
            logger.info(f"---> {'Query END' in str(out)}")

            logger.info(f"{'  Export log to file  ':-^50}")
            res = logMonitor_api.export_log_txt(log_switch=False)
            res = str(res)
            # logger.info(res)
            logger.info(f"---> {bool(res)}")

            logger.info(f"{'  Check drop logs  ':-^50}")
            for domain in domains:
                domain = domain.strip()
                rc = f'Dropped by DNS sinkhole.Domain: {domain}' in res
                if not rc:
                    logger.error(f'Block Domain {domain} failed!!')
                    break
            logger.info(f'---> {rc}')
            if not rc:
                break
        Assertion.assert_equal(rc, True, "ERR: check_drop_log failed!!")


# Verify FW can be managed normally and CUP utilization is normal if DNS flood happened
class TestFunc_1503234(Test):
    uuid = "SOSAIOT-TC-51672"
    description = show_testcase_info(TESTPLAN, '1503234', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503234')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    def test_02_do_dns_flood_and_check_cpu(self):
        PC2_LOGIN.send_command('python3 /tmp/dns_flooding.py &', backend=True)
        time.sleep(5)
        res = diag_cli.show_cpu()
        rc = re.search('Current 10s CPU Utilization: 100%|Total Average CPU Utilization: 100%', res, re.I)
        Assertion.assert_equal(not rc, True, "ERR: do_dns_flood_and_check_cpu failed!!")

    def test_03_config_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_negative_dns_reply_to_source'})
        Assertion.assert_equal(rc, True, "ERR: config_dns_sinkhole failed!!")


# DNS sinkhole can work well when have Split DNS configured
class TestFunc_1503236(Test):
    uuid = "SOSAIOT-TC-51673"
    description = show_testcase_info(TESTPLAN, '1503236', description=True)['title']
    qry_domain = CParam.Custom_Domain_1

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503236')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_split_dns(self):
        split_dns = {
            'domain': self.qry_domain,
            'ipv4': {
                'primary': Parameter.X1_DNS2,
                'secondary': '',
                'tertiary': ''
            },
            'ipv6': {
                'primary': '',
                'secondary': '',
                'tertiary': ''
            },
            'local_interface': 'X0',
        }
        rc = dnsSett_api.add_split_dns(**split_dns)
        Assertion.assert_equal(rc, True, "ERR: failed to add_split_dns !!")

    def test_02_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    def test_03_add_domain_to_malicious_list(self):
        rc = dnsSecurity_api.add_dns_custom_list(domain=self.qry_domain)
        Assertion.assert_equal(rc, True, "ERR: add_domain_to_malicious_list failed!!")

    @repeat_method(3)
    def test_04_check_drop_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        rc, _ = check_dns_query_result(domain=self.qry_domain, block=True)
        Assertion.assert_equal(rc, True, "ERR: check_drop_result failed!!")

    def test_05_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {self.qry_domain}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")

    def test_06_delete_added_domain(self):
        rc = dnsSecurity_api.delete_dns_custom_list(domains=(self.qry_domain,))
        Assertion.assert_equal(rc, True, "ERR: delete_added_domain failed!!")

    def test_07_initial_split_dns(self):
        rc = dnsSett_api.delete_split_dns(domain=self.qry_domain)
        Assertion.assert_equal(rc, True, "ERR: failed to initial_split_dns !!")


# Verify the DNS query that initiated by firewall itself (e.g. FQDN AO, or diagnostic DNS lookup)
class TestFunc_1503237(Test):
    uuid = "SOSAIOT-TC-51674"
    description = show_testcase_info(TESTPLAN, '1503237', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503237')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    def test_02_do_dns_lookup(self):
        rc = diagnostic_api.diag_dns_lookup_name_by_api(msg=False, **{'type': 'system', 'domain_name': domain_pool[0]})
        Assertion.assert_equal(rc, True, "ERR: do_dns_lookup failed")

    def test_03_add_fqdn(self):
        rc = ao_api.config_addressobject(msg=False, **ao_dict)
        Assertion.assert_equal(rc, True, "ERR: add_fqdn failed")

    def test_04_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {domain_pool[0]}',
                  f'Dropped by DNS sinkhole.Domain: {ao_dict["value"]}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")

    def test_05_delete_added_fqdn(self):
        rc = ao_api.del_addressobject(**{'ip_type': 'fqdn', 'name': ao_dict['name']})
        Assertion.assert_equal(rc, True, "ERR: delete added fqdn failed")


# Verify DNS sinkhole will work will if DNS proxy enabled
class TestFunc_1503274(Test):
    uuid = "SOSAIOT-TC-51703"
    description = show_testcase_info(TESTPLAN, '1503274', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503274')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    def test_02_add_dns_proxy_rule(self):
        rc = dnsRule_api.add_dns_rule(**dns_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_proxy_rule failed")

    @repeat_method(3)
    def test_03_check_drop_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        rc, _ = check_dns_query_result(domain=CParam.Domain, block=True, opt=f'@{Parameter.FIREWALL}')
        Assertion.assert_equal(rc, True, "ERR: check_drop_result failed!!")

    def test_04_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Domain}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")


# Both DNS proxy and cache enabled, query domain B, B has been cached, before cache expired,
# add B into custom malicious domain list, query B again
class TestFunc_1503229(Test):
    uuid = "SOSAIOT-TC-51667"
    description = show_testcase_info(TESTPLAN, '1503229', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503229')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    @repeat_method(3)
    def test_01_cache_malicious_domain(self):
        res, _ = check_dns_query_result(domain=CParam.Custom_Domain_1, opt=f'@{Parameter.FIREWALL}')
        out = dnsProxy_api.show_dns_proxy_caches_report()
        rc = CParam.Custom_Domain_1 in json.dumps(out) if res else False
        Assertion.assert_equal(rc, True, "ERR: cache_malicious_domain failed!!")

    def test_02_add_domain_to_malicious_list(self):
        rc = dnsSecurity_api.add_dns_custom_list(domain=CParam.Custom_Domain_1)
        Assertion.assert_equal(rc, True, "ERR: add_domain_to_malicious_list failed!!")

    @repeat_method(3)
    def test_03_check_drop_result(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        rc, _ = check_dns_query_result(domain=CParam.Custom_Domain_1, block=True, opt=f'@{Parameter.FIREWALL}')
        Assertion.assert_equal(rc, True, "ERR: check_drop_result failed!!")

    def test_04_check_dns_sinkhole_logs(self):
        target = ('Drop Hit DNS Sinkhole Malicious Database Packets',
                  f'Dropped by DNS sinkhole.Domain: {CParam.Custom_Domain_1}')
        rc = check_related_logs(target=target)
        Assertion.assert_equal(rc, True, "ERR: check_dns_sinkhole_logs failed!!")

    def test_05_delete_added_domain(self):
        rc = dnsSecurity_api.delete_dns_custom_list(domains=(CParam.Custom_Domain_1,))
        Assertion.assert_equal(rc, True, "ERR: delete_added_domain failed!!")


# Verify all sinkhole configuration info included in tsr
class TestSettings_1503228(Test):
    uuid = "SOSAIOT-TC-51666"
    description = show_testcase_info(TESTPLAN, '1503228', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503228')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSecurity_api.enable_dns_sinkhole(msg=False, **forged_reply_dict)
        Assertion.assert_equal(rc, True, "ERR: enable_dns_sinkhole failed!!")

    def test_02_check_tsr(self):
        out = diagnostic_api.get_tsr_part(func='Network', lab1='DNS Security')
        logger.info(f'TSR\n{out}')
        check_infos = (
            'Enable DNS Sinkhole Service: 1',
            'Dropping, with DNS reply of Forged IP',
            forged_reply_dict['ipv4'],
            forged_reply_dict['ipv6'],
            'Enable WhiteList: Yes',
            'Malicious Domain Name Total Number: 16045 Entries',
            'Detection Number',
            'Total Custom Entry Count'
        )
        for check_info in check_infos:
            rc = check_info in str(out)
            if not rc:
                logger.error(f'Info <{check_info}> is not in TSR !!!')
                break
        Assertion.assert_equal(rc, True, "ERR: check_tsr failed!!")


# Verify settings keep intack after exp export/import
class TestSettings_1503250(Test):
    uuid = "SOSAIOT-TC-51686"
    description = show_testcase_info(TESTPLAN, '1503250', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503250')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_sinkhole(self):
        forged_reply_dict['use_whitelist'] = False
        base_res = dnsSecurity_api.enable_dns_sinkhole(msg=False, **forged_reply_dict)
        logger.info(f'Config dns sinkhole base settings...... {base_res}')
        custom_domain_res = dnsSecurity_api.add_dns_custom_list(domain=CParam.Custom_Domain_1)
        logger.info(f'Config dns filtering custom domain...... {custom_domain_res}')
        rc = base_res & custom_domain_res
        Assertion.assert_equal(rc, True, "ERR: failed to config sinkhole !!")

    def test_02_export_configs(self):
        rc = sett_api.export_setting_exp()
        Assertion.assert_equal(rc, True, "ERR: failed to export configs !!")

    def test_03_initialize_all_configs(self):
        default_config = {
            'action': 'dropping_with_dns_reply_of_forged_ip',
            'ipv4': '127.0.0.1',
            'ipv6': '::1',
            'use_whitelist': True
        }
        forged_ip_res = dnsSecurity_api.enable_dns_sinkhole(msg=False, **default_config)
        base_res = dnsSecurity_api.disable_dns_sinkhole()
        logger.info(f'Initialize dns sinkhole base settings...... {forged_ip_res}, {base_res}')
        custom_domain_res = dnsSecurity_api.delete_dns_custom_list(domains=(CParam.Custom_Domain_1,))
        logger.info(f'Initialize dns sinkhole custom domain...... {custom_domain_res}')
        rc = forged_ip_res & base_res & custom_domain_res
        Assertion.assert_equal(rc, True, "ERR: failed to initialize_all_configs !!")

    def test_04_import_configs(self):
        rc = sett_api.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(rc, True, "ERR: failed to import_configs !!")

    @repeat_method(3)
    def test_05_check_configs(self):
        time.sleep(10)
        base_out = json.dumps(dnsSecurity_api.show_dns_sinkhole())
        base_rc = all(json.dumps(x) in base_out for x in forged_reply_dict.values())
        logger.info(f'Check dns sinkhole base settings...... {base_rc}')

        custom_domain_out = dnsSecurity_api.show_dns_custom_list()
        cus_rc = CParam.Custom_Domain_1 in json.dumps(custom_domain_out)
        logger.info(f'Check dns sinkhole custom domain...... {cus_rc}')

        rc = base_rc & cus_rc
        Assertion.assert_equal(rc, True, "ERR: failed to check_configs !!")


# Verify the settings keep intact after restart FW
class TestSettings_1503239(Test):
    uuid = "SOSAIOT-TC-51676"
    description = show_testcase_info(TESTPLAN, '1503239', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1503239')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_reboot(self):
        rc = sett_api.boot_fw(mode=1)
        Assertion.assert_equal(rc, True, "ERR: failed to reboot !!")

    def test_02_check_configs(self):
        TestSettings_1503250().test_05_check_configs()
