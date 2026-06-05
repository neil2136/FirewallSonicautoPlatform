import sys
import os
import re
import time
import paramunittest
import json
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Proxy')
from runner.unittest.setup import Test
from lib.modules.API import network
from lib.modules.CLI import diag
from lib.modules.API import system
from lib.modules.API import firewall
from utm import Firewall
from testcases.settings import Parameter
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info
from modules.API.policy import SecurityPolicyApi
from modules.API.accessrule import AccessRuleIPv4Api

ip = "192.168.168.168"
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
dnsproxy_api = network.DnsProxyApi(fw)
pkg_api = system.PacketmonitorApi(fw)
interface_api = network.InterfaceIPv4Api(fw)
diag_api = system.DiagnosticApi(fw)
diagping_api = system.DiagnosticPingApi(fw)
dnsrule_api = firewall.DNSRuleApi(fw)
diag_cli = diag.DiagCli(fw_cli)
access_rules =  SecurityPolicyApi(fw)
acc_rules = AccessRuleIPv4Api(fw)




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

class Test_check_DNS_Proxy(Test):
    uuid = "SOSAIOT-TC-51584"
    
    def test_18_01_enable_dns_proxy(self):
        rc = dnsproxy_api.get_dnsproxy()   
        Assertion.assert_regular(json.dumps(rc), '"enforce_all_dns_requests": false', "err: Enable dns proxy failed.")

        
class Test_enable_DNS_Proxy(Test):
    uuid = "SOSAIOT-TC-51587"
    
    def test_18_01_enable_dns_proxy(self):
        dns_setting = {
            'enable': True,
        }
        rc = dnsproxy_api.config_dnsproxy(**dns_setting)   
        Assertion.assert_equal(rc, True, "ERR: Enable dns proxy failed.")
        
class Test_enable_DNS_cache(Test):
    uuid = "SOSAIOT-TC-51587"
   
    def test_18_01_enable_dns_proxy(self):
        dns_setting = {
            'dns_cache': True
        }
        rc = dnsproxy_api.config_dnsproxy(**dns_setting)   
        Assertion.assert_equal(rc, True, "ERR: Enable dns proxy failed.")

class Test_check_dns_status_interface(Test):
    uuid = "SOSAIOT-TC-51585"
    
    def test_01_enable_dns_proxy(self):
        dns_setting = {
            'enable': False,
        }
        rc = dnsproxy_api.config_dnsproxy(**dns_setting)   
        Assertion.assert_equal(rc, True, "ERR: Enable dns proxy failed.")
           
    def test_02_Config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': "2.2.2.168"            
           
        }
        rc = interface_api.config_interface(**x2_static)
        response = interface_api.get_interface_status("x2")   
        Assertion.assert_not_regular(json.dumps(response), '"dns_proxy": False', "err: Enable dns proxy failed.")
        
    def test_03_Config_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'DMZ', 
            'mode': 'static',
            'ip': "3.3.3.168",
           
        }
        rc = interface_api.config_interface(**x3_static)
        response = interface_api.get_interface_status("x3")   
        Assertion.assert_not_regular(json.dumps(response), '"dns_proxy": False', "err: Enable dns proxy failed.")
            
    def test_04_Config_X4(self):
        x3_static = {
            'if': 'X4',
            'zone': 'WLAN', 
            'mode': 'static',
            'ip': "4.4.4.168",
           
        }
        rc = interface_api.config_interface(**x3_static)
        response = interface_api.get_interface_status("x4")   
        Assertion.assert_not_regular(json.dumps(response), '"dns_proxy": False', "err: Enable dns proxy failed.")       
   
class Test_check_dns_status_interface_proxy(Test):
    uuid = "SOSAIOT-TC-51588"
    
    def test_01_enable_dns_proxy(self):
        dns_setting = {
            'enable': True,
        }
        rc = dnsproxy_api.config_dnsproxy(**dns_setting)   
        Assertion.assert_equal(rc, True, "ERR: Enable dns proxy failed.")
          
    def test_02_Config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': "2.2.2.168",
            "dns_proxy": True
        }
        rc = interface_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "err: Enable dns proxy failed.")
    
    def test_03_Config_X3(self):
        x2_static = {
            'if': 'X3',
            'zone': 'DMZ', 
            'mode': 'static',
            'ip': "3.3.3.168",
            'dns_proxy': True
        }
        rc = interface_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "err: Enable dns proxy failed.")
    
    def test_04_Config_X4(self):
        x3_static = {
            'if': 'X4',
            'zone': 'WLAN', 
            'mode': 'static',
            'ip': "4.4.4.168",
            'dns_proxy': True
        }
        rc = interface_api.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "err: Enable dns proxy failed.")
   
class Test_DNS_Proxy_4to4_Mode(Test):
    uuid = "SOSAIOT-TC-85235"
    
    def test_02_config_interface_X2_vlan1(self):
        x2_vlan1_static = {
            'if': 'x2',
            'type': 'vlan',
            'vlan_tag': 200,
            'zone': 'lan',
            'mode': 'static',
            'ip': '2.1.1.168',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_api.add_interface(**x2_vlan1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 vlan to static failed")

    def test_18_01_enable_dns_proxy(self):
        dns_setting = {
            'enable': True,
        }
        rc = dnsproxy_api.config_dnsproxy(**dns_setting)   
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
        rc = os.system(f'dig @{Parameter.X2_IP} {Parameter.REACH_WEB}')
        Assertion.assert_equal(rc, 2304, f"ERR: dig @{Parameter.X2_IP} {Parameter.REACH_WEB} fail.")

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
        Assertion.assert_equal(packet, 3, f"ERR: Not capture packet from {expect_packet_proxy['src']} to {expect_packet_proxy['dst']}.")
        Assertion.assert_equal(packet_proxy, 0, f"ERR: Not capture packet from {expect_packet_proxy['proxy_src']} to {expect_packet_proxy['proxy_dst']}.")

class Test_Check_Default_Access_Rule(Test):
    uuid = "SOSAIOT-TC-51592"
    
    def test_add_dnsrules(self):
        kwargs = {
        "dns_policies": [
            {
            "action": {
                "proxy": True
            },
            "comment": "",
            "connection_limit": {
                "source": {
                "enable": False,
                "threshold": {
                    "value": 128
                }
                }
            },
            "enable": True,
            "from": "X2",
            "max_connections": 100,
            "name": "My Rule",
            "priority": {
                "manual": 1
            },
            "proxy_mode": "ipv4-ipv4",
            "schedule": {
                "always_on": True
            },
            "service": {
                "group": "DNS (Name Service)"
            },
            "source": {
                "address": {
                "name": "X2 IP"
                }
            },
            "ticket": {
                "tag1": "",
                "tag2": "",
                "tag3": ""
            }
            }
        ]
        }
        dns_rules = dnsrule_api.add_dns_rule(**kwargs)
        logger.info(dns_rules)
        Assertion.assert_equal(dns_rules,True,'Err: Failed to add dns rules')
    
    def test_check_access_dns(self):
        show_accessrule= acc_rules.get_ipv4_access_rule_given_from_to('X2','X2')
        Assertion.assert_regular(json.dumps(show_accessrule),'"from": "X2", "to": "X2"','Err:Unable to find dns rules')
      
class Test_Delete_Dns_Cache(Test):
    uuid = "SOSAIOT-TC-51594"
    
    def test_delete_dns_cache(self):
        delete_dns_proxy = dnsproxy_api.delete_static_dns_cache_entry(domain = ["www.baidu.com","www.163.game.com"])
        logger.info(delete_dns_proxy)
        Assertion.assert_not_equal(delete_dns_proxy, True , "ERR: del Static DNS Proxy Cache Entry failed")


class Test_Flush_Cache(Test):
    uuid = "SOSAIOT-TC-51595"
    
    def test_delete_dns_cache(self):
        dns_cache_flush = dnsproxy_api.flush_caches('ipv4')
        logger.info(dns_cache_flush)
        Assertion.assert_equal(dns_cache_flush, True , "ERR: del Static DNS Proxy Cache Entry failed")

        

 
        
        
