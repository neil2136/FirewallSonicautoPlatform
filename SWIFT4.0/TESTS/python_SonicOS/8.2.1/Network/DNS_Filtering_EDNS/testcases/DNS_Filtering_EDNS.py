from definition.settings import *
from definition.utils import *


# Expected: Check DNS query received and forwarded by DUT keeps same and DNS response received
# includes category information
class Test_Category_to_Client(Test):
    uuid = "SOSAIOT-TC-51409"
    # uuid = '68333034-8641-11EB-826C-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521032', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521032')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_packet_monitor_and_dns_cache(self):
        rc = initial_packet_monitor_and_flush_dns_cache()
        Assertion.assert_equal(rc, True, "ERR: initial monitor and cache failed!!")

    def test_02_do_dig_to_check_DNS_response(self):
        query_rc, output = check_dns_query_no_error(CParam.Domain)
        rc = CParam.EDNS_Record in output if query_rc else False
        Assertion.assert_equal(rc, True, "ERR: check DNS response failed!!")

    def test_03_check_DNS_query_from_client(self):
        cmd_client = f'dns.qry.name=={CParam.Domain} and ip.src=={PC1_ETH0_IP} and ip.dst=={Parameter.FIREWALL}'
        found = check_dns_packets_in_wireshark(cmd_client, CParam.EDNS_Flag_On)
        Assertion.assert_equal(found, True, "ERR: failed to find expected packets")

    def test_04_check_DNS_query_to_Neustar_Server(self):
        cmd_fw = f'dns.qry.name=={CParam.Domain} and ip.src=={Parameter.X1_IP} and ip.dst=={Parameter.Neustar_server}'
        found = check_dns_packets_in_wireshark(cmd_fw, CParam.EDNS_Flag_On)
        Assertion.assert_equal(found, True, "ERR: failed to find expected packets")


# Expected: Check DNS response contains category info and DNS proxy cache table displays correctly
class Test_Resp_Category_Cache(Test):
    uuid = "SOSAIOT-TC-51410"
    # uuid = '6833B9C8-8641-11EB-826C-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521033', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521033')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_DNS_packet_from_Default_Server(self):
        cmd = f'dns.qry.name=={CParam.Domain} and ip.src=={Parameter.Neustar_server} and ip.dst=={Parameter.X1_IP}'
        ekey = (CParam.EDNS_Flag_On, CParam.Pkt_EDNS, CParam.Pkt_Category)
        rc = check_dns_packets_in_wireshark(cmd, ekey)
        Assertion.assert_equal(rc, True, "ERR: failed to find expected packets")

    def test_02_check_DNS_proxy_cache(self):
        rc = False
        caches = dnspxy_api.show_dns_proxy_caches_report()
        for cache in caches:
            rc = cache.get('category') == 'Gaming' and cache.get('domain_name') == CParam.Domain
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: Fail to check_DNS_proxy_cache")


# Expected: Check DNS response generated and sent by DUT contains Additional Records.
class Test_Resp_Category_Sent_by_FW(Test):
    uuid = "SOSAIOT-TC-51411"
    # uuid = '683425A2-8641-11EB-826C-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521034', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521034')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_DNS_resp_from_firewall(self):
        cmd = f'dns.qry.name=={CParam.Domain} and ip.src=={Parameter.FIREWALL} and ip.dst=={PC1_ETH0_IP}'
        ekey = (CParam.EDNS_Flag_On, CParam.Pkt_EDNS, CParam.Pkt_Category)
        rc = check_dns_packets_in_wireshark(cmd, ekey)
        Assertion.assert_equal(rc, True, "ERR: failed to find expected packets")


# Expected: Check Firewall added Additional Records to the DNS query without RR from client
class Test_without_Additional_RRs(Test):
    uuid = "SOSAIOT-TC-51413"
    # uuid = '68356688-8641-11EB-826C-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521037', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521037')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_packet_monitor_and_dns_cache(self):
        rc = initial_packet_monitor_and_flush_dns_cache()
        Assertion.assert_equal(rc, True, "ERR: initial monitor and cache failed")

    def test_02_do_nslookup(self):
        rc, res = check_dns_query_no_error(CParam.Domain, opt='nslookup')
        Assertion.assert_equal(rc, True, "ERR: do_nslookup failed")

    def test_03_check_DNS_query_from_client(self):
        cmd_client = f'dns.qry.name=={CParam.Domain} and ip.src=={PC1_ETH0_IP} and ip.dst=={Parameter.FIREWALL}'
        found = check_dns_packets_in_wireshark(cmd_client, CParam.EDNS_Flag_Off)
        Assertion.assert_equal(found, True, "ERR: failed to find expected packets")

    def test_04_check_DNS_query_to_Neustar_Server(self):
        cmd_fw = f'dns.qry.name=={CParam.Domain} and ip.src=={Parameter.X1_IP} and ip.dst=={Parameter.Neustar_server}'
        found = check_dns_packets_in_wireshark(cmd_fw, CParam.EDNS_Flag_On)
        Assertion.assert_equal(found, True, "ERR: failed to find expected packets")


# Expected: Check DNS query without RR from client is forwarded by Firewall when DNS filter policy is disabled.
class Test_Disable_without_RRs(Test):
    uuid = "SOSAIOT-TC-51414"
    # uuid = '6835D7E4-8641-11EB-826C-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521038', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521038')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_dns_filter_policy(self):
        disable = {
            'name': filter_rule_dict['dns_policies'][0]['name'],
            'enable': False
        }
        rc = dnsRule_api.edit_dns_rule(**disable)
        Assertion.assert_equal(rc, True, "ERR: disable_dns_filter_policy failed")

    def test_02_initial_packet_monitor_and_dns_cache(self):
        rc = initial_packet_monitor_and_flush_dns_cache()
        Assertion.assert_equal(rc, True, "ERR: initial monitor and cache failed")

    def test_03_do_nslookup(self):
        rc, res = check_dns_query_no_error(CParam.Domain, opt='nslookup')
        Assertion.assert_equal(rc, True, "ERR: do_nslookup failed")

    def test_04_check_DNS_query_from_client_no_RRs(self):
        cmd_client = f'dns.qry.name=={CParam.Domain} and ip.src=={PC1_ETH0_IP} and ip.dst=={Parameter.FIREWALL}'
        found = check_dns_packets_in_wireshark(cmd_client, CParam.EDNS_Flag_Off)
        Assertion.assert_equal(found, True, "ERR: failed to find expected packets")

    def test_05_check_DNS_query_to_Neustar_Server_no_RRs(self):
        cmd_fw = f'dns.qry.name=={CParam.Domain} and ip.src=={Parameter.X1_IP} and ip.dst=={Parameter.Neustar_server}'
        found = check_dns_packets_in_wireshark(cmd_fw, CParam.EDNS_Flag_Off)
        Assertion.assert_equal(found, True, "ERR: failed to find expected packets")


# Expected: Check DNS response contains category information and DNS proxy cache table displays correctly
class Test_Disable_Resp_Category_Cache(Test):
    uuid = "SOSAIOT-TC-51412"
    # uuid = '68349046-8641-11EB-826C-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521035', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521035')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_dns_filter_policy(self):
        disable = {
            'name': filter_rule_dict['dns_policies'][0]['name'],
            'enable': False
        }
        rc = dnsRule_api.edit_dns_rule(**disable)
        Assertion.assert_equal(rc, True, "ERR: disable_dns_filter_policy failed")

    def test_02_initial_packet_monitor_and_dns_cache(self):
        rc = initial_packet_monitor_and_flush_dns_cache()
        Assertion.assert_equal(rc, True, "ERR: initial monitor and cache failed")

    def test_03_do_dig_to_check_DNS_response(self):
        rc, res = check_dns_query_no_error(CParam.Domain)
        Assertion.assert_equal(rc, True, "ERR: do_dig failed")

    def test_04_DNS_packet_from_Neustar_with_RRs(self):
        cmd = f'dns.qry.name=={CParam.Domain} and ip.src=={Parameter.Neustar_server} and ip.dst=={Parameter.X1_IP}'
        ekey = (CParam.EDNS_Flag_On, CParam.Pkt_EDNS, CParam.Pkt_Category)
        rc = check_dns_packets_in_wireshark(cmd, ekey)
        Assertion.assert_equal(rc, True, "ERR: failed to find expected packets")

    def test_05_check_DNS_proxy_cache_null(self):
        rc = False
        caches = dnspxy_api.show_dns_proxy_caches_report()
        for cache in caches:
            rc = cache.get('category') == ' ' and cache.get('domain_name') == CParam.Domain
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: Category should not display in DNS_proxy_cache!!")
