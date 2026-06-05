from settings import *

ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
interface_api = network.InterfaceIPv4Api(fw)
split_dns_api = network.DnsSettingsApi(fw)
dnsproxy_api = network.DnsProxyApi(fw)
dnspolicy_api = network.DnsPolicyApi(fw)
pkg_api = system.PacketmonitorApi(fw)

def searchPackets(obj, **kwargs):
    found_packet = 0
    found_proxy_packet = 0
    obj.stop_capture()
    packets = obj.export_captured_packets()
    logger.info(packets)
    
    for packet in re.split('Packet number: \d+\*', packets):
        if not re.search(r''+ kwargs['src'] +'', packet) and not re.search(r''+ kwargs['proxy_src'] +'', packet):
            continue
        pattern1 = kwargs['proxy_in'] + '.*' + kwargs['proxy_out'] + '.*' + kwargs['proxy_status'] + '.*' + kwargs['proto'] + '.*' + 'Src=\[' + kwargs['proxy_src'] + '\], Dst=\[' + kwargs['proxy_dst'] + '\].*' + kwargs['domain']
        pattern2 = kwargs['in'] + '.*' + kwargs['out'] + '.*' + kwargs['status'] + '.*' + kwargs['proto'] + '.*' + 'Src=\[' + kwargs['src'] + '\], Dst=\[' + kwargs['dst'] + '\].*' + kwargs['domain']
        pattern1 =re.sub('(\.\*)+','.*',pattern1)
        pattern2 =re.sub('(\.\*)+','.*',pattern2)
        print(pattern1)
        print(pattern2)
        
        packet = packet.replace('\n','').replace('\r\n','')
        print(packet)
        
        if re.search(r'' + pattern1 +'', packet, re.I):
            logger.info(f"Packet from {kwargs['proxy_src']} to {kwargs['proxy_dst']} is found")
            logger.info('Packet detail:' + packet)
            found_proxy_packet +=1
        elif re.search(r'' + pattern2 +'', packet, re.I):
            logger.info(f"Packet from {kwargs['src']} to {kwargs['dst']} is found")
            logger.info('Packet detail:' + packet)
            found_packet +=1
        if found_proxy_packet>=1 and found_packet>=1:
            break
    return (found_packet, found_proxy_packet)


class Test_065_Add_split_DNS_Entry(Test):
    uuid = "SOSAIOT-TC-51761"
    description= show_testcase_info(Parameter.TESTPLAN, '065', description=True)['title']

    def test_065_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '065')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_065_01_add_split_DNS(self):
        split_dns_dict = {
            'domain': '*.baidu.com',
            'ipv4': {
                'primary': '8.8.8.8',
            },
            'local_interface': 'X1',
        }
        rc = split_dns_api.add_split_dns(**split_dns_dict)
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_065_02_delete_split_DNS(self):
        rc = split_dns_api.delete_split_dns(domain='*.baidu.com')
        Assertion.assert_equal(rc, True, "ERR: delete split DNS entry failed.")


class Test_068_split_DNS_Works_Well(Test):
    uuid = "SOSAIOT-TC-51762"
    description= show_testcase_info(Parameter.TESTPLAN, '068', description=True)['title']

    def test_068_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '068')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_068_01_add_dns_proxy_policy(self):
        dns_proxy_4to4 = {
            "from": "LAN",
            "name": "dns_proxy",
            "proxy_mode": "ipv4-ipv4"
        }
        rc = dnspolicy_api.add_dns_proxy_policy(**dns_proxy_4to4)
        Assertion.assert_equal(rc, True, "ERR: Add dns proxy failed.")

    def test_068_02_Config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP,
            'dns_proxy': True,
        }
        rc = interface_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_068_03_add_split_DNS(self):
        split_dns_dict = {
            'domain': '*.baidu.com',
            'ipv4': {
                'primary': Parameter.DNS_SERVER,
            },
            'local_interface': 'X1',
        }
        rc = split_dns_api.add_split_dns(**split_dns_dict)
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_068_04_dns_query(self):
        rc = True
        foundit = 0
        Parameter.ZONES=list(map(lambda x: 'custom_zone_'+x,Parameter.ZONES))
        x2_static = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP,
            # 'gateway': Parameter.X1_GW,
            'dns_proxy': True,
        }
        logger.info('Config capture ip type to udp.')
        pkt_setting= {   
            'display_filter': {
                'bidirectional': True,
                'destination_ips': '',
                'destination_ports': '',
                'ip_types': 'UDP',
            }
        }
        rc &= pkg_api.conf_packmon(**pkt_setting)

        for zone in Parameter.ZONES:
            x2_static['zone'] = 'custom_zone_' + zone
            rc &= interface_api.config_interface(**x2_static)
            logger.info('Clear capture')
            rc &= pkg_api.clear_packets()
            logger.info('Start capture')
            rc &= pkg_api.start_capture()
            os.system(f'dig @{Parameter.DUT_X2_IP} {Parameter.REACH_WEB}')
            expect_packet_proxy= {
                'src': Parameter.MY_DMZ_PC_IP,
                'dst': Parameter.DUT_X2_IP,
                'proxy_src': Parameter.DUT_X1_IP,
                'proxy_dst': Parameter.DNS_SERVER,
                'proxy_in': '',
                'proxy_out': 'X1',
                'in': 'X2',
                'out': '',
                'status': '',
                'proxy_status': '',
                'proto': 'udp',
                'domain': Parameter.REACH_WEB,
            }
            (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
            dnsproxy_api.flush_caches('ipv4')
            if packet == 0 or packet_proxy == 0:
                logger.error(f"Error:DUT do NOT proxy when set x2 to {zone}.")
            else:
                logger.info(f'DUT do proxy when set x2 to {zone}')
                foundit += 1
        Assertion.assert_equal(foundit, len(Parameter.ZONES), "ERR: DUT dns proxy failed.")

    def test_068_05_edit_split_DNS(self):
        split_dns_dict = {
            'domain': '*.baidu.com',
            'ipv4': {
                'primary': Parameter.DNS_SERVER,
            },
            'local_interface': 'X2',
        }
        rc = split_dns_api.edit_split_dns(**split_dns_dict)
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_068_06_dns_query(self):
        logger.info('Clear capture')
        rc = pkg_api.clear_packets()
        logger.info('Start capture')
        rc &= pkg_api.start_capture()
        os.system(f'dig @{Parameter.DUT_X2_IP} {Parameter.REACH_WEB}')
        expect_packet_proxy= {
            'src': Parameter.MY_DMZ_PC_IP,
            'dst': Parameter.DUT_X2_IP,
            'proxy_src': Parameter.DUT_X1_IP,
            'proxy_dst': Parameter.DNS_SERVER,
            'proxy_in': '',
            'proxy_out': 'X1',
            'in': 'X2',
            'out': '',
            'status': '',
            'proxy_status': '',
            'proto': 'udp',
            'domain': Parameter.REACH_WEB,
        }
        (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
        dnsproxy_api.flush_caches('ipv4')
        Assertion.assert_not_equal(packet, 0, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")
        Assertion.assert_not_equal(packet_proxy, 0, f"ERR: Not capture packet from {expect_packet_proxy['proxy_src']} to {expect_packet_proxy['proxy_dst']}.")

    def test_068_07_delete_split_DNS(self):
        rc = split_dns_api.delete_split_dns(domain='*.baidu.com')
        Assertion.assert_equal(rc, True, "ERR: delete split DNS entry failed.")


class Test_079_Test_with_Enforce_DNS_Proxy_Enabled(Test):
    uuid = "SOSAIOT-TC-51763"
    description= show_testcase_info(Parameter.TESTPLAN, '079', description=True)['title']

    def test_079_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '079')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_079_01_enforce_all_dns_requests(self):
        dns_setting = {
            'enforce_all_dns_requests': True,
            'dns_cache': False,
        }
        rc = dnsproxy_api.config_dnsproxy(**dns_setting)
        Assertion.assert_equal(rc, True, "ERR: enforce_all_dns_requests failed.")
        
    def test_079_02_add_split_DNS(self):
        split_dns_dict = {
            'domain': '*.baidu.com',
            'ipv4': {
                'primary': Parameter.DNS_SERVER,
            },
            'local_interface': 'X1',
        }
        rc = split_dns_api.add_split_dns(**split_dns_dict)
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_079_03_Config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP,
            'dns_proxy': True,
        }
        rc = interface_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_79_04_Config_Packet_Monitor(self):
        logger.info('Clear the capture results.')
        rc = pkg_api.clear_packets()
        logger.info('Config capture ip type to udp.')
        pkt_setting= {   
            'display_filter': {
                'bidirectional': True,
                'destination_ips': '',
                'destination_ports': '',
                'ip_types': 'UDP',
            }
        }
        rc &= pkg_api.conf_packmon(**pkt_setting)
        logger.info('Start capture')
        rc &= pkg_api.start_capture()
        Assertion.assert_equal(rc, True, "ERR: Config packet monitore fail.")

    def test_79_05_Start_dns_query(self):
        logger.info(f'dig @{Parameter.DESTINATION} {Parameter.REACH_WEB}')
        rc = os.system(f'dig @{Parameter.DESTINATION} {Parameter.REACH_WEB}')
        Assertion.assert_equal(rc, 0, f"ERR: dig @{Parameter.DESTINATION} {Parameter.REACH_WEB} fail.")

    def test_79_06_check_packet(self):
        expect_packet_proxy= {
            'src': Parameter.MY_DMZ_PC_IP,
            'dst': Parameter.DESTINATION,
            'in': 'X2',
            'out': '--', 
            'status': 'receive', 
            'proxy_src': Parameter.DUT_X1_IP,
            'proxy_dst': Parameter.DNS_SERVER,
            'proxy_in': '--',
            'proxy_out': 'X1', 
            'proxy_status': 'generate', 
            'proto': 'udp',
            'domain': Parameter.REACH_WEB,
        }
        (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
        Assertion.assert_not_equal(packet, 0, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")
        Assertion.assert_not_equal(packet_proxy, 0, f"ERR: Not capture packet from {expect_packet_proxy['proxy_src']} to {expect_packet_proxy['proxy_dst']}.")

    def test_079_07_delete_split_DNS(self):
        rc = split_dns_api.delete_split_dns(domain='*.baidu.com')
        Assertion.assert_equal(rc, True, "ERR: delete split DNS entry failed.")