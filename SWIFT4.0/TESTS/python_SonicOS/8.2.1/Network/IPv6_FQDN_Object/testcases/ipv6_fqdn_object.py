import json
import re
import ipaddress
from definition.settings import *
from definition.utils import *


class TestTC01_add_ipv6_fqdn_ao(Test):
    uuid = "SOSAIOT-TC-56566"
    description = show_testcase_info(TESTPLAN, 'tc01', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_ipv6_fqdn_ao(self):
        probe_object_dict = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Hostname_one_ipv6,
            "zone": "WAN",
            "value": Parameter.FQDN_Hostname_one_ipv6
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add FQDN address object failed")

    @repeat_method(3)
    def test_03_check_resolved_ipv6_address(self):
        time.sleep(10)
        output = addressobjectsapi.get_DAO_info(Parameter.FQDN_Hostname_one_ipv6)
        logger.info(f'output is:{output}')
        flag = True if f'Host: {PC3_ETH1_IPv6}' in str(output) else False
        Assertion.assert_equal(flag, True, "ERR: check resolved ipv6 address failed")

    def test_04_delete_fqdn_ao(self):
        res = addressobjectsapi.del_ao_by_name(name=Parameter.FQDN_Hostname_one_ipv6, version='fqdn')
        Assertion.assert_equal(res, True, "ERR: check resolved ipv6 address failed")


class TestTC04_add_ipv6_fqdn_ao_conclude_wildcard(Test):
    uuid = "SOSAIOT-TC-56567"
    description = show_testcase_info(TESTPLAN, 'tc04', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc04')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_fqdn_over_tcp_dns_for_dns_settings_on_dut(self):
        dns_update = {
            "dns": {
                "fqdn_over_tcp_dns": True,
            }
        }
        rc = dnssettingsapi.set_dns(**dns_update)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_03_add_ipv6_wildcard_fqdn_ao(self):
        probe_object_dict = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Wildcard_Hostname,
            "zone": "WAN",
            "value": Parameter.FQDN_Wildcard_Hostname
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add wildcard FQDN address object failed")

    def test_04_add_ipv6_fqdn_ao(self):
        probe_object_dict = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Mixed_Hostname,
            "zone": "WAN",
            "value": Parameter.FQDN_Mixed_Hostname
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add FQDN address object failed")

    @repeat_method(3)
    def test_05_check_tcp_dns_query_response_packets_with_30_resolved_ipv4_hosts_and_30_resolved_ipv6_hosts(self):
        flag = False
        hostsipv4list = []
        hostsipv6list = []
        # generate domain name's IPs on dns server: ipv4:12.12.1.30--12.12.1.59, ipv6:2001:20::30 to 2001:20::59
        for i in range(30, 60):
            hostsipv4list.append(f'12.12.1.{i}')
            hostsipv6list.append(f'2001:20::{i}')
        logger.info(f'hostsipv4list is:{hostsipv4list},hostsipv6list is:{hostsipv6list}')
        res1 = addressobjectsapi.purge_ao_by_name(name=Parameter.FQDN_Mixed_Hostname, version='fqdn')
        res2 = dnsproxyapi.flush_caches(ip_version = 'ipv4')  # need add this step to flush fqdn ao cache
        start_capture_and_clear_packets(packetmonitorapi)
        res3 = addressobjectsapi.resolve_ao_by_name(name=Parameter.FQDN_Mixed_Hostname, version='fqdn')
        time.sleep(10)
        logger.info(f'res1 is {res1},res2 is:{res2},res3 is :{res3}')
        if res1 and res2 and res3:
            (answeripv4list, answeripv6list) = check_dns_udp_packets(packetmonitorapi, PC1_Login, Parameter.FQDN_Mixed_Hostname,
                                                                     type='mixed')
            logger.info(f'answeripv4list is:{answeripv4list},answeripv6list is:{answeripv6list}')
            if (set(answeripv4list) == set(hostsipv4list)) and (set(answeripv6list) == set(hostsipv6list)):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: check tcp response with 30 ipv4 and 30 ipv6 resolved ips")

    def test_06_check_fqdn_ao_resolved_ipv4_and_ipv6_address_on_gui(self):
        # gui cannot display all the resolved ips,so check some ips
        output = addressobjectsapi.get_DAO_info(Parameter.FQDN_Mixed_Hostname)
        logger.info(f'output is:{output}')
        ipv4resolvedlist = re.findall(r'\d+\.\d+\.\d+\.\d+', str(output), re.I | re.S | re.M)
        ipv6resolvedlist = re.findall(r'\d+\:\d+\::[A-Za-z0-9]+', str(output), re.I | re.S | re.M)
        logger.info(f'ipv4resolvedlist is:{ipv4resolvedlist},lenth is:{len(ipv4resolvedlist)}\n,'
                    f'ipv6resolvedlist is:{ipv6resolvedlist},length is:{len(ipv6resolvedlist)}')
        flag = True if len(ipv4resolvedlist) >= 10 and len(ipv6resolvedlist) >= 10 else False
        Assertion.assert_equal(flag, True, "ERR: check fqdn ao resolved ips on gui failed")

    def test_07_check_wildcard_fqdn_ao_resolved_ipv4_and_ipv6_address_on_gui(self):
        output = addressobjectsapi.get_DAO_info(Parameter.FQDN_Wildcard_Hostname)
        logger.info(f'output is:{output}')
        ipv4resolvedlist = re.findall(r'\d+\.\d+\.\d+\.\d+', str(output), re.I | re.S | re.M)
        ipv6resolvedlist = re.findall(r'\d+\:\d+\::[A-Za-z0-9]+', str(output), re.I | re.S | re.M)
        logger.info(f'ipv4resolvedlist is:{ipv4resolvedlist},lenth is:{len(ipv4resolvedlist)}\n,'
                    f'ipv6resolvedlist is:{ipv6resolvedlist},length is:{len(ipv6resolvedlist)}')
        flag = True if len(ipv4resolvedlist) >= 10 and len(ipv6resolvedlist) >= 10 else False
        Assertion.assert_equal(flag, True, "ERR: check wildcard fqdn ao resolved ips on gui failed")

    @repeat_method(3)
    def test_08_check_tcp_dns_query_response_packets_with_30_resolved_ipv4_hosts_and_30_resolved_ipv6_hosts_for_second_time(self):
        flag = False
        hostsipv4list = []
        hostsipv6list = []
        # generate domain name's IPs on dns server: ipv4:12.12.1.30--12.12.1.59, ipv6:2001:20::30 to 2001:20::59
        for i in range(30, 60):
            hostsipv4list.append(f'12.12.1.{i}')
            hostsipv6list.append(f'2001:20::{i}')
        logger.info(f'hostsipv4list is:{hostsipv4list},hostsipv6list is:{hostsipv6list}')
        res1 = addressobjectsapi.purge_ao_by_name(name=Parameter.FQDN_Mixed_Hostname, version='fqdn')
        start_capture_and_clear_packets(packetmonitorapi)
        res2 = addressobjectsapi.resolve_ao_by_name(name=Parameter.FQDN_Mixed_Hostname, version='fqdn')
        time.sleep(10)
        logger.info(f'res1 is {res1},res2 is:{res2}')
        if res1 and res2:
            # Test resolve FQDN for the second time,then will get resolved ip from local cache
            (answeripv4list, answeripv6list) = check_dns_udp_packets(packetmonitorapi, PC1_Login, Parameter.FQDN_Mixed_Hostname,
                                                                     type='mixed')
            logger.info(f'answeripv4list is:{answeripv4list},answeripv6list is:{answeripv6list}')
            if (not answeripv4list) and (not answeripv6list):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: check tcp response with 30 ipv4 and 30 ipv6 resolved ips for the second time")

    def test_09_disable_fqdn_over_tcp_dns_for_dns_settings_on_dut(self):
        dns_update = {
            "dns": {
                "fqdn_over_tcp_dns": False,
            }
        }
        rc = dnssettingsapi.set_dns(**dns_update)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_10_delete_fqdn_ao(self):
        res = addressobjectsapi.del_ao_by_name(name=Parameter.FQDN_Mixed_Hostname, version='fqdn')
        Assertion.assert_equal(res, True, "ERR: delete fqdn ao failed")


class TestTC05_Test_option_refresh_sub_domains_of_wildcard_fqdn_address_objects_in_diag_page(Test):
    uuid = "SOSAIOT-TC-56568"
    description = show_testcase_info(TESTPLAN, 'tc05', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc05')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_enable_option_refresh_sub_domains_of_wildcard_fqdn_address_objects_in_diag_page(self):
        rc = diagapi.config_raw_api(**{'stream': 'refreshFqdnSubDomains=on'})
        Assertion.assert_equal(rc, True, "ERR: enable option 'Refresh sub-domains of wildcard FQDN address objects' "
                                         "in diag page failed")

    def test_03_change_mixed_fqdn_ao_with_custom_ttl(self):
        edit_fqdn_ao_dict = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Wildcard_Hostname,
            "zone": "WAN",
            "value": Parameter.FQDN_Wildcard_Hostname,
            "dns_ttl": 120
        }
        res = addressobjectsapi.edit_addressobject_by_name(Parameter.FQDN_Wildcard_Hostname, **edit_fqdn_ao_dict)
        Assertion.assert_equal(res, True, "ERR: edit fqdn ao used by others failed")

    def test_04_check_fqdn_ttl_refresh_when_enable_refresh_option(self):
        flag = False
        addressobjectsapi.purge_ao_by_name(name=Parameter.FQDN_Wildcard_Hostname, version='fqdn')
        nslookupdict = {
            'version': 'ipv6',
            'type': 'system',
            'domain_name': Parameter.FQDN_Hostname_one_ipv6,
        }
        diagnosticapi.diag_dns_lookup_name_by_api(**nslookupdict)
        nsloutput = diagnosticapi.get_name_lookup_Result()
        logger.info(f'nsloutput is:{nsloutput}')
        time.sleep(5)
        fqdnoutput1 = addressobjectsapi.get_DAO_info(Parameter.FQDN_Wildcard_Hostname)
        logger.info(f'fqdnoutput1 is:{fqdnoutput1}')
        if fqdnoutput1["data"]["daoInfo"] != 'UNRESOLVED':
            getttlvalue1 = re.search(r'(?<=TTL=)\d+', str(fqdnoutput1), re.I)
            logger.info(f'getttlvalue1 is:{getttlvalue1}')
            if getttlvalue1:
                ttlvalue1 = getttlvalue1.group()
                logger.info(f'ttlvalue1 is:{ttlvalue1}')
                if 100 < int(ttlvalue1) < 120:
                    time.sleep(160)
                    fqdnoutput2 = addressobjectsapi.get_DAO_info(Parameter.FQDN_Wildcard_Hostname)
                    logger.info(f'output2 is:{fqdnoutput2}')
                    getttlvalue2 = re.search(r'(?<=TTL=)\d+', str(fqdnoutput2), re.I)
                    logger.info(f'getttlvalue2 is:{getttlvalue2}')
                    if getttlvalue2:
                        ttlvalue2 = getttlvalue2.group()
                        if 0 < int(ttlvalue2) <= 120:
                            flag = True
                            logger.info('fqdn ao fresh after TTL expired and offset time elapsed successfully')
        else:
            logger.error("error:didn't get resolved ip")
        Assertion.assert_equal(flag, True, "ERR: check fqdn ao refresh after ttp expired failed")

    def test_05_disable_option_refresh_sub_domains_of_wildcard_fqdn_address_objects_in_diag_page(self):
        rc = diagapi.config_raw_api(**{'stream': 'refreshFqdnSubDomains='})
        Assertion.assert_equal(rc, True, "ERR: disable option 'Refresh sub-domains of wildcard FQDN address objects' "
                                         "in diag page failed")

    def test_06_check_fqdn_resolved_ip_deleted_when_disable_refresh_option(self):
        flag = False
        addressobjectsapi.purge_ao_by_name(name=Parameter.FQDN_Wildcard_Hostname, version='fqdn')
        nslookupdict = {
            'version': 'ipv6',
            'type': 'system',
            'domain_name': Parameter.FQDN_Hostname_one_ipv6,
        }
        diagnosticapi.diag_dns_lookup_name_by_api(**nslookupdict)
        nsloutput = diagnosticapi.get_name_lookup_Result()
        logger.info(f'nsloutput is:{nsloutput}')
        time.sleep(5)
        fqdnoutput1 = addressobjectsapi.get_DAO_info(Parameter.FQDN_Wildcard_Hostname)
        logger.info(f'fqdnoutput1 is:{fqdnoutput1}')
        if fqdnoutput1["data"]["daoInfo"] != 'UNRESOLVED':
            getttlvalue1 = re.search(r'(?<=TTL=)\d+', str(fqdnoutput1), re.I)
            logger.info(f'getttlvalue1 is:{getttlvalue1}')
            if getttlvalue1:
                ttlvalue1 = getttlvalue1.group()
                logger.info(f'ttlvalue1 is:{ttlvalue1}')
                if 100 < int(ttlvalue1) < 120:
                    time.sleep(160)
                    fqdnoutput2 = addressobjectsapi.get_DAO_info(Parameter.FQDN_Wildcard_Hostname)
                    logger.info(f'output2 is:{fqdnoutput2}')
                    flag = True if 'UNRESOLVED' in str(fqdnoutput2) else False
        else:
            logger.error("error:didn't get resolved ip")
        Assertion.assert_equal(flag, True, "ERR: check fqdn ao resolved ip deleted after ttp expired failed")


# Excepted: the FQDN AO can be resolved with increased host ip
class TestTC07_Function_test_when_the_resolved_ipv6_addresses_increased(Test):
    uuid = "SOSAIOT-TC-56569"
    description = show_testcase_info(TESTPLAN, 'tc07', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc07')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_ipv6_fqdn_ao(self):
        probe_object_dict = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Hostname_four_ipv6,
            "zone": "WAN",
            "value": Parameter.FQDN_Hostname_four_ipv6
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add FQDN address object failed")

    def test_03_check_resolved_ipv6_address(self):
        time.sleep(15)
        output = addressobjectsapi.get_DAO_info(Parameter.FQDN_Hostname_four_ipv6)
        logger.info(f'output is:{output}')
        hostlist = ['Host: 2001:20::130', 'Host: 2001:20::131', 'Host: 2001:20::132', 'Host: 2001:20::133',
                    'Host: 2001:20::134']
        checkres = [i in str(output) for i in hostlist]
        logger.info(f'resolved ip address check result: {checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check resolved ip address failed.")

    def test_04_add_another_host_ip_to_the_domain_name_on_dns_server(self):
        commands = [f'echo "{Parameter.FQDN_Hostname_four_ipv6}. IN      AAAA    2001:20::135" >> /var/named/baidu.com.zone',
                    'cat /var/named/baidu.com.zone',
                    'systemctl restart named',
                    'systemctl status named',
                    ]
        output = PC3_Login.send_commands(commands)
        logger.info(f'*******************output is :{output}')
        flag = True if f'{Parameter.FQDN_Hostname_four_ipv6}. IN      AAAA    2001:20::135' in str(output) and 'running' in str(
            output) else False
        Assertion.assert_equal(flag, True, "ERR: add another host on dns server failed.")

    def test_05_check_resolved_ipv6_address_if_increased(self):
        flag = False
        res1 = addressobjectsapi.purge_ao_by_name(name=Parameter.FQDN_Hostname_four_ipv6, version='fqdn')
        time.sleep(10)
        res2 = addressobjectsapi.resolve_ao_by_name(name=Parameter.FQDN_Hostname_four_ipv6, version='fqdn')
        time.sleep(10)
        if res1 and res2:
            output = addressobjectsapi.get_DAO_info(Parameter.FQDN_Hostname_four_ipv6)
            logger.info(f'output is:{output}')
            if "2001:20::135" in str(output):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: check resolved ip address increased failed.")


# Excepted: the FQDN AO can be resolved with decreased host ip
class TestTC08_Function_test_when_the_resolved_ipv6_addresses_decreased(Test):
    uuid = "SOSAIOT-TC-56570"
    description = show_testcase_info(TESTPLAN, 'tc08', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc08')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_resolved_ipv6_address(self):
        res = addressobjectsapi.resolve_ao_by_name(name=Parameter.FQDN_Hostname_four_ipv6, version='fqdn')
        if res:
            time.sleep(15)
            output = addressobjectsapi.get_DAO_info(Parameter.FQDN_Hostname_four_ipv6)
            logger.info(f'output is:{output}')
            hostlist = ['Host: 2001:20::130', 'Host: 2001:20::131', 'Host: 2001:20::132', 'Host: 2001:20::133',
                        'Host: 2001:20::134', 'Host: 2001:20::135']
            checkres = [i in str(output) for i in hostlist]
            logger.info(f'resolved ip address check result: {checkres}')
            Assertion.assert_equal(all(checkres), True, "ERR: check resolved ip address failed.")

    def test_03_delete_one_host_ip_for_the_domain_name_on_dns_server(self):
        commands = [f'sed -i "/{Parameter.FQDN_Hostname_four_ipv6}. IN      AAAA    2001:20::135/d"  /var/named/baidu.com.zone',
                    'cat /var/named/baidu.com.zone',
                    'systemctl restart named',
                    'systemctl status named',
                    ]
        output = PC3_Login.send_commands(commands)
        logger.info(f'********************output is :{output}')
        flag = True if f'{Parameter.FQDN_Hostname_four_ipv6}. IN      AAAA    2001:20::135' not in str(output) and 'running' in str(
            output) else False
        Assertion.assert_equal(flag, True, "ERR: delete one host on dns server failed.")

    def test_04_check_resolved_ipv6_address_if_decreased(self):
        flag = False
        res1 = addressobjectsapi.purge_ao_by_name(name=Parameter.FQDN_Hostname_four_ipv6, version='fqdn')
        time.sleep(10)
        res2 = addressobjectsapi.resolve_ao_by_name(name=Parameter.FQDN_Hostname_four_ipv6, version='fqdn')
        time.sleep(10)
        if res1 and res2:
            output = addressobjectsapi.get_DAO_info(Parameter.FQDN_Hostname_four_ipv6)
            logger.info(f'output is:{output}')
            if "TTL" in str(output):
                if "2001:20::135" not in str(output):
                    flag = True
        Assertion.assert_equal(flag, True, "ERR: check resolved ip address decreased failed.")


# Excepted: option " Manually set DNS entries' TTL " work normally
class TestTC10_Test_option_manually_set_dns_entries_ttl_on_ipv6_fqdn_ao_page(Test):
    uuid = "SOSAIOT-TC-56571"
    description = show_testcase_info(TESTPLAN, 'tc10', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x1',
                'ether_types': 'ip',
                'ip_types': 'udp',
                'destination_ports': '53',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_03_add_ipv6_fqdn_ao(self):
        probe_object_dict = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Hostname_one_ipv6,
            "zone": "WAN",
            "value": Parameter.FQDN_Hostname_one_ipv6,
            "dns_ttl": 120
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add FQDN address object failed")

    def test_04_check_resend_dns_query_in_captured_packets(self):
        res = False
        time.sleep(2)
        output = addressobjectsapi.get_DAO_info(Parameter.FQDN_Hostname_one_ipv6)
        logger.info(f'**********output is:{output}')
        ttlvalue = get_ttl_from_fqdn_ao(str(output))
        logger.info(f'ttlvalue is:{ttlvalue}')
        if ttlvalue and 100 <= int(ttlvalue) < 120:
            start_capture_and_clear_packets(packetmonitorapi)
            time.sleep(160)
            checkdict = {
                "pclogin": PC1_Login,
                "domainname": Parameter.FQDN_Hostname_one_ipv6,
                "domaintype": "AAAA",
                "resolvedip": "2001:20::30"

            }
            (res, packet) = check_resend_dns_query_and_mark_ttl(packetmonitorapi, **checkdict)
            logger.info(f'res is:{res},packet is:{packet}')
        else:
            logger.info("didn't get ttlvalue")
        ParamCases.tc10result = res
        Assertion.assert_equal(res, True, "ERR: check captured packets failed")

    def test_05_check_ttl_value_for_fqdn_ao_after_send_dns_query(self):
        output = addressobjectsapi.get_DAO_info(Parameter.FQDN_Hostname_one_ipv6)
        logger.info(f'**********output is:{output}')
        ttlvalue = get_ttl_from_fqdn_ao(str(output))
        logger.info(f'ttlvalue is:{ttlvalue}')
        flag = True if int(ttlvalue) >= 70 else False
        Assertion.assert_equal(flag, True, "ERR: mark ttl value failed")


# Excepted: Verify when one of the binding host's TTL has expired, SonicOS will resend dns qurey.
class TestTC12_Test_host_ttl_has_expired(Test):
    uuid = "SOSAIOT-TC-56572"
    description = show_testcase_info(TESTPLAN, 'tc12', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc12')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test02_check_resend_dns_query_after_ttl_expired(self):
        Assertion.assert_equal(ParamCases.tc10result, True, "ERR: check resend dns query after TTL expired failed")


# Excepted: "Added host entry to dynamic address object" is shown in log
class TestTC18_Log_support_added_host_entry_to_dynamic_address_object(Test):
    uuid = "SOSAIOT-TC-56573"
    description = show_testcase_info(TESTPLAN, 'tc18', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_change_central_log_level(self):
        editdict = {
            "log": {
                "group": [
                    {
                        "id": 70,
                        "name": "Dynamic Address Objects",
                        "log_monitor": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                    }
                ]
            }
        }
        logsetres = logcategapi.logging_level(level='debug')
        logsetres &= logcategapi.edit_log_category_groups_by_id(70, **editdict)
        Assertion.assert_equal(logsetres, True, "ERR: change central log failed.")

    def test_03_check_log_event(self):
        flag = False
        res1 = addressobjectsapi.purge_ao_by_name(name=Parameter.FQDN_Hostname_one_ipv6, version='fqdn')
        time.sleep(10)
        logmonitorapi.clear_log()
        time.sleep(5)
        res2 = addressobjectsapi.resolve_ao_by_name(name=Parameter.FQDN_Hostname_one_ipv6, version='fqdn')
        logger.info(f'res1 is:{res1},res2 is:{res2}')
        if res1 and res2:
            time.sleep(10)
            getlogres = logmonitorapi.get_log(id=911)
            logger.info(f'getlogres is:{getlogres}')
            if "Added host entry to dynamic address object" in str(getlogres):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: change central log failed.")


# Excepted: IPv6_FQDN_ACL: Deny ACL (LAN-WAN),the ping should fail
class TestTC25_ipv6_fqdn_acl_deny_acl_lan_to_wan(Test):
    uuid = "SOSAIOT-TC-56574"
    description = show_testcase_info(TESTPLAN, 'tc25', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc25')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_edit_ipv6_fqdn_ao_without_set_ttl(self):
        edit_fqdn_ao_dict = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Hostname_one_ipv6,
            "zone": "WAN",
            "value": Parameter.FQDN_Hostname_one_ipv6
        }
        rc = addressobjectsapi.edit_addressobject_by_name(Parameter.FQDN_Hostname_one_ipv6, **edit_fqdn_ao_dict)
        Assertion.assert_equal(rc, True, "ERR: edit FQDN address object failed")

    def test_03_add_ipv6_access_rule_from_x2_to_wan_deny_and_verify_traffic(self):
        flag = True
        accessrule_opt = {
            'option': 'add',
            'name': Parameter.IPv6_Accessrule_Name,
            'from': 'X2',
            'to': 'WAN',
            'destination_addr': Parameter.FQDN_Hostname_one_ipv6,
            'action': 'deny'
        }
        res = accessrule.config_ipv6_access_rule(**accessrule_opt)
        if res:
            addressobjectsapi.purge_ao_by_name(name=Parameter.FQDN_Hostname_one_ipv6, version='fqdn')
            time.sleep(10)
            addressobjectsapi.resolve_ao_by_name(name=Parameter.FQDN_Hostname_one_ipv6, version='fqdn')
            time.sleep(10)
            logger.info('start to ping resolved ip on pc2')
            output = PC2_Login.send_command(f'ping -6 {PC3_ETH1_IPv6} -c 5')
            flag = True if '100% packet loss' in str(output) else False

        else:
            logger.info('add ipv6 accessrule failed')
        ParamCases.tc25result.append(flag)
        Assertion.assert_equal(flag, True, "ERR: Add access rules and verify traffic Failed!")

    def test_04_edit_ipv6_access_rule_from_x2_to_wan_allow_and_verify_traffic(self):
        flag = False
        edit_acl_dict = {
            "name": Parameter.IPv6_Accessrule_Name,
            "action": "allow",
            "from": "X2",
            "to": "WAN",
            'destination_addr': Parameter.FQDN_Hostname_one_ipv6,
        }
        res = accessrule.modify_ipv6_access_rule(**edit_acl_dict)
        if res:
            output = PC2_Login.send_command(f'ping -6 {PC3_ETH1_IPv6} -c 5')
            flag = True if '100% packet loss' not in str(output) else False
        else:
            logger.info('edit ipv6 accessrule failed')
        ParamCases.tc25result.append(flag)
        Assertion.assert_equal(flag, True, "ERR: allowed lan to wan,verify ping traffic Failed!")

    def test_05_change_x2_to_dmz_zone(self):
        del_rule = {'name': Parameter.IPv6_Accessrule_Name, 'from': 'X2', 'to': 'WAN'}
        delres = accessrule.delete_ipv6_accessrule(**del_rule)
        logger.info(f'delres is:{delres}')
        edit_x2_dict = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**edit_x2_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to dmz zone failed")

    def test_06_check_dmz_to_wan_traffic_when_access_rule_deny(self):
        self.test_03_add_ipv6_access_rule_from_x2_to_wan_deny_and_verify_traffic()

    def test_07_check_dmz_to_wan_traffic_when_access_rule_allow(self):
        self.test_04_edit_ipv6_access_rule_from_x2_to_wan_allow_and_verify_traffic()

    def test_08_creat_custom_zone(self):
        custom_zone_dict = {
            "zones": [
                {
                    "name": "custom_zone",
                    "security_type": "trusted",
                    "interface_trust": True,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "gateway_anti_virus": True,
                    "intrusion_prevention": False
                }
            ]
        }
        res = zoneobjectsapi.add_zone_object(**custom_zone_dict)
        Assertion.assert_equal(res, True, "ERR:add custom zone failed")

    def test_09_change_x2_to_custom_zone(self):
        del_rule = {'name': Parameter.IPv6_Accessrule_Name, 'from': 'X2', 'to': 'WAN'}
        delres = accessrule.delete_ipv6_accessrule(**del_rule)
        logger.info(f'delres is:{delres}')
        edit_x2_dict = {
            'if': 'X2',
            'zone': 'custom_zone',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**edit_x2_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to custom zone failed")

    def test_10_check_custom_zone_to_wan_traffic_when_access_rule_deny(self):
        self.test_03_add_ipv6_access_rule_from_x2_to_wan_deny_and_verify_traffic()

    def test_11_check_dmz_to_wan_traffic_when_access_rule_allow(self):
        self.test_04_edit_ipv6_access_rule_from_x2_to_wan_allow_and_verify_traffic()


# Excepted: IPv6_FQDN_ACL: Allow ACL (LAN-WAN),the ping should success
class TestTC26_ipv6_fqdn_acl_allow_acl_lan_to_wan(Test):
    uuid = "SOSAIOT-TC-56575"
    description = show_testcase_info(TESTPLAN, 'tc26', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc26')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_test_allow_ipv6_fqdn_acl(self):
        logger.info(f'ParamCases.tc25result is:{ParamCases.tc25result}')
        Assertion.assert_equal(all(ParamCases.tc25result), True, "ERR: show test case info failed")


# Excepted: Add a FQDN based IPv6 Network monitor policy with newly created FQDN Aos
class TestTC28_Add_fqdn_based_ipv6_network_monitor_policy_with_newly_created_fqdn_aos(Test):
    uuid = "SOSAIOT-TC-56576"
    description = show_testcase_info(TESTPLAN, 'tc28', description=True)['title']
    probename = 'ipv6pingprobe'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc28')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_ipv6_nm_policy_with_fqdn_probe_target(self):
        ipv6_nm_dict = copy.deepcopy(ipv6_nm_ping_non_explicit_with_fqdn_target_dict)
        ipv6_nm_dict["network_monitors"][0]["policy"]["ipv6"]["probe"]["target"]["name"] = Parameter.FQDN_Hostname_one_ipv6
        res = networkmonitorapi.add_network_monitor(**ipv6_nm_dict)
        Assertion.assert_equal(res, True, "ERR: add network monitor policy with fqdn_probe failed")

    def test_03_check_ipv6_nm_policy_status(self):
        time.sleep(20)
        output = networkmonitorapi.get_network_monitor_status_by_name(self.probename)
        res = True if 'green' in str(output) else False
        ParamCases.tc28result = res
        Assertion.assert_equal(res, True, "ERR: check ipv6 network monitor policy up failed")

    def test_04_delete_ipv6_nm_policy(self):
        res = networkmonitorapi.del_network_monitor(self.probename, version=6)
        Assertion.assert_equal(res, True, "ERR: delete ipv6 nm policy failed")


# Excepted: Add a FQDN based IPv6 Network monitor policy and choose version IPv6 and make sure it works as expected.
class TestTC30_Add_a_FQDN_based_ipv6_network_monitor_policy(Test):
    uuid = "SOSAIOT-TC-56577"
    description = show_testcase_info(TESTPLAN, 'tc30', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc30')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_Add_a_FQDN_based_ipv6_network_monitor_policy(self):
        Assertion.assert_equal(ParamCases.tc28result, True,
                               "ERR: Add a FQDN based IPv6 Network monitor policy and choose version IPv6 failed")


# Excepted: edit/delete IPv6 FQDN  AO when it's used by other policy
class TestTC50_edit_delete_ipv6_fqdn_ao(Test):
    uuid = "SOSAIOT-TC-56581"
    description = show_testcase_info(TESTPLAN, 'tc50', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc50')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_fqdn_ao_can_be_edit_when_it_is_used(self):
        edit_fqdn_ao_dict = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Hostname_one_ipv6,
            "zone": "WAN",
            "value": Parameter.FQDN_Hostname_one_ipv6,
            "dns_ttl": 150
        }
        res = addressobjectsapi.edit_addressobject_by_name(Parameter.FQDN_Hostname_one_ipv6, **edit_fqdn_ao_dict)
        Assertion.assert_equal(res, True, "ERR: edit fqdn ao used by others failed")

    def test_03_check_fqdn_ao_can_be_deleted_when_it_is_used(self):
        (res, msg) = addressobjectsapi.del_ao_by_name(name=Parameter.FQDN_Hostname_one_ipv6, version='fqdn', msg=True)
        logger.info(f'res is:{res},msg is:{msg}')
        Assertion.assert_regular(str(msg), 'Object is in use by rule', "ERR: delete fqdn ao used by others failed")

    def test_04_delete_access_rule_with_fqdn_ao_configured(self):
        del_rule = {'name': Parameter.IPv6_Accessrule_Name, 'from': 'X2', 'to': 'WAN'}
        res = accessrule.delete_ipv6_accessrule(**del_rule)
        Assertion.assert_equal(res, True, "ERR: delete access rule with fqdn ao configured failed")

    def test_05_check_fqdn_ao_can_be_edit_when_it_is_not_used(self):
        edit_fqdn_ao_dict = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Hostname_one_ipv6,
            "zone": "WAN",
            "value": Parameter.FQDN_Hostname_one_ipv6,
        }
        res = addressobjectsapi.edit_addressobject_by_name(Parameter.FQDN_Hostname_one_ipv6, **edit_fqdn_ao_dict)
        Assertion.assert_equal(res, True, "ERR: edit fqdn ao used by others failed")

    def test_06_check_fqdn_ao_can_be_deleted_when_it_is_not_used(self):
        res = addressobjectsapi.del_ao_by_name(name=Parameter.FQDN_Hostname_one_ipv6, version='fqdn')
        Assertion.assert_equal(res, True, "ERR: delete fqdn ao that is not used by others failed")


# Excepted: add ipv6 accessrule,ipv6 route policy,ipv6 network policy,then download tsr
class TestTC49_tsr_test(Test):
    uuid = "SOSAIOT-TC-56580"
    description = show_testcase_info(TESTPLAN, 'tc49', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc49')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_ipv6_fqdn_aos_and_ao_group(self):
        add_fqdn_ao_dict1 = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Hostname_one_ipv6,
            "zone": "WAN",
            "value": Parameter.FQDN_Hostname_one_ipv6,
        }
        add_fqdn_ao_dict2 = {
            "object_type": "fqdn",
            "name": Parameter.FQDN_Hostname_one_ipv6_not_pc3,
            "zone": "WAN",
            "value": Parameter.FQDN_Hostname_one_ipv6_not_pc3,
        }
        add_fqdn_ao_group_dict = {
            "address_groups": [
                {
                    "ipv6": {
                        "address_object": {
                            "fqdn": [
                                {
                                    "name": Parameter.FQDN_Hostname_one_ipv6
                                },
                                {
                                    "name": Parameter.FQDN_Hostname_one_ipv6_not_pc3
                                },
                            ]
                        },
                        "name": "testgroup"
                    }
                }
            ]
        }
        res1 = addressobjectsapi.config_addressobject(**add_fqdn_ao_dict1)
        res2 = addressobjectsapi.config_addressobject(**add_fqdn_ao_dict2)
        res3 = addressobjectgroupapi.add_addressgroup(**add_fqdn_ao_group_dict)
        Assertion.assert_equal(res1 & res2 & res3, True, "ERR: add FQDN address objects/group failed")

    def test_03_add_ipv6_access_rule_from_x2_to_wan_allow(self):
        accessrule_opt = {
            'option': 'add',
            'name': Parameter.IPv6_Accessrule_Name,
            'from': 'X2',
            'to': 'WAN',
            'source_addr_any': True,
            'destination_addr': Parameter.FQDN_Hostname_one_ipv6,
            'action': 'allow'
        }
        out = accessrule.config_ipv6_access_rule(**accessrule_opt)
        Assertion.assert_equal(out, True, "ERR: Add access rules Failed!")

    def test_04_add_ipv6_route_policy_with_probe_selected(self):
        ipv6_route_policy_with_probe_dict = {
            "route_policies": [
                {
                    "ipv6": {
                        "name": Parameter.IPv6_Routepolicy_Name,
                        "comment": "",
                        "interface": "X1",
                        "metric": 20,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": "X1 IPv6 Default Gateway"
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": Parameter.FQDN_Hostname_one_ipv6_not_pc3
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        res = routepolicyapi.add_route_policy(**ipv6_route_policy_with_probe_dict)
        Assertion.assert_equal(res, True, "ERR: add route policy with probe and check its status failed")

    def test_05_check_new_added_ipv6_routing_with_fqdn_ao_in_tsr(self):
        flag = False
        getrouting = diagnosticapi.get_tsr_route_policy_part(func='Network : Routing')
        logger.info(f'getrouting is:{getrouting}')
        route_sp = getrouting.split('\n\n\n')
        for eachroute in route_sp:
            checklist = [f'name: {Parameter.IPv6_Routepolicy_Name}', f'destinationObject: {Parameter.FQDN_Hostname_one_ipv6_not_pc3}']
            checkres = [i in eachroute for i in checklist]
            logger.info(f'checkres is :{checkres}')
            if all(checkres):
                flag = True
                logger.info(f'eachroute is :{eachroute}')
                break
        Assertion.assert_equal(flag, True, "ERR: check new added ipv6 routing with fqdn ao in tsr failed")

    def test_06_check_new_added_access_rule_with_fqdn_ao_in_tsr(self):
        flag = False
        getaccessrule = diagnosticapi.get_tsr_accessrule_part()
        logger.info(f'getaccessrule is:{getaccessrule}')
        accessrule_sp = getaccessrule.split('Rule ')
        # logger.info(accessrule_sp)
        for eachaccessrule in accessrule_sp:
            logger.info(f'eachaccessrule is:{eachaccessrule}')
            checklist = [f"Policy Name:               {Parameter.IPv6_Accessrule_Name}",
                         f"IP: Any -> {Parameter.FQDN_Hostname_one_ipv6}"
                         ]
            checkres = [i in eachaccessrule for i in checklist]
            logger.info(f'checkres is :{checkres}')
            if all(checkres):
                logger.info(f'matching accessrule is:{eachaccessrule}')
                flag = True
                logger.info(f'eachaccessrule is :{eachaccessrule}')
                break
        Assertion.assert_equal(flag, True, "ERR: check new added ipv6 accessrule with fqdn ao in tsr failed")

    def test_07_check_fqdn_aos_in_tsr(self):
        flag = True
        fqdnaodict = [{Parameter.FQDN_Hostname_one_ipv6: '2001:20::30'},
                      {Parameter.FQDN_Hostname_one_ipv6_not_pc3: '2001:20::31'}]
        for fqdnao in fqdnaodict:
            output = diagnosticapi.get_tsr_part('Network', lab1='Address Objects')
            fqdnaoname = list(fqdnao.keys())[0]
            logger.info(f'fqdnaoname is:{fqdnaoname}')
            pattern = '-------' + fqdnaoname + '-------\n(.*?)Time Created'
            aopartres = re.search(pattern, output, re.S)
            if aopartres:
                aopart = aopartres.group(0)
                logger.info(f'{fqdnao.keys()} TSR Part is found:\n{aopart}\n')
                hostsvalue = re.search(r'[A-Za-z0-9]{1,4}(:[A-Za-z0-9]{1,4}){7}', aopart, re.I | re.S | re.M)
                logger.info(f'hostsvalue is:{hostsvalue}')
                if hostsvalue:
                    resolvedip = hostsvalue.group()
                    logger.info(f'resolvedip is:{resolvedip}')
                    resolvedip_int = ipaddress.IPv6Address(resolvedip)
                    logger.info(f'resolvedip_int is:{resolvedip_int}')
                    flag = True if resolvedip_int == ipaddress.IPv6Address(list(fqdnao.values())[0]) else False
        Assertion.assert_equal(flag, True, "ERR: check new added ipv6 accessrule with fqdn ao in tsr failed")


# Excepted:  Restart test
class TestTC48_Restart_test(Test):
    uuid = "SOSAIOT-TC-56579"
    description = show_testcase_info(TESTPLAN, 'tc48', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc48')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_restart_dut(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Restart DUT failed")

    @repeat_method(3,5)
    def test_03_check_ipv6_fqdn_aos_and_groups_settings_and_resolved_ips(self):
        flag = False
        groupchecklist = ['"name": "testgroup"', f'"name": "{Parameter.FQDN_Hostname_one_ipv6_not_pc3}"', f'"name": "{Parameter.FQDN_Hostname_one_ipv6}"']
        output1 = addressobjectsapi.get_DAO_info(Parameter.FQDN_Hostname_one_ipv6)
        logger.info(f'output1 is:{output1}')
        output2 = addressobjectsapi.get_DAO_info(Parameter.FQDN_Hostname_one_ipv6_not_pc3)
        logger.info(f'output2 is:{output2}')
        output3 = addressobjectgroupapi.get_addressgroup_by_name('testgroup', version='v6')
        logger.info(f'output3 is:{json.dumps(output3)}')
        groupcheckres = [i in json.dumps(output3) for i in groupchecklist]
        logger.info(f'groupcheckres is :{groupcheckres}')
        if 'Host: 2001:20::30' in str(output1) and 'Host: 2001:20::31' in str(output2) and all(groupcheckres):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check resolved ipv6 address failed")

    def test_04_check_ipv6accessrule_settings_and_functions(self):
        flag = False
        accessrule_opt = {
            'from': 'X2',
            'to': 'WAN',
            'name': Parameter.IPv6_Accessrule_Name
        }
        output = accessrule.get_ipv6_accessrule(**accessrule_opt)
        logger.info(f'output is:{output}')
        if f"'name': '{Parameter.IPv6_Accessrule_Name}'" in str(output) and f"'name': '{Parameter.FQDN_Hostname_one_ipv6}'" in str(output):
            logger.info('ipv6accessrule is displayed correctly after restart,start to ping resolved dest ip')
            pingoutput = PC2_Login.send_command(f'ping -6 {PC3_ETH1_IPv6} -c 5')
            flag = True if '0% packet loss' in str(pingoutput) else False
        Assertion.assert_equal(flag, True, "ERR: check ipv6 accessrule settings and ping resovled ipv6 address Failed!")

    def test_05_check_ipv6_routing_settings_and_functions(self):
        getoutput = routepolicyapi.get_route_policy_by_name(Parameter.IPv6_Routepolicy_Name, version='v6')
        logger.info(f'getoutput is:{getoutput}')
        flag = True if f"'name': '{Parameter.FQDN_Hostname_one_ipv6_not_pc3}'" in str(getoutput) else False
        Assertion.assert_equal(flag, True, "ERR: check added ipv6 route policy failed")


# Excepted:  Prefs export and import test
class TestTC47_Prefs_export_and_import_test(Test):
    uuid = "SOSAIOT-TC-56578"
    description = show_testcase_info(TESTPLAN, 'tc47', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc47')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_export_exp_file(self):
        logger.info('=> export exp file.')
        res = settingapi.export_setting_exp('/tmp/jlian_ipv6_pbr_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_03_restore_fw(self):
        logger.info('=> restore DUT.')
        res = settingapi.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_04_import_exp_file(self):
        logger.info('=> import exp file.')
        res = settingapi.import_setting_exp(
            filepath='/tmp/jlian_ipv6_pbr_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_05_check_ipv6_fqdn_aos_and_groups_settings_and_resolved_ips_after_restore_and_import_prefs(self):
        TestTC48_Restart_test().test_03_check_ipv6_fqdn_aos_and_groups_settings_and_resolved_ips()

    def test_06_check_ipv6accessrule_settings_and_functions_after_restore_and_import_prefs(self):
        TestTC48_Restart_test().test_04_check_ipv6accessrule_settings_and_functions()

    def test_07_check_ipv6_routing_settings_and_functions_after_restore_and_import_prefs(self):
        TestTC48_Restart_test().test_05_check_ipv6_routing_settings_and_functions()

    def test_08_delete_ipv6_access_and_ipv6_routepolicy_and_one_ipv6_fqdn_ao(self):
        accessrule_opt = {
            'name': Parameter.IPv6_Accessrule_Name,
            'from': 'X2',
            'to': 'WAN',
        }
        res1 = routepolicyapi.del_route_policy_by_name(Parameter.IPv6_Routepolicy_Name, version='ipv6')
        res2 = accessrule.delete_ipv6_accessrule(**accessrule_opt)
        res3 = addressobjectgroupapi.del_addressgroup('testgroup', version='v6')
        Assertion.assert_equal(res1 & res2 & res3, True, "ERR: delete ipv6 accessrule, ipv6 routepolicy and ipv6 fqdn "
                                                         "ao group failed")

    def test_09_import_exp_file(self):
        self.test_04_import_exp_file()

    def test_10_check_ipv6_fqdn_aos_and_groups_settings_and_resolved_ips_after_delete_settings_and_import_prefs(self):
        TestTC48_Restart_test().test_03_check_ipv6_fqdn_aos_and_groups_settings_and_resolved_ips()

    def test_11_check_ipv6accessrule_settings_and_functions_after_delete_settings_and_import_prefs(self):
        TestTC48_Restart_test().test_04_check_ipv6accessrule_settings_and_functions()

    def test_12_check_ipv6_routing_settings_and_functions_after_delete_settings_and_import_prefs(self):
        TestTC48_Restart_test().test_05_check_ipv6_routing_settings_and_functions()
