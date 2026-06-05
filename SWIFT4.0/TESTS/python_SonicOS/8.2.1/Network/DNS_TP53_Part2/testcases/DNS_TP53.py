from definition.settings import *
from definition.utils import *


class TestDNS_3830207(Test):
    uuid = "SOSAIOT-TC-51385"
    description = "Verify no unwanted DNS traffic can be captured"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3830207')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Config_X1_IPv4(self):
        x1_static_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ping': True,

        }
        res = interfacev4api.config_interface(**x1_static_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 IPv4 to static failed")

    def test_02_check_no_unwanted_dns_traffic_can_be_captured(self):
        res = {'1.1.1.1': False, '1.0.0.1': False, '169.254.0.1': False}
        pc_run_http_dict = {
            'type': 'cmd',  # ping, cmd, http,script
            'cmds': 'sleep 300',
        }
        (digres, packets) = fw_packet_monitor_run(packetmonitorapi, PC2_login, pc_run_http_dict)
        logger.info(f'http request result: {digres}')
        logger.info(f'packets captured on FW result: {packets}')
        check_list = ['1.1.1.1', '1.0.0.1', '169.254.0.1']
        for ip in check_list:
            if ip not in packets:
                res[ip] = True
        logger.info(f'check no unwanted dns traffic can be captured result: {res}')
        Assertion.assert_equal(all(res.values()), True, "ERR: check no unwanted dns traffic can be captured failed")


class TestDNS_3932088(Test):
    uuid = "SOSAIOT-TC-51387"
    description = "Verify the whole domain can be send when the domain's name over 128 bytes"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3932088')  
        Assertion.assert_equal(True, True, "ERR: show testcase info failed") 

    def test_01_check_whole_domain_can_be_send(self):
        res = False
        dns_lookup_dict = {
            'version': 'ipv4',
            'type': 'system',
            # if the input is longer than 128 char, it will be automated cut to smaller char to diag
            'domain_name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.1.1.1.1.nip.io',
            'ipv4-dns1': Params.G_DNS1
        }

        logger.info(dns_lookup_dict)
        (output, msg) = diagapi.diag_dns_lookup_name_by_api(**dns_lookup_dict)
        logger.info('waiting for 30s to check domain resolved...')
        time.sleep(30)
        try:
            output = diagapi.get_name_lookup_Result()
            searchres = re.search('(\d+.){3}\d+', output['data']['resolvedAddrs'])
            res = True if searchres else False
        except exception as e:
            logger.info(f'check name resolved failed: {repr(e)}')
        Assertion.assert_equal(res, True, "ERR: diag dns name lookup failed")


class TestDNS_3912897(Test):
    uuid = "SOSAIOT-TC-51386"
    description = "Verify DHCP INFORM will not be replied when there is no valid DHCP scope"
    dynamic_name = 'start/192.168.20.130/end/192.168.20.135'
    static_name = 'ip/192.168.20.100/mac/FA163ED025CC'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3912897')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Config_X2_IPv4(self):
        x2_static_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
        }
        res = interfacev4api.config_interface(**x2_static_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 IPv4 to static failed")

    def test_02_add_valid_static_entry_to_X2(self):
        static_entry = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "static": [
                            {
                                "ip": "192.168.20.120",
                                "mac": 'FA163ED025CC',
                                "enable": True,
                                "name": "test",
                                "lease_time": 2,
                                "default_gateway": "192.168.20.1",
                                "netmask": "255.255.255.0",
                            }
                        ]
                    }
                }
            }
        }
        ret = dhcpserverapi.add_dhcp_server_scope_static(**static_entry)
        Assertion.assert_equal(ret, True, "ERR: Add valid static entry failed")

    def test_03_add_dynamic_entries_to_X2(self):
        dynamic_entry = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "192.168.20.130",
                                "to": "192.168.20.135",
                                "enable": True,
                                "lease_time": 2,
                                "default_gateway": "192.168.20.1",
                                "netmask": "255.255.255.0",
                                "comment": "x2_dynamic_scope",
                            }
                        ]
                    }
                }
            }
        }
        time.sleep(5)
        output = dhcpserverapi.add_dhcp_server_scope_dynamic(**dynamic_entry)
        time.sleep(5)
        output1 = dhcpserverapi.get_dhcp_server_scope_dynamic()
        res = 'x2_dynamic_scope' in str(output1)
        Assertion.assert_equal(res, True, "ERR: Add dynamic entry failed")

    def test_04_pc2_can_get_ip_from_dhcp_server(self):
        DHCLIEN_LEASE_FILE = '/var/lib/dhclient/dhclient-eth1.leases'
        PC2_login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        releaseres = release_ip_in_pc(PC2_login, 'eth1')
        leaseres = get_ip_lease_in_pc(PC2_login, 'eth1')
        logger.info(f'release result: {releaseres}, get ip result: {leaseres}')
        Assertion.assert_equal(leaseres, True, "ERR: check ip for client failed")

    def test_05_disable_dhcp_server_dynamic_entries(self):
        logger.info('start run FW packet monitor...')
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        dynamic_entry = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "192.168.20.130",
                                "to": "192.168.20.135",
                                "enable": False,
                                "lease_time": 2,
                                "default_gateway": "192.168.20.1",
                                "netmask": "255.255.255.0",
                            }
                        ]
                    }
                }
            }
        }
        output = dhcpserverapi.edit_dhcp_server_scope_v4(scope = 'dynamic',p1 = '192.168.20.130', p2 = '192.168.20.135',**dynamic_entry)
        Assertion.assert_equal(output, True, "ERR: Disable dynamic entry failed")   

    def test_06_check_DHCP_ACK_in_packets(self):
        logger.info('waiting for 100s to check DHCP ACK...')
        time.sleep(100)
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'start packets on FW result: {stopres}')
        packetres = packetmonitorapi.export_captured_packets_pcapng()
        logger.info(f'packets captured on FW result: {packetres}')  
        cmd = f'tshark -R "ip.src=={Parameter.X2_IP}" -r /tmp/packet-c.pcapng -V -T text'
        pc1cmdres = PC1_login.send_command(cmd)
        logger.info(f'fitter qry packet result: {pc1cmdres}')
        res = True if 'DHCP: NAK' in pc1cmdres else False
        Assertion.assert_equal(res, True, "ERR: check DHCP NAK failed")

    def test_07_pc2_can_not_get_ip_from_dhcp_server(self):
        rang_ip_part = '192.168.20.13'
        cmds = [f'ifconfig eth1 0.0.0.0', 'timeout 20 killall dhclient']
        PC2_login.send_commands(cmds)
        output = PC2_login.send_command('timeout 20 dhclient -v eth1')
        time.sleep(10)
        logger.info(f'run dhcp client on pc: {output}')
        res = f'bound to {rang_ip_part}' not in output
        Assertion.assert_equal(res, True, "ERR: check ip for client failed")

    def test_08_init_pc2_fw_configure(self):
        output = PC2_login.send_commands([f'ifconfig eth1 {PC2_ETH1_IP}', 'ifconfig eth1'])
        logger.info(f'init pc2 configure result: {output}')
        res1 = f'inet {PC2_ETH1_IP}' in output
        res2 = dhcpserverapi.delete_dhcp_server_scope_v4(scope='static', p1='192.168.20.120', p2='FA163ED025CC'.lower())
        res3 = dhcpserverapi.delete_dhcp_server_scope_v4(scope='dynamic', p1='192.168.20.130', p2='192.168.20.135')
        logger.info(f'init pc2 and fw result: {res1}, {res2}, {res3}')
        Assertion.assert_equal(res1 & res2 & res3, True, "ERR: init pc2 and fw configure failed")

        

       
        