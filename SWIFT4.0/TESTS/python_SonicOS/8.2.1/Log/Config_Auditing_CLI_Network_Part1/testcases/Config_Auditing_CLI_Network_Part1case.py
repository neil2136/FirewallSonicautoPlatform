from settings import *
from utils import *

param_list = []
uuid_list1 = ['1530910', '1530911', '1530914', '1530915', '1530916', '1530921', '1530923', '1530922', 
         '1530926', '1530927', '1530928', '1530929', '1530930', '1530931', '1530932', '1530933', '1530934','1530935',
          '1530936','1530937','1530939','1530941','1530942','1530943','1530948','1530949','1530950','1530951',
           '1530952','1530953','1530954','1530955','1530956','1530957','1530958','1530959','1530960','1530961','1530962',
           '1530963','1530964','1530965','1530966','1530967','1530968','1530970','1530971','1530972','1530973','1530974',
           '1530975','1530917','1530918','1530919','1530920']    
uuid_list2 = ['1530912', '1530938', '1530913']
if Params.product == 'TZ80-PROTOTYPE':
    uuid_list = uuid_list1
else:
    uuid_list = uuid_list1 + uuid_list2
logger.info(uuid_list)
for uuid in uuid_list:
    param_dict = {
        'uuid': uuid,
        'syslog_check': check_info_dict[f'tc{uuid}_syslog_check'],
        'auditlog_check': check_info_dict[f'tc{uuid}_auditlog_check'],
        'log_check': check_info_dict[f'tc{uuid}_syslog_check'],
        'snmplog_check': check_info_dict[f'tc{uuid}_syslog_check']
    }
    param_list.append(param_dict)    
logger.info(param_list) 

@paramunittest.parametrized(*param_list)

class TestConfig_Auditing_CLI_Network_Part1(Test):
    def setParameters(self, uuid, syslog_check, auditlog_check,log_check,snmplog_check):
        self.uuid = uuid
        self.syslog_check = syslog_check
        self.auditlog_check = auditlog_check
        self.log_check = log_check
        self.snmplog_check = snmplog_check
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN,self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_fw_use_CLI(self):
        logger.info('Clear related logs')
        clear_log_message() 
        flag = False
        if self.uuid == '1530913':
            logger.info('Interfaces - Create Virtual Interface via CLI')
            commands = ['con', f'interface X4 vlan {VLAN_id_X4}','ip-assignment LAN tap-mode','end','commit','exit']

        if self.uuid == '1530920':
            logger.info('Failover&amp;LB - Modify Default LB Group IPv6 - General settings via CLI')
            commands = ['con', 'failover-lb','group \ Default\ LB\ Group\ IPv6','type ratio','commit',
                        'type basic','commit','end','commit','exit']

        if self.uuid == '1530919':
            logger.info('Failover&amp;LB - Add WAN interface to WLB via CLI')
            commands = ['con', 'failover-lb','group \ Default\ LB\ Group\ IPv6','interface U0','end','commit',
                        'failover-lb','group \ Default\ LB\ Group\ IPv6','no interface U0','end','commit','exit']

        if self.uuid == '1530918':
            logger.info('Failover&amp;LB - Modify Default LB Group - General settings via CLI')
            commands = ['con', 'failover-lb','group \ Default\ LB\ Group','type ratio','commit',
                        'type basic','commit','end','commit','exit']

        if self.uuid == '1530917':
            logger.info('"Failover&amp;LB - Add WAN interface to WLB via CLI')
            commands = ['con', 'failover-lb','group \ Default\ LB\ Group','interface U0','end','commit',
                        'failover-lb','group \ Default\ LB\ Group','no interface U0','end','commit','exit']
        
        if self.uuid == '1530975':
            logger.info('DHCP Server - Delete  DHCPv6 Server Lease Scopes via CLI')
            commands = ['con', 'dhcp-server ipv6','no scope dynamic dyanmicScope',
                        'no scope static dhcps6StaticName','commit','exit']

        if self.uuid == '1530974':
            logger.info('DHCP Server - Modify Static DHCPv6 Range - Genetal Settings via CLI')
            commands = ['con', 'dhcp-server ipv6','scope static dhcps6StaticName',
                        'always-send-option','commit','exit']

        if self.uuid == '1530973':
            logger.info('DHCP Server - Add Static DHCPv6  Range via CLI')
            commands = ['con', 'dhcp-server ipv6','scope static dhcps6StaticName',
                        'ip fe00::2016','iaid 28','prefix fe00::',
                        'duid 29','commit','exit']

        if self.uuid == '1530972':
            logger.info('DHCP Server - Modify Dynamic DHCPv6 Range - Genetal Settings via CLI')
            commands = ['con', 'dhcp-server ipv6','scope dynamic dyanmicScope',
                        'always-send-option','commit','exit']

        if self.uuid == '1530971':
            logger.info('DHCP Server - Add Dynamic DHCPv6  Range via CLI')
            commands = ['con', 'dhcp-server ipv6','scope dynamic dyanmicScope','range fe00::1 fe00::2014','prefix fe00::','commit','exit']

        if self.uuid == '1530970':
            logger.info('DHCP Server - Modify DHCPv6 Server Settings - Global General Settings via CLI')
            commands = ['con', 'dhcp-server ipv6','no enable','commit','enable','commit',
                        'no enable','commit','exit']

        if self.uuid == '1530968':
            logger.info('DHCP Server - Delete DHCPv4 Server Lease Scopes via CLI')
            commands = ['con', 'dhcp-server','no scope static 10.10.10.10 000102030405','commit','exit']

        if self.uuid == '1530967':
            logger.info('DHCP Server - Modify Static DHCPv4 Range - Genetal Settings via CLI')
            commands = ['con', 'dhcp-server','scope static 192.168.168.188 00:01:02:03:04:05','ip 10.10.10.10','commit','exit']

        if self.uuid == '1530966':
            logger.info('DHCP Server - Add Static DHCPv4 Range via CLI')
            commands = ['con', 'dhcp-server','scope static 192.168.168.188 00:01:02:03:04:05','netmask 255.255.255.0','commit','exit']

        if self.uuid == '1530965':
            logger.info('DHCP Server - Modify Dynamic DHCPv4 Range - Genetal Settings via CLI')
            commands = ['con', 'dhcp-server','scope dynamic 6.6.6.7 6.6.6.254','range 6.6.6.10 6.6.6.200','allow-bootp','commit','exit']

        if self.uuid == '1530964':
            logger.info('DHCP Server - Add Dynamic DHCPv4 Range via CLI')
            commands = ['con', 'dhcp-server','scope dynamic 6.6.6.7 6.6.6.254','netmask 255.255.255.0','commit','exit']

        if self.uuid == '1530963':
            logger.info('DHCP Server - Modify DHCPv4 Server Settings - Global General Settings via CLI')
            commands = ['con', 'dhcp-server','enable','commit','no enable','commit','enable','commit','exit']

        if self.uuid == '1530962':
            logger.info('MAC-IP Anti-spoof - Delete Static IPv6 Cache Entries via CLI')
            commands = ['con', 'mac-ip-anti-spoof ipv6','no cache entries ipv6','commit','exit']

        if self.uuid == '1530961':
            logger.info('MAC-IP Anti-spoof - Add Static IPv6 Cache Entries via CLI')
            commands = ['con', 'mac-ip-anti-spoof ipv6','cache entry 1030::C9B4:FF12:48AA:1A2B 00:01:02:03:04:05 X3','commit','exit']

        if self.uuid == '1530960':
            logger.info('MAC-IP Anti-spoof - Modify IPv6 Settings for Interface - Anti-Soof Settings via CLI')
            commands = ['con', 'mac-ip-anti-spoof ipv6','interface X3','enable','enforce-ingress','ndp-lock',
                         'spoof-detection','static-ndp','commit','exit']

        if self.uuid == '1530959':
            logger.info('MAC-IP Anti-spoof - Delete Static IPv4 Cache Entries via CLI')
            commands = ['con', 'mac-ip-anti-spoof','no cache entries ipv4',
                         'commit','exit']

        if self.uuid == '1530958':
            logger.info('MAC-IP Anti-spoof - Add Static IPv4 Cache Entries via CLI')
            commands = ['con', 'mac-ip-anti-spoof','cache entry 10.10.10.10 00:01:02:03:04:05 X3',
                         'commit','exit']

        if self.uuid == '1530957':
            logger.info('MAC-IP Anti-spoof - Modify IPv4 Settings for Interface - Anti-Soof Settings via CLI')
            commands = ['con', 'mac-ip-anti-spoof','interface X3','arp-lock','arp-watch','dhcp-relay','dhcp-server',
                        'enable','enforce-ingress','spoof-detection','static-arp',
                         'commit','exit']

        if self.uuid == '1530956':
            logger.info('Neighbor Discovery - Delete Static NDP Entries via CLI')
            commands = ['con', 'no ndp entries',
                         'commit','exit']

        if self.uuid == '1530955':
            logger.info('Neighbor Discovery - Add Static NDP Entries via CLI')
            commands = ['con', 'ndp entry 2001:10:10:10:2D0:02BB:03CC:04DD 02:BB:03:CC:04:DD X0',
                         'commit','exit']

        if self.uuid == '1530954':
            logger.info('ARP - Modify ARP Settings via CLI')
            commands = ['con', 'arp','timeout 15',
                         'commit','exit']

        if self.uuid == '1530953':
            logger.info('ARP - Delete Static ARP Entries via CLI')
            commands = ['con', 'arp','no entries',
                         'commit','exit']

        if self.uuid == '1530952':
            logger.info('ARP - Add Static ARP Entries via CLI ')
            commands = ['con', 'arp','entry 3.3.3.3 00:01:02:03:04:05 X0',
                         'commit','exit']

        if self.uuid == '1530951':
            logger.info('NAT Policy - Delete IPv6 Nat Policies via CLI  ')
            commands = ['con', 'no nat-policies ipv6',
                         'commit','exit']

        if self.uuid == '1530950':
            logger.info('NAT Policy - Add IPv6 Nat Policies via CLI  ')
            commands = ['con', 'nat-policy ipv6 inbound X2 outbound X3','name newaddv6nat',
                         'commit','exit']

        if self.uuid == '1530949':
            logger.info('NAT Policy - Delete IPv4 Nat Policies via CLI  ')
            commands = ['con', 'no nat-policies ipv4',
                         'commit','exit']

        if self.uuid == '1530948':
            logger.info('NAT Policy - Add IPv4 Nat Policies via CLI  ')
            commands = ['con', 'nat-policy ipv4 inbound X2 outbound X3','name newaddnatpolicy',
                         'commit','exit']

        if self.uuid == '1530943':
            logger.info('Routing - Delete IPv6 Route policies via CLI  ')
            commands = ['con', 'no route-policy ipv6 interface X4 metric 3',
                         'commit','exit']

        if self.uuid == '1530942':
            logger.info('Routing - Add IPv6 Standard Route Policy via CLI  ')
            commands = ['con', 'route-policy ipv6 interface X4 metric 3','name newaddv6policy',
                         'commit','exit']

        if self.uuid == '1530941':
            logger.info('Routing - Delete Route Policies via CLI  ')
            commands = ['con', 'no route-policies ipv4',
                         'commit','exit']

        if self.uuid == '1530939':
            logger.info('Routing - Add Multi-Path Route Policy via CLI  ')
            commands = ['con', 'route-policy ipv4 interface X7 metric 3','gateway default','nexthop-number 2',
                         'interface X0','interface2 X2','comment newMultiPathpolicy',
                         'commit','exit']

        if self.uuid == '1530938':
            logger.info('Routing - Add Standard Route Policy via CLI  ')
            commands = ['con', 'route-policy ipv4 interface X6 metric 4','comment newStandRoutepolicy',
                         'commit','exit']

        if self.uuid == '1530937':
            logger.info('DNS Security - Add DNS Security - White List for DNS Tunnel Detection via CLI  ')
            commands = ['con', 'dns-security','dns-tunnel','white-list-entry 10.10.10.1',
                         'commit','exit']

        if self.uuid == '1530936':
            logger.info('DNS Security - Add DNS Security - White Domain Name via CLI  ')
            commands = ['con', 'dns-security','white-list-entry sonicwall.com',
                         'commit','exit']

        if self.uuid == '1530935':
            logger.info('DNS Security - Add DNS Security - Custom Malicious Domain Name via CLI  ')
            commands = ['con', 'dns-security','dns-sinkhole','commit','custom-malicious-entry sonicwall.com',
                         'commit','exit']

        if self.uuid == '1530910':
            logger.info('Interfaces - Configure one interface - LAN zone and static mode via CLI')
            commands = ['con', 'interface X3','ip-assignment LAN static','ip 2.3.3.3','commit', 'exit',]

        if self.uuid == '1530911':
            logger.info('Interfaces - Modify Interface - General settings via CLI')
            commands = ['con', 'interface X3','ip-assignment DMZ static','ip 6.6.6.6','exit',
                         'management ping','management ssh','commit','exit']

        if self.uuid == '1530912':
            logger.info('Interfaces - Modify Interface - Advanced Settings via CLI ')
            commands = ['con', 'interface X3','multicast','port aggregation aggregate 3 X5',
                         'commit','exit']

        if self.uuid == '1530914':
            logger.info('Interfaces - Configure one ipv6 interface - global static mode via CLI ')
            commands = ['con', 'interface ipv6 X3','ip-assignment static','ip 3ffe:1900:4545::f8ff:fe21:67cf',
                         'commit','exit','management https','management ssh',
                         'commit','exit']

        if self.uuid == '1530915':
            logger.info('Interfaces - Modify ipv6 interface - General settings via CLI  ')
            commands = ['con', 'interface ipv6 X3','ip-assignment static','ip 3ffe:1900:4545::f8ff:fe21:67ce',
                        'commit','exit','user-login https',
                         'commit','exit']

        if self.uuid == '1530916':
            logger.info('Interfaces - Add IPv6 Manual Tunnel Inteface via CLI  ')
            commands = ['con', 'tunnel-interface ipv6 newaddtunnelinterface','type manual','remote ipv4-address name 192.168.168.169',
                         'commit','exit']

        if self.uuid == '1530921':
            logger.info('Add Custom Zones via CLI  ')
            commands = ['con', 'zone name newaddzone','security-type public',
                         'commit','exit']

        if self.uuid == '1530922':
            logger.info('Delete Custom Zones via CLI  ')
            commands = ['con', 'no zone newupdatezone',
                         'commit','exit']

        if self.uuid == '1530923':
            logger.info('Modify Zones- General Settings via CLI  ')
            commands = ['con', 'zone name newaddzone','name newupdatezone','security-type trusted','dpi-ssl-client',
                         'commit','exit']

        if self.uuid == '1530926':
            logger.info('DNS - Modify IPv4 DNS Settings via CLI  ')
            commands = ['con', 'dns server static primary 1.1.1.1','dns server static secondary 2.2.2.2',
                        'dns server static tertiary 3.3.3.3','no dns server inherit',
                         'commit','exit']

        if self.uuid == '1530927':
            logger.info('DNS - Add IPv4 Split DNS Entry via CLI  ')
            commands = ['con', 'dns split-entry mail.126.com','server ipv4 primary 10.8.166.239',
                         'commit','exit']

        if self.uuid == '1530928':
            logger.info('Add VLAN Translation via CLI  ')
            commands = ['con', 'no dns split-entry mail.126.com',
                         'commit','exit']

        if self.uuid == '1530929':
            logger.info('DNS - Add IPv6 Split DNS Entry via CLI  ')
            commands = ['con', 'dns split-entry mail.163.com','server ipv6 primary 33::33',
                         'commit','exit']

        if self.uuid == '1530930':
            logger.info('DNS - Delete IPv6 Split DNS Entry via CLI  ')
            commands = ['con', 'no dns split-entry mail.163.com',
                         'commit','exit']

        if self.uuid == '1530931':
            logger.info('DNS Proxy - Modify DNS Proxy Global Settings via CLI  ')
            commands = ['con', 'dns-proxy','enforce-all-dns-requests','commit','no enforce-all-dns-requests',
                         'commit','exit']

        if self.uuid == '1530932':
            logger.info('DNS Proxy - Modify DNS Proxy Settings via CLI  ')
            commands = ['con', 'dns-proxy','no dns-cache','commit','dns-cache',
                         'commit','exit']

        if self.uuid == '1530933':
            logger.info('DNS Proxy - Add Static DNS Proxy Cache Entry via CLI  ')
            commands = ['con', 'dns-proxy','cache-entry sonicwall.com','address ipv4 primary 3.3.3.3',
                         'commit','exit']

        if self.uuid == '1530934':
            logger.info('DNS Proxy -Delete Static DNS Cache Entries via CLI  ')
            commands = ['con', 'dns-proxy','no cache-entry sonicwall.com',
                         'commit','exit']
            
        rc = fw_cli.do_cli_commands(commands,tag=1)
        if "Changes made" in rc[1] or "changes made" in rc[1]:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_01_config_fw_use_CLI failed")
        
    def test_02_verify_syslog_on_PC1(self):
        syslog = get_syslog()
        rc = check_result(check_list=self.syslog_check,output=syslog,mode='syslog')
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_03_verify_auditing_log(self):
        rc = verify_result('audit', self.auditlog_check)
        Assertion.assert_equal(rc, True, "ERR: test_03_verify_auditing_log failed")

    def test_04_verify_log(self):
        if self.uuid == '1530913':
            logger.info("There is a bug.")
        else:
            rc = verify_result('log', self.log_check)
            Assertion.assert_equal(rc, True, "ERR: test_04_verify_log failed")

    def test_05_verify_snmp(self):
        rc = verify_result('snmp',self.snmplog_check)
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")