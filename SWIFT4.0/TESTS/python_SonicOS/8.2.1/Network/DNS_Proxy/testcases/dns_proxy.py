import sys
import os
import re
import time
import paramunittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Proxy')
from runner.unittest.setup import Test,repeat_method
from lib.modules.API import network
from lib.modules.API import diag
from lib.modules.API import system
from utm import Firewall
from testcases.settings import Parameter
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info

ip = Parameter.X0_IP
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
dnsproxy_api = network.DnsProxyApi(fw)
dnspolicy_api = network.DnsPolicyApi(fw)
pkg_api = system.PacketmonitorApi(fw)
interface_api = network.InterfaceIPv4Api(fw)
diagnostic_api = system.DiagnosticApi(fw)
diagping_api = system.DiagnosticPingApi(fw)
diag_api = diag.DiagApi(fw)

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

class Test_18_Enable_DNS_Proxy(Test):
    uuid = "SOSAIOT-TC-51590"
    description= show_testcase_info(Parameter.TESTPLAN, '018', description=True)['title']

    def test_18_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '018')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_18_01_add_dns_proxy_policy(self):
        dns_proxy_4to4 = {
            "name": "dns_proxy",
            "proxy_mode": "ipv4-ipv4",
            "from": "LAN"
        }
        rc = dnspolicy_api.add_dns_proxy_policy(**dns_proxy_4to4)
        Assertion.assert_equal(rc, True, "ERR: Enable dns proxy failed.")

    def test_18_02_Config_packet_monitor(self):
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

    def test_18_03_Start_dns_query(self):
        logger.info(f'dig @{Parameter.X2_IP} {Parameter.REACH_WEB}')
        for _ in range(10):
            rc = os.system(f'dig @{Parameter.X2_IP} {Parameter.REACH_WEB}')
            if rc == 0:
                break
            time.sleep(2)
        Assertion.assert_equal(rc, 0, f"ERR: dig @{Parameter.X2_IP} {Parameter.REACH_WEB} fail.")

    def test_18_04_check_packet(self):
        expect_packet_proxy= {
            'src': Parameter.MY_DMZ_PC_IP,
            'dst': Parameter.X2_IP,
            'proxy_in': '',
            'proxy_out': 'X1',
            'in': 'X2',
            'out': '',
            'status': '',
            'proxy_status': '',
            'proxy_src': Parameter.X1_IP,
            'proxy_dst': Parameter.DNS_SERVER,
            'proto': 'udp',
            'domain': Parameter.REACH_WEB,
        }
        (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
        Assertion.assert_not_equal(packet, 0, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")
        Assertion.assert_not_equal(packet_proxy, 0, f"ERR: Not capture packet from {expect_packet_proxy['proxy_src']} to {expect_packet_proxy['proxy_dst']}.")


class Test_19_DNS_Proxy_4to4_mode(Test):
    uuid = "SOSAIOT-TC-51591"
    description= show_testcase_info(Parameter.TESTPLAN, '019', description=True)['title']

    def test_19_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '019')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    
    @repeat_method(3)
    def test_19_03_dns_query(self):
        rc = True
        foundit = 0
        Parameter.ZONES.extend(['LAN', 'DMZ'])
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            # 'gateway': Parameter.X1_GW,
            # 'dns_proxy': True,
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
            x2_static['zone'] = zone
            rc &= interface_api.config_interface(**x2_static)
            if zone != 'LAN':
                dns_proxy_4to4 = {
                    "name": "dns_proxy"+ zone,
                    "proxy_mode": "ipv4-ipv4",
                    "from": zone
                }
                rc &= dnspolicy_api.add_dns_proxy_policy(**dns_proxy_4to4)
            logger.info('Clear capture')
            rc &= pkg_api.clear_packets()
            logger.info('Start capture')
            rc &= pkg_api.start_capture()
            os.system(f'dig @{Parameter.X2_IP} {Parameter.REACH_WEB}')
            expect_packet_proxy= {
                'src': Parameter.MY_DMZ_PC_IP,
                'dst': Parameter.X2_IP,
                'proxy_src': Parameter.X1_IP,
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


class Test_49_Enforcement_of_DNS_Proxy(Test):
    uuid = "SOSAIOT-TC-51597"
    description = show_testcase_info(
        Parameter.TESTPLAN, '049', description=True)['title']

    def test_49_000_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '049')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_49_002_Config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            # 'dns_proxy': True,
        }
        rc = interface_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_49_003_Config_Packet_Monitor(self):
        logger.info('Clear the capture results.')
        rc = pkg_api.clear_packets()
        logger.info('Config capture ip type to udp.')
        pkt_setting = {
            'display_filter': {
                'bidirectional': True,
                'destination_ips': '',
                'destination_ports': '',
                'ip_types': 'UDP',
            },
            'monitor_filter': {      
                'firewall_generated': True,
            }
        }
        rc &= pkg_api.conf_packmon(**pkt_setting)
        logger.info('Start capture')
        rc &= pkg_api.start_capture()
        Assertion.assert_equal(rc, True, "ERR: Config packet monitore fail.")
    '''
    def test_49_004_Start_dns_query(self):
        logger.info(f'dig @{Parameter.DESTINATION} {Parameter.REACH_WEB}')
        rc = os.system(f'dig @{Parameter.DESTINATION} {Parameter.REACH_WEB}')
        Assertion.assert_equal(
            rc, 0, f"ERR: dig @{Parameter.DESTINATION} {Parameter.REACH_WEB} fail.")
    '''
    @repeat_method(3)
    def test_49_005_check_packet(self):
        logger.info(f'dig @{Parameter.DESTINATION} {Parameter.REACH_WEB}')
        for _ in range(10):
            rc = os.system(f'dig @{Parameter.DESTINATION} {Parameter.REACH_WEB}')
            if rc == 0:
                break
            time.sleep(2)
        Assertion.assert_equal(
            rc, 0, f"ERR: dig @{Parameter.DESTINATION} {Parameter.REACH_WEB} fail.")

        expect_packet_proxy = {
            'src': Parameter.MY_DMZ_PC_IP,
            'dst': Parameter.DESTINATION,
            'in': 'X2',
            'out': 'X1',
            'status': 'Forwarded',
            'proxy_src': Parameter.X1_IP,
            'proxy_dst':  Parameter.DESTINATION,
            'proxy_in': '--',
            'proxy_out': 'X1',
            'proxy_status': 'Forwarded',
            'proto': 'udp',
            'domain': Parameter.REACH_WEB,
        }
        (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
        Assertion.assert_not_equal(
            packet, 0, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")
        Assertion.assert_not_equal(
            packet_proxy, 0, f"ERR: Not capture packet from {expect_packet_proxy['proxy_src']} to {expect_packet_proxy['proxy_dst']}.")

    def test_49_006_enforce_all_dns_requests(self):
        dns_setting = {
            'enforce_all_dns_requests': True,
            'dns_cache': False,
        }
        rc = dnsproxy_api.config_dnsproxy(**dns_setting)
        Assertion.assert_equal(rc, True, "ERR: Enable dns proxy failed.")

    def test_49_007_check_diagnotics_page(self):
        
        logger.info('Clear the capture results.')
        rc = pkg_api.clear_packets()
        rc &= dnsproxy_api.flush_caches('ipv4')
        logger.info('Start capture')
        rc &= pkg_api.start_capture()
        logger.info('Check test mysonicwall on Diagnotics page')
        diagping_api.diag_ping('check-network my-sonicwall')
        expect_packet_proxy = {
            'src': Parameter.X1_IP,
            'dst': Parameter.DNS_SERVER,
            'in': '--',
            'out': 'X1', 
            'status': 'generate|consumed', 
            'proxy_src': Parameter.X1_IP,
            'proxy_dst': Parameter.DNS_SERVER,
            'proxy_in': 'X1',
            'proxy_out': 'X1',
            'proxy_status': 'generate',
            'proto': 'udp',
            'domain': 'mysonicwall',
        }
        (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
        Assertion.assert_not_equal(
            packet, 0, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")
        Assertion.assert_not_equal(
            packet_proxy, 0, f"ERR: Not capture packet from {expect_packet_proxy['proxy_src']} to {expect_packet_proxy['proxy_dst']}.")

    def test_49_008_disable_dns_proxy_policy(self):
        dns_proxy_disable = {
            "from":"LAN",
            "name": "dns_proxy",
            "enable": False,
        }
        time.sleep(480)
        rc = dnspolicy_api.edit_dns_policy(**dns_proxy_disable)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_49_009_Config_Packet_Monitor(self):
        logger.info('Clear and start the capture results.')
        rc = pkg_api.clear_packets()
        rc &= pkg_api.start_capture()
        Assertion.assert_equal(rc, True, "ERR: disable_dns_proxy_policy fail.")

    def test_49_010_check_packet(self):
        logger.info(f'dig @{Parameter.X2_IP} {Parameter.REACH_WEB}')
        os.system(f'dig @{Parameter.X2_IP} {Parameter.REACH_WEB}')
        expect_packet_proxy = {
            'src': Parameter.MY_DMZ_PC_IP,
            'dst': Parameter.X2_IP,
            'in': 'X2',
            'out': '--',
            'status': 'dropped',
            'proxy_src': Parameter.X1_IP,
            'proxy_dst': Parameter.DNS_SERVER,
            'proxy_in': '--',
            'proxy_out': 'X1',
            'proxy_status': 'generate',
            'proto': 'udp',
            'domain': Parameter.REACH_WEB,
        }
        (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
        Assertion.assert_not_equal(
            packet, 0, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")

    def test_49_011_Enable_dns_proxy_policy(self):
        dns_proxy_enable = {
            "name": "dns_proxy",
            "enable": True,
            "from":'LAN',
        }
        time.sleep(480)
        rc = dnspolicy_api.edit_dns_policy(**dns_proxy_enable)

        Assertion.assert_equal(rc, True, "ERR: enable_dns_proxy_policy failed")


class Test_53_Enable_TCP_support(Test):
    uuid = "SOSAIOT-TC-51599"
    description = show_testcase_info(
        Parameter.TESTPLAN, '053', description=True)['title']

    def test_53_000_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '053')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_53_001_enable_dns_proxy(self):
        dns_setting = {

            'dns_cache': False,
        }
        rc = dnsproxy_api.config_dnsproxy(**dns_setting)
        Assertion.assert_equal(rc, True, "ERR: Enable dns proxy failed.")

    def test_53_002_config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            # 'dns_proxy': True,
        }
        rc = interface_api.config_interface(**x2_static)

    def test_53_002_Config_packet_monitor(self):
        logger.info('Clear the capture results.')
        rc = pkg_api.clear_packets()
        logger.info('Config capture ip type to tcp.')
        pkt_setting = {
            'display_filter': {
                'bidirectional': True,
                'destination_ips': '',
                'destination_ports': '',
                'ip_types': 'TCP',
            },
            'monitor_filter': {
                'firewall_generated': True,
                'ip_types': 'TCP',
            }
        }
        rc &= pkg_api.conf_packmon(**pkt_setting)
        logger.info('Start capture')
        rc &= pkg_api.start_capture()
        Assertion.assert_equal(rc, True, "ERR: Config packet monitore fail.")

    @repeat_method(3)
    def test_53_003_Start_dns_query(self):
        rc = os.popen(
            f'dig @{Parameter.X2_IP} {Parameter.REACH_WEB} +tcp').read()
        Assertion.assert_regular(
            rc, f'{Parameter.REACH_WEB}.*{Parameter.DNS_MAP[Parameter.REACH_WEB]}', f"ERR: dig @{Parameter.X2_IP} {Parameter.REACH_WEB} fail.")

    @repeat_method(3)
    def test_53_004_check_packet(self):
        expect_packet_proxy = {
            'src': Parameter.MY_DMZ_PC_IP,
            'dst': Parameter.X2_IP,
            'proxy_src': Parameter.X1_IP,
            'proxy_dst': Parameter.DNS_SERVER,
            'proxy_in': '',
            'proxy_out': 'X1',
            'in': 'X2',
            'out': '',
            'status': '',
            'proxy_status': '',
            'proto': 'tcp',
            'domain': Parameter.REACH_WEB,
        }
        (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
        Assertion.assert_not_equal(
            packet, 0, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")
        Assertion.assert_not_equal(
            packet_proxy, 0, f"ERR: Not capture packet from {expect_packet_proxy['proxy_src']} to {expect_packet_proxy['proxy_dst']}.")


class Test_58_static_DNS_cache_entry(Test):
    uuid = "SOSAIOT-TC-51601"
    description = show_testcase_info(
        Parameter.TESTPLAN, '058', description=True)['title']

    def test_58_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '058')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_58_01_enable_dns_cache(self):
        dns_setting = {

            'enforce_all_dns_requests': False,
            'dns_cache': True,
        }
        rc = dnsproxy_api.config_dnsproxy(**dns_setting)
        Assertion.assert_equal(rc, True, "ERR: Enable dns proxy failed.")

    def test_58_01_add_dns_proxy_entry(self):
        entry = {
            'domain': Parameter.REACH_WEB,
            'ipv4_primary': Parameter.TC58_CACHE_V4,
            'ipv6_primary': Parameter.TC58_CACHE_V6,
        }
        rc = dnsproxy_api.add_dns_proxy_entry(**entry)
        Assertion.assert_equal(rc, True, "ERR: Add dns proxy entry failed.")

    def test_58_02_Config_packet_monitor(self):
        logger.info('Clear the capture results.')
        rc = pkg_api.clear_packets()
        logger.info('Config capture ip type to tcp.')
        pkt_setting = {
            'display_filter': {
                'bidirectional': True,
                'destination_ips': '',
                'destination_ports': '',
                'ip_types': 'UDP',
            },
            'monitor_filter': {
                'firewall_generated': True,
                'ip_types': 'UDP',
            }
        }
        rc &= pkg_api.conf_packmon(**pkt_setting)
        logger.info('Start capture')
        rc &= pkg_api.start_capture()
        Assertion.assert_equal(rc, True, "ERR: Config packet monitore fail.")

    def test_58_03_Start_dns_query(self):
        rc = os.popen(f'dig @{Parameter.X2_IP} {Parameter.REACH_WEB}').read()
        Assertion.assert_regular(rc, f'{Parameter.REACH_WEB}.*{Parameter.TC58_CACHE_V4}',
                                 f"ERR: dig @{Parameter.X2_IP} {Parameter.REACH_WEB} fail.")

    def test_58_04_Check_dns_proxy(self):
        expect_packet_proxy = {
            'src': Parameter.MY_DMZ_PC_IP,
            'dst': Parameter.X2_IP,
            'proxy_src': Parameter.X1_IP,
            'proxy_dst': Parameter.DNS_SERVER,
            'proxy_in': '',
            'proxy_out': '',
            'in': 'X2',
            'out': '--',
            'status': 'Received',
            'proxy_status': '',
            'proto': 'UDP',
            'domain': Parameter.REACH_WEB,
        }
        (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
        Assertion.assert_not_equal(
            packet, 0, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")
        Assertion.assert_equal(
            packet_proxy, 0, f"ERR: Not capture packet from {expect_packet_proxy['proxy_src']} to {expect_packet_proxy['proxy_dst']}.")

    def test_58_05_change_dns_proxy_mode(self):
        dns_proxy_4to6 = {
            "from":"LAN",
            "name": "dns_proxy",
            "proxy_mode": "ipv4-ipv6",
        }
        time.sleep(480)
        rc = dnspolicy_api.edit_dns_policy(**dns_proxy_4to6)
        Assertion.assert_equal(rc, True, "ERR: change_dns_proxy_mode failed.")

    def test_58_06_Config_packet_monitor(self):
        logger.info('Clear the capture results.')
        rc = pkg_api.clear_packets()
        logger.info('Start capture')
        rc &= pkg_api.start_capture()
        Assertion.assert_equal(rc, True, "ERR: Config packet monitore fail.")

    def test_58_07_Start_dns_query(self):
        rc = os.popen(
            f'dig @{Parameter.X2_IP} {Parameter.REACH_WEB} AAAA').read()
        Assertion.assert_regular(rc, f'{Parameter.REACH_WEB}.*{Parameter.TC58_CACHE_V6}',
                                 f"ERR: dig {Parameter.X2_IP} {Parameter.REACH_WEB} fail.")

    def test_58_08_Check_dns_proxy(self):
        expect_packet_proxy = {
            'src': Parameter.MY_DMZ_PC_IP,
            'dst': Parameter.X2_IP,
            'proxy_src': Parameter.X1_IP,
            'proxy_dst': Parameter.DNS_SERVER_V6,
            'proxy_in': '',
            'proxy_out': '',
            'in': 'X2',
            'out': '--',
            'status': 'Received',
            'proxy_status': '',
            'proto': 'UDP',
            'domain': Parameter.REACH_WEB,
        }
        (packet, packet_proxy) = searchPackets(pkg_api, **expect_packet_proxy)
        Assertion.assert_not_equal(
            packet, 0, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")
        Assertion.assert_equal(
            packet_proxy, 0, f"ERR: Not capture packet from {expect_packet_proxy['proxy_src']} to {expect_packet_proxy['proxy_dst']}.")
