from definition.settings import *
from definition.utils import *


# Verify the response is received in LAN client PC
class TestDNS_01(Test):
    uuid = "SOSAIOT-TC-51381"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'destination_ips': PC2_ETH1_IP,
                'interfaces': 'x1,x2',
                'destination_ports': '53'
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_02_check_dns_query_and_response(self):
        pc_run_http_dict = {
            'type': 'cmd',  # ping, cmd, http,script
            'cmds': f'dig @{Parameter.DNS_SERVER_IP} ns.test.com',
        }
        (digres, packets) = fw_packet_monitor_run(packetmonitorapi, PC2_login, pc_run_http_dict)
        logger.info(f'http request result: {digres}')
        logger.info(f'packets captured on FW result: {packets}')
        (respres, packet) = dns_response_check(packets, src_ip=PC3_ETH1_IP, dst_ip=PC2_ETH1_IP)
        logger.info(f'check http response forwarded result: {packet}')
        Assertion.assert_equal(respres, True, "ERR: check query response failed.")


# check the fw dns server input.
class TestDNS_02(Test):
    uuid = "SOSAIOT-TC-51376"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_config_dns_server(self):
        invalid_ip_list = ['256.1.1.1', '1.256.1.1', '1.1.1.256', '1.1.@.1', '1.1.1.-9', 'Asfdfds']
        valid_ip_list = ['10.10.10.10']
        dns_dict = {"dns": {"server": {"static": {"primary": '256.1.1.1'}}}}
        tag = []
        for ip in invalid_ip_list:
            dns_dict['dns']['server']['static']['primary'] = ip
            (res, msgres) = dnssettingapi.set_dns(msg=True, **dns_dict)

            msg_lower = str(msgres).lower()
            if 'invalid ip address' in str(msg_lower):
                logger.info('check invalid ip successful.')
                tag.append(True)
            elif 'invalid input detected' in str(msg_lower):
                logger.info('check invalid input successful.')
                tag.append(True)
            else:
                logger.info(f'set invalid dns ip failed. msgres: {msg_lower}')
                tag.append(False)
        for ip in valid_ip_list:
            dns_dict['dns']['server']['static']['primary'] = ip
            (res, msgres) = dnssettingapi.set_dns(msg=True, **dns_dict)
            if res:
                tag.append(True)
            else:
                logger.info(f'set valid dns ip failed. msgres: {msgres}')
                tag.append(False)
        Assertion.assert_equal(all(tag), True, "ERR: Set server ip failed")


# check 3 dns server options use valid/fake dns ip
class TestDNS_04(Test):
    uuid = "SOSAIOT-TC-51377"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']
    jira = 'GEN7-38761'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_dns_server_1(self):
        rc = dnssettingapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS1 failed")

    def test_02_check_dns1_result(self):
        output = diagapi.diag_dns_name_lookup(cmd="nslookup ns.test.com")
        logger.info(f'nslookup ns.test.com result: {output}')
        res = True if Parameter.NS_TEST_COM_IP in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check DNS1 failed")

    def test_03_config_dns_server_2(self):
        dns_dict = {
            "dns": {
                "server": {
                    "inherit": False,
                    "static": {
                        "primary": Parameter.FAKE_DNS1,
                        "secondary": Parameter.VALID_DNS,
                        "tertiary": Parameter.FAKE_DNS2,
                    }
                }
            }
        }
        rc = dnssettingapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS2 failed")

    def test_04_check_dns2_result(self):
        output = diagapi.diag_dns_name_lookup(cmd="nslookup ns.test.com")
        logger.info(f'nslookup ns.test.com result: {output}')
        res = True if Parameter.NS_TEST_COM_IP in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check DNS2 failed")

    def test_05_config_dns_server_3(self):
        dns_dict = {
            "dns": {
                "server": {
                    "inherit": False,
                    "static": {
                        "primary": Parameter.FAKE_DNS1,
                        "secondary": Parameter.FAKE_DNS2,
                        "tertiary": Parameter.VALID_DNS,
                    }
                }
            }
        }
        rc = dnssettingapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS3 failed")

    def test_06_check_dns3_result(self):
        output = diagapi.diag_dns_name_lookup(cmd="nslookup ns.test.com")
        logger.info(f'nslookup ns.test.com result: {output}')
        res = True if Parameter.NS_TEST_COM_IP in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check DNS3 failed")


# check primary dns server option use valid dns server
class TestDNS_05(Test):
    uuid = "SOSAIOT-TC-51378"
    description = show_testcase_info(TESTPLAN, '5', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_dns_server_1(self):
        dns_dict = {
            "dns": {
                "server": {
                    "inherit": False,
                    "static": {
                        "primary": Parameter.DNS_SERVER_IP,
                    }
                }
            }
        }
        rc = dnssettingapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS1 failed")

    def test_02_check_primary_dns_query_and_response(self):
        pc_run_http_dict = {
            'type': 'cmd',  # ping, cmd, http,script
            'cmds': f'dig @{Parameter.DNS_SERVER_IP} ns.test.com',
        }
        (digres, packets) = fw_packet_monitor_run(packetmonitorapi, PC2_login, pc_run_http_dict)
        logger.info(f'http request result: {digres}')
        logger.info(f'packets captured on FW result: {packets}')
        (respres, packet) = dns_response_check(packets, src_ip=PC3_ETH1_IP, dst_ip=PC2_ETH1_IP)
        logger.info(f'check http response forwarded result: {packet}')
        Assertion.assert_equal(respres, True, "ERR: check query response failed.")


# check backup dns server option use valid dns server
class TestDNS_06(Test):
    uuid = "SOSAIOT-TC-51379"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_dns_server_ip(self):
        cmd = f'ifconfig eth1 {CaseParm.tc6backupip};service named restart;ifconfig eth1'
        output = PC3_login.send_command(cmd)
        logger.info(f'change dns server ip result: \n{output}')
        res = True if f'inet addr:{CaseParm.tc6backupip}' in output else False
        Assertion.assert_equal(res, True, "ERR: Set dns server ip failed")

    def test_02_check_backup_dns_response(self):
        pc_run_http_dict = {
            'type': 'cmd',  # ping, cmd, http,script
            'cmds': f'dig @{CaseParm.tc6backupip} ns.test.com',
        }
        (digres, packets) = fw_packet_monitor_run(packetmonitorapi, PC2_login, pc_run_http_dict)
        logger.info(f'http request result: {digres}')
        logger.info(f'packets captured on FW result: {packets}')
        (respres, packet) = dns_response_check(packets, src_ip=CaseParm.tc6backupip, dst_ip=PC2_ETH1_IP)
        logger.info(f'check http response forwarded result: {packet}')
        Assertion.assert_equal(respres, True, "ERR: check query response failed.")

    def test_03_init_dns_server_ip(self):
        cmd = f'ifconfig eth1 {Parameter.DNS_SERVER_IP};service named restart;ifconfig eth1'
        output = PC3_login.send_command(cmd)
        logger.info(f'change dns server ip result: \n{output}')
        res = True if f'inet addr:{Parameter.DNS_SERVER_IP}' in output else False
        Assertion.assert_equal(res, True, "ERR: Set dns server ip failed")


# restart fw check dns configure
class TestDNS_07(Test):
    uuid = "SOSAIOT-TC-51380"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_dns_server(self):
        dns_dict = {
            "dns": {
                "server": {
                    "inherit": False,
                    "static": {
                        "primary": Parameter.VALID_DNS,
                        "secondary": Parameter.FAKE_DNS1,
                        "tertiary": Parameter.FAKE_DNS2,
                    }
                }
            }
        }
        res = dnssettingapi.set_dns(**dns_dict)
        Assertion.assert_equal(res, True, "ERR: Set DNS failed")

    def test_02_Restart_DUT(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Restart DUT failed")

    @repeat_method(3)
    def test_03_Verify_DNS_config(self):
        time.sleep(10)
        output = dnssettingapi.get_dns()
        logger.info(f'dns setting info: {str(json.dumps(output))}')
        lists = [f'primary\': \'{PC3_ETH1_IP}', f'secondary\': \'{Parameter.FAKE_DNS1}', f'tertiary\': \'{Parameter.FAKE_DNS2}']
        logger.info(str(lists))
        # find multiple contents in a json string at the same time.
        res = all(x in str(output) for x in lists)
        Assertion.assert_equal(res, True, "ERR: Verify DNS config failed")


# check dnssec query from pc2 to pc3
class TestDNS_09(Test):
    uuid = "SOSAIOT-TC-51383"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_dns_server_inherit(self):
        dns_dict = {"dns": {"server": {"inherit": True}}}
        res = dnssettingapi.set_dns(**dns_dict)
        Assertion.assert_equal(res, True, "ERR: enable dns inherit failed")

    def test_03_check_dnssec_query_and_response(self):
        pc_run_http_dict = {
            'type': 'cmd',  # ping, cmd, http,script
            'packet': 'pcapng',
            'cmds': f'dig @{Parameter.DNS_SERVER_IP} +dnssec ns.test.com',
        }
        (digres, packets) = fw_packet_monitor_run(packetmonitorapi, PC2_login, pc_run_http_dict)
        logger.info(f'http request result: {digres}')
        digres = True if Parameter.NS_TEST_COM_IP in digres and 'RRSIG' in digres else False
        cmd = f'tshark -R "dns.qry.type and ip.src=={PC2_ETH1_IP} and ip.dst=={PC3_ETH1_IP}" -r /tmp/packet-c.pcapng -V -T text'
        pc1cmdres = PC1_login.send_command(cmd)
        logger.info(f'fitter qry packet result: {pc1cmdres}')
        captureres = True if 'Accepts DNSSEC security RRs' in pc1cmdres \
                             and 'UDP payload size: 4096' in pc1cmdres else False
        # TC11 response test
        cmd2 = f'tshark -R "dns.resp.type and ip.src=={PC3_ETH1_IP} and ip.dst=={PC2_ETH1_IP}" -r /tmp/packet-c.pcapng -V -T text'
        pc1cmdres2 = PC1_login.send_command(cmd2)
        logger.info(f'fitter resp packet result: {pc1cmdres2}')
        CaseParm.tc11testres = True if ('Type: NS' and 'Type: OPT' and
                                        'UDP payload size: 4096') in pc1cmdres else False
        logger.info(f'digres: {digres}, captureres: {captureres}')
        Assertion.assert_equal(digres & captureres, True, "ERR: check dns query failed.")


# check dnssec response from pc3 to pc2
class TestDNS_11(Test):
    uuid = "SOSAIOT-TC-51382"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_dnssec_response_check(self):
        res = CaseParm.tc11testres
        logger.info(f'get result from tc9: {res}')
        Assertion.assert_equal(res, True, "ERR: check dnssec response failed")


# check dnssec query/response after os dns config
class TestDNS_10(Test):
    uuid = "SOSAIOT-TC-51375"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_dnssec_query_and_response(self):
        pc_run_http_dict = {
            'type': 'ping',  # ping, cmd, http,script
            'packet': 'pcapng',
            'des': 'ns.test.com',
            'eth': 'eth1',
        }
        # modify the pc2 dns file
        cmd1 = f'echo "nameserver {Parameter.DNS_SERVER_IP}" > /etc/resolv.conf'
        PC2_login.send_command(cmd1)

        (digres, packets) = fw_packet_monitor_run(packetmonitorapi, PC2_login, pc_run_http_dict)
        logger.info(f'ping request result: {digres}')
        cmd = f'tshark -R "dns.qry.type and ip.src=={PC2_ETH1_IP} and ip.dst=={PC3_ETH1_IP}" -r /tmp/packet-c.pcapng -V -T text'
        pc1cmdres = PC1_login.send_command(cmd)
        logger.info(f'fitter query packet: {pc1cmdres}')
        qryres = True if 'ns.test.com: type A, class IN' in pc1cmdres else False
        logger.info(f'check query packet result: {qryres}')
        cmd2 = f'tshark -R "dns.resp.type and ip.src=={PC3_ETH1_IP} and ip.dst=={PC2_ETH1_IP}" -r /tmp/packet-c.pcapng -V -T text'
        pc1cmdres2 = PC1_login.send_command(cmd2)
        logger.info(f'fitter response packet: {pc1cmdres2}')
        lists = [f'ns.test.com: type A, class IN, addr {Parameter.NS_TEST_COM_IP}',
                 'test.com: type NS, class IN, ns ns.test.com']
        # find multiple contents in a json string at the same time.
        respres = all(x in pc1cmdres2 for x in lists)
        logger.info(f'check response packet result: {respres}')
        Assertion.assert_equal(qryres & respres, True, "ERR: check dns query for ping failed.")
