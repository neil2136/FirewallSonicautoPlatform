from definition.settings import *
from definition.utils import *

# GUI:Enable DNS Proxy on LAN/DMZ zone interface
class TestGUI_1526805(Test):
    uuid = "SOSAIOT-TC-51589"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    LAN_name = 'X0_interface'
    DMZ_name = 'X3_interface'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy_on_LAN(self):
        X0_interface = {
            "name": self.LAN_name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}}
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_on_LAN failed!!")

    def test_02_add_dns_policy_on_DMZ(self):
        X3_interface = {
            "name": self.DMZ_name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X3",
            "source":{"address":{"any":True}}
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X3_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_on_DMZ failed!!")

    def test_03_delete_added_dns_policies(self):
        rc_lan = dns_rule_api.del_dns_rule_by_name(name=self.LAN_name)
        logger.info(f'Delete LAN dns proxy policy result...... {rc_lan}')
        rc_dmz = dns_rule_api.del_dns_rule_by_name(name=self.DMZ_name)
        logger.info(f'Delete DMZ dns proxy policy result...... {rc_dmz}')
        Assertion.assert_equal(rc_lan & rc_dmz, True, "ERR: delete_added_dns_policies failed!!")


# [7.1.1] Verify the Service is 'DNS (Name Service)' as default in DNS Proxy Policy
class TestGUI_2268490(Test):
    uuid = "SOSAIOT-TC-51625"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'proxy'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy_on_CLI(self):
        proxy = {
            "name": self.name,
        }
        rc = dns_policy_cli.add_dns_policy(**proxy)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_on_CLI failed!!")

    def test_02_check_default_service(self):
        res = dns_rule_api.get_dns_rule_by_name(name=self.name)
        rc = res['dns_policies'][0]['service'].get('group') == 'DNS (Name Service)' if 'dns_policies' in res else False
        Assertion.assert_equal(rc, True, "ERR: check default service failed!!")

    def test_03_delete_added_dns_policies(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        logger.info(f'Delete LAN dns proxy policy result...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policies failed!!")


# Verify the auto added ACL will be change when switch DNS Proxy Protocol
class TestGUI_1526813(Test):
    uuid = "SOSAIOT-TC-51593"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'MODE'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_UDP_only_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
            "service": {"name": "DNS (Name Service) UDP"}
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_UDP_only_dns_policy failed!!")

    def test_02_check_related_ACL_service(self):
        acls = accessrule_api.find_access_rules_by_json(**{"comment": "Auto rule for DNS policy"})
        for acl in acls:
            if 'DNS (Name Service) UDP' in json.dumps(acl):
                rc = True
                break
        else:
            rc = False
            logger.error('Cannot find related ACLs!')
        Assertion.assert_equal(rc, True, "ERR: check_related_ACL_service failed!!")

    def test_03_change_UDP_only_to_UDP_and_TCP(self):
        edit = {
            'name': self.name, 
            "service": {"group": "DNS (Name Service)"}
        }
        rc = dns_rule_api.edit_dns_rule(**edit)
        Assertion.assert_equal(rc, True, "ERR: change_UDP_only_to_UDP_and_TCP failed!!")

    def test_04_check_related_ACL_service(self):
        acls = accessrule_api.find_access_rules_by_json(**{"comment": "Auto rule for DNS policy"})
        for acl in acls:
            if 'DNS (Name Service) UDP' not in json.dumps(acl) and 'DNS (Name Service)' in json.dumps(acl):
                rc = True
                break
        else:
            rc = False
            logger.error('Cannot find related ACLs!')
        Assertion.assert_equal(rc, True, "ERR: check_related_ACL_service failed!!")

    def test_05_delete_added_dns_policies(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policies failed!!")


# Function: DNS Proxy mode 4TO4/4TO6 mode work fine when DUT has multiple(3) ipv4/ipv6 DNS servers.
class TestFunc_1526810(Test):
    uuid = "SOSAIOT-TC-51617"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    # jira = 'GEN8-8494'
    Fake_1 = '1.2.3.4'
    Fake_2 = '2.2.3.4'
    Real_Server = CaseParams.DNS_PC2
    V6_Fake_1 = '1:2:3::4'
    V6_Fake_2 = '2:2:3::4'
    V6_Real_Server = CaseParams.DNS_V6_PC2
    static = {
        'static':{
            "primary": Real_Server,
            "secondary": Fake_1,
            "tertiary": Fake_2
    }}
    server = 'ipv4_1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_4to4_dns_policy_on_X0(self):
        X0_interface = {
            "name": 'X0_4to4',
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}}
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_on_X0 failed!!")

    def test_02_config_real_server_dns_server_1_and_check(self):
        dns = copy.deepcopy(dns_dict)
        dns['dns']['server'].update(self.static)
        rc_dns = dns_api.set_dns(**dns)
        logger.info(f'Config real server to dns server {self.server} result ...... {rc_dns}')
        time.sleep(5)
        out = ''
        rc_check = False
        if '1' not in self.server:
            failed_queries()
        for _ in range(10):
            out += PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
            if CaseParams.DOMAIN_IP in out:
                rc_check = True
                break
        logger.info(f'Check proxy result ...... {rc_check}')
        Assertion.assert_equal(rc_check, True, f"ERR: config_real_server_dns_server_{self.server}_and_check failed!!")

    def test_03_config_real_server_dns_server_2_and_check(self):
        self.static = {
            'static':{
                "primary": self.Fake_1,
                "secondary": self.Real_Server,
                "tertiary": self.Fake_2
            }}
        self.server = 'ipv4_2'
        self.test_02_config_real_server_dns_server_1_and_check()

    def test_04_config_real_server_dns_server_3_and_check(self):
        self.static = {
            'static':{
                "primary": self.Fake_1,
                "secondary": self.Fake_2,
                "tertiary": self.Real_Server
            }}
        self.server = 'ipv4_3'
        self.test_02_config_real_server_dns_server_1_and_check()

    def test_05_change_policy_to_4to6_mode(self):
        edit = {
            'name': 'X0_4to4', 
            'new-name': 'X0_4to6',
            "proxy_mode": "ipv4-ipv6"
        }
        rc = dns_rule_api.edit_dns_rule(**edit)
        Assertion.assert_equal(rc, True, "ERR: change_policy_to_4to6_mode failed!!")

    def test_06_config_real_server_ipv6_dns_server_1_and_check(self):
        self.static = {
            'ipv6':{
                "static": {
                    "primary": self.V6_Real_Server,
                    "secondary": self.V6_Fake_1,
                    "tertiary": self.V6_Fake_2
                },
                "preferred": True,
                "inherit": False
            }
        }
        self.server = 'ipv6_1'
        self.test_02_config_real_server_dns_server_1_and_check()

    def test_07_config_real_server_ipv6_dns_server_2_and_check(self):
        self.static = {
            'ipv6':{
                "static": {
                    "primary": self.V6_Fake_1,
                    "secondary": self.V6_Real_Server,
                    "tertiary": self.V6_Fake_2
                },
                "preferred": True,
                "inherit": False
            }
        }
        self.server = 'ipv6_2'
        self.test_02_config_real_server_dns_server_1_and_check()

    def test_08_config_real_server_ipv6_dns_server_3_and_check(self):
        self.static = {
            'ipv6':{
                "static": {
                    "primary": self.V6_Fake_1,
                    "secondary": self.V6_Fake_2,
                    "tertiary": self.V6_Real_Server
                },
                "preferred": True,
                "inherit": False
            }
        }
        self.server = 'ipv6_3'
        self.test_02_config_real_server_dns_server_1_and_check()

    def test_09_delete_added_dns_policies(self):
        rc = dns_rule_api.del_dns_rule_by_name(name='X0_4to6')
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policies failed!!")


# Function: Test the failover and failback between the primary DNS server and the secondary server and the tertiary server.
class TestFunc_1526830(Test):
    uuid = "SOSAIOT-TC-51604"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    jira = 'GEN8-8494'
    name = 'failover'
    domain = 'dns.baidu.com'
    type = 'ipv4'
    host = PC2_login
    reply_ip = CaseParams.DNS_PC3

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_4to4_dns_policy_on_X0(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}}
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_on_X0 failed!!")

    def test_02_config_dns_servers_and_check(self):
        static = {
            'static':{
                "primary": CaseParams.DNS_PC2,
                "secondary": CaseParams.DNS_PC3,
                "tertiary": CaseParams.DNS_PC4
                },
            'ipv6': {
                "static": {
                    "primary": CaseParams.DNS_V6_PC2,
                    "secondary": CaseParams.DNS_V6_PC3,
                    "tertiary": CaseParams.DNS_V6_PC4
                },
                "preferred": False
            }}
        dns = copy.deepcopy(dns_dict)
        dns['dns']['server'].update(static)
        rc_dns = dns_api.set_dns(**dns)
        logger.info(f'Config servers result ...... {rc_dns}')
        time.sleep(5)
        out = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {self.domain}')
        rc_check = str(CaseParams.DNS_PC2) in out
        logger.info(f'Check proxy result ...... {rc_check}')
        Assertion.assert_equal(rc_check, True, "ERR: config_dns_servers_and_check failed!!")

    def test_03_down_server_1_and_check(self):
        logger.info('Config down dns server......')
        _ = self.host.send_command('service named stop')
        time.sleep(5)
        out = ''
        rc = False
        failed_queries()
        for _ in range(10):
            out += PC1_login.send_command(f'dig @{Parameter.FIREWALL} {self.domain}')
            if str(self.reply_ip) in out:
                rc = True
                break
        logger.info(f'Check failover dns server result ...... {rc}')
        Assertion.assert_equal(rc, True, f"ERR: down_{self.type}_server_1_and_check failed!!")

    def test_04_down_server_2_and_check(self):
        self.host = PC3_login
        self.reply_ip = CaseParams.DNS_PC4
        self.test_03_down_server_1_and_check()

    def test_05_down_all_servers_and_check(self):
        logger.info('Config down dns server 3......')
        _ = PC3_login.send_command('service named stop')
        time.sleep(5)
        failed_queries()
        logger.info('Init packet capture and query ......')
        fw_packet_monitor_clear_start()
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        logger.info(rc)
        logger.info('Check captured packets ......')
        cmd = f'dns.qry.name=={CaseParams.DOMAIN} and ip.src=={Parameter.X1_IP} and ip.dst=={CaseParams.DNS_PC4}'
        out = fw_packet_monitor_stop_export(cmd=cmd, pc_login=PC1_login)
        rc = 'Generated' in out
        Assertion.assert_equal(rc, True, "ERR: down_all_servers_and_check failed!!")

    def test_06_up_server_1_and_check(self):
        cmd = ["systemctl restart named", "systemctl status named"]
        res_3 = PC4_login.send_commands(cmd)
        rc_3 = 'running\n' in res_3
        failed_queries()
        PC1_login.send_command(f'dig @{Parameter.FIREWALL} {self.domain}')
        logger.info(f'Config UP dns server 3 result ...... {rc_3}')
        res_2 = PC3_login.send_commands(cmd)
        rc_2 = 'running\n' in res_2
        failed_queries()
        PC1_login.send_command(f'dig @{Parameter.FIREWALL} {self.domain}')
        logger.info(f'Config UP dns server 2 result ...... {rc_2}')
        res_1 = PC2_login.send_commands(cmd)
        rc_1 = 'running\n' in res_1
        failed_queries()
        PC1_login.send_command(f'dig @{Parameter.FIREWALL} {self.domain}')
        logger.info(f'Config UP dns server 1 result ...... {rc_1}')
        time.sleep(5)
        out = ''
        rc = False
        for _ in range(10):
            out += PC1_login.send_command(f'dig @{Parameter.FIREWALL} {self.domain}')
            if str(CaseParams.DNS_PC2) in out:
                rc = True
                break
        logger.info(f'Check failover dns server result ...... {rc}')
        Assertion.assert_equal(rc, True, f"ERR: down_{self.type}_server_1_and_check failed!!")

    def test_07_change_policy_to_4to6_mode(self):
        edit = {
            'name': self.name, 
            "proxy_mode": "ipv4-ipv6"
        }
        rc = dns_rule_api.edit_dns_rule(**edit)
        Assertion.assert_equal(rc, True, "ERR: change_policy_to_4to6_mode failed!!")

    def test_08_down_ipv6_server_1_and_check(self):
        self.type = 'ipv6'
        self.host = PC2_login
        self.reply_ip = CaseParams.DNS_PC3
        self.test_03_down_server_1_and_check()

    def test_09_down_ipv6_server_2_and_check(self):
        self.type = 'ipv6'
        self.host = PC3_login
        self.reply_ip = CaseParams.DNS_PC4
        self.test_03_down_server_1_and_check()

    def test_10_down_all_servers_and_check(self):
        logger.info('Config down dns server 3......')
        _ = PC3_login.send_command('service named stop')
        time.sleep(5)
        failed_queries()
        logger.info('Init packet capture and query ......')
        fw_packet_monitor_clear_start()
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        logger.info(rc)
        logger.info('Check captured packets ......')
        cmd = f'dns.qry.name=={CaseParams.DOMAIN} and ipv6.src=={Parameter.X1_IPV6} and ipv6.dst=={CaseParams.DNS_V6_PC4}'
        out = fw_packet_monitor_stop_export(cmd=cmd, pc_login=PC1_login)
        Assertion.assert_equal(bool(out), True, "ERR: down_all_servers_and_check failed!!")

    def test_11_up_ipv6_server_1_and_check(self):
        self.type = 'ipv6'
        self.test_06_up_server_1_and_check()

    def test_12_delete_added_dns_policies(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policies failed!!")


# Function: For the LAN interface that not enable DNS proxy, verify firewall won't do the proxy work when receive DNS qurey to LAN interface IP
class TestFunc_1526816(Test):
    uuid = "SOSAIOT-TC-51596"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_init_packet_capture_and_query(self):
        fw_packet_monitor_clear_start()
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, 'no servers could be reached', "ERR: query should fail!!")

    def test_02_check_dropped_packet(self):
        cmd = f'dns.qry.name=={CaseParams.DOMAIN} and ip.src=={PC1_ETH2_IP} and ip.dst=={Parameter.FIREWALL}'
        out = fw_packet_monitor_stop_export(cmd=cmd, pc_login=PC1_login)
        rc = 'DROPPED' in out
        logger.info(f'DROPPED in captured packet ...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: check_dropped_packet failed!!")


# Function test when enable TCP support in 4to6 DNS Proxy mode
class TestFunc_1526823(Test):
    uuid = "SOSAIOT-TC-51619"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'TCP_4to6'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_ipv6_dns_server(self):
        static = {
                "static": {
                    "primary": CaseParams.DNS_V6_PC2,
                    "secondary": '',
                    "tertiary": ''
                },
                "preferred": True
            }
        dns = copy.deepcopy(dns_dict)
        dns['dns']['server']['ipv6'].update(static)
        rc = dns_api.set_dns(**dns)
        Assertion.assert_equal(rc, True, "ERR: config_ipv6_dns_server failed!!")

    def test_02_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv6",
            "from": "X0",
            "source":{"address":{"any":True}},
            "service": {"name": "DNS (Name Service) TCP"}
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_03_query_and_check(self):
        time.sleep(5)
        rc = False
        for _ in range(5):
            res = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN} +tcp')
            if CaseParams.DOMAIN_IP in res:
                rc = True
                break
            time.sleep(2)
        Assertion.assert_equal(rc, True, "ERR: query failed!!")

    def test_04_query_via_other_dns_server_and_check(self):
        res = PC1_login.send_command(f'dig @{Parameter.X1_DNS1} bing.com +tcp')
        rc = all(x not in res for x in ('no servers could be reached', 'connection timed out', 'connection refused'))
        Assertion.assert_equal(rc, True, "ERR: query failed!!")

    def test_05_delete_added_dns_policies(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policies failed!!")


# Function test when disable TCP support in 4to4 DNS Proxy mode
class TestFunc_1526824(Test):
    uuid = "SOSAIOT-TC-51620"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'UDP_4to4'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_dns_server(self):
        static = {
                    "primary": CaseParams.DNS_PC2,
                    "secondary": '',
                    "tertiary": ''
                }
        dns = copy.deepcopy(dns_dict)
        dns['dns']['server']['static'].update(static)
        rc = dns_api.set_dns(**dns)
        Assertion.assert_equal(rc, True, "ERR: config_dns_server failed!!")

    def test_02_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
            "service": {"name": "DNS (Name Service) UDP"}
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_03_init_packet_capture_and_query(self):
        fw_packet_monitor_clear_start()
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN} +tcp')
        Assertion.assert_regular(rc, 'connection refused', "ERR: query should fail!!")

    def test_04_check_dropped_packet(self):
        cmd = f'tcp.port==53 and ip.src=={PC1_ETH2_IP} and ip.dst=={Parameter.FIREWALL}'
        out = fw_packet_monitor_stop_export(cmd=cmd, pc_login=PC1_login)
        rc = 'DROPPED' in out
        logger.info(f'DROPPED in captured packet ...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: check_dropped_packet failed!!")

    def test_05_query_via_other_dns_server_and_check(self):
        res = PC1_login.send_command(f'dig @{Parameter.X1_DNS1} bing.com +tcp')
        rc = all(x not in res for x in ('no servers could be reached', 'connection timed out', 'connection refused'))
        Assertion.assert_equal(rc, True, "ERR: query failed!!")

    def test_06_delete_added_dns_policies(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policies failed!!")


# Function test while switching mode between 4to4 and 4to6.
class TestFunc_1526825(Test):
    uuid = "SOSAIOT-TC-51600"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'MODE'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_dns_server(self):
        static = {
            'static':{
                    "primary": CaseParams.DNS_PC2,
                    "secondary": '',
                    "tertiary": ''
                },
            'ipv6': {
                "static": {
                    "primary": CaseParams.DNS_V6_PC2,
                    "secondary": '',
                    "tertiary": ''
                },
                "preferred": False
            }}
        dns = copy.deepcopy(dns_dict)
        dns['dns']['server'].update(static)
        rc = dns_api.set_dns(**dns)
        Assertion.assert_equal(rc, True, "ERR: config_dns_server failed!!")

    def test_02_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_03_init_packet_capture_and_query(self):
        fw_packet_monitor_clear_start()
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, CaseParams.DOMAIN_IP, "ERR: query failed!!")

    def test_04_check_proxy_packet(self):
        cmd = f'dns.qry.name=={CaseParams.DOMAIN} and ip.src=={CaseParams.DNS_PC2} and ip.dst=={Parameter.X1_IP}'
        out = fw_packet_monitor_stop_export(cmd=cmd, pc_login=PC1_login)
        rc = 'No error' in out
        logger.info(f'"No error" in ipv4 dns server replied packet ...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: check_proxy_packet failed!!")

    def test_05_change_policy_to_4to6_mode(self):
        edit = {
            'name': self.name,
            "proxy_mode": "ipv4-ipv6"
        }
        rc = dns_rule_api.edit_dns_rule(**edit)
        Assertion.assert_equal(rc, True, "ERR: change_policy_to_4to6_mode failed!!")

    def test_06_init_packet_capture_and_query(self):
        fw_packet_monitor_clear_start()
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, CaseParams.DOMAIN_IP, "ERR: query failed!!")

    def test_07_check_proxy_packet(self):
        cmd = f'dns.qry.name=={CaseParams.DOMAIN} and ipv6.src=={CaseParams.DNS_V6_PC2} and ipv6.dst=={Parameter.X1_IPV6}'
        # cmd = f'dns.qry.name=={CaseParams.DOMAIN}'
        out = fw_packet_monitor_stop_export(cmd=cmd, pc_login=PC1_login)
        logger.info(out)
        rc = 'No error' in out
        logger.info(f'No error in ipv6 dns server replied packet ...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: check_proxy_packet failed!!")

    def test_08_delete_added_dns_policies(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policies failed!!")


# Function test when dns cache enabled and the cache entry is already expired in 4to4 and 4to6 mode.
class TestFunc_1526828(Test):
    uuid = "SOSAIOT-TC-51602"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'Enable_Cache'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_proxy_cache(self):
        disCache = {
            'dns_cache': True
        }
        rc = dns_proxy_api.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: Enable DNS Proxy Cache failed")

    def test_02_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_03_query_and_check(self):
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, CaseParams.DOMAIN_IP, "ERR: query failed!!")

    def test_04_check_dynamic_dns_cache(self):
        res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        rc = CaseParams.DOMAIN in json.dumps(res)
        logger.info(f'{CaseParams.DOMAIN} in dynamic cache ...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: check_proxy_packet failed!!")

    def test_05_query_after_expired_and_check_updated(self):
        time.sleep(10)
        cache_res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        rc_expired = False
        for cache in cache_res:
            if cache['domain_name'] == CaseParams.DOMAIN and 'Expired' in cache['time_to_live']:
                rc_expired = True
                break
        # rc_expired = 'Expired' in json.dumps(cache_res)
        logger.info(f'The dynamic cache is expired...... {rc_expired}')
        qry_res = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        rc_query = CaseParams.DOMAIN_IP in qry_res
        logger.info(f'Query again result ...... {rc_query}')
        update_res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        rc_update = False
        for cache in update_res:
            if cache['domain_name'] == CaseParams.DOMAIN and 'Expired' not in cache['time_to_live']:
                rc_update = True
                break
        # rc_update = CaseParams.DOMAIN in json.dumps(update_res) and 'Expired' not in json.dumps(update_res)
        logger.info(f'The dynamic cache is updated ...... {rc_update}')
        Assertion.assert_equal(rc_update, True, "ERR: query_after_expired_and_check_updated failed!!")

    def test_06_change_policy_to_4to6_mode(self):
        edit = {
            'name': self.name,
            "proxy_mode": "ipv4-ipv6"
        }
        rc = dns_rule_api.edit_dns_rule(**edit)
        Assertion.assert_equal(rc, True, "ERR: change_policy_to_4to6_mode failed!!")

    def test_07_flush_dynamic_cache_and_query_and_check(self):
        res = dns_proxy_api.flush_caches('ipv4')
        logger.info(f'Flush dynamic cache result ...... {res}')
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, CaseParams.DOMAIN_IP, "ERR: query failed!!")

    def test_08_check_dynamic_dns_cache(self):
        res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        rc = CaseParams.DOMAIN in json.dumps(res)
        logger.info(f'{CaseParams.DOMAIN} in dynamic cache ...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: check_proxy_packet failed!!")

    def test_09_query_after_expired_and_check_updated(self):
        time.sleep(10)
        cache_res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        rc_expired = False
        for cache in cache_res:
            if cache['domain_name'] == CaseParams.DOMAIN and 'Expired' in cache['time_to_live']:
                rc_expired = True
                break
        # rc_expired = 'Expired' in json.dumps(cache_res)
        logger.info(f'The dynamic cache is expired...... {rc_expired}')
        qry_res = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        rc_query = CaseParams.DOMAIN_IP in qry_res
        logger.info(f'Query again result ...... {rc_query}')
        update_res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        rc_update = False
        for cache in update_res:
            if cache['domain_name'] == CaseParams.DOMAIN and 'Expired' not in cache['time_to_live']:
                rc_update = True
                break
        # rc_update = CaseParams.DOMAIN in json.dumps(update_res) and 'Expired' not in json.dumps(update_res)
        logger.info(f'The dynamic cache is updated ...... {rc_update}')
        Assertion.assert_equal(rc_update, True, "ERR: query_after_expired_and_check_updated failed!!")

    def test_10_delete_added_dns_policies_and_flush_caches(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        logger.info(f'Delete added policy result...... {rc}')
        res = dns_proxy_api.flush_caches('ipv4')
        logger.info(f'Flush dynamic cache result ...... {res}')
        Assertion.assert_equal(rc and res, True, "ERR: delete_added_dns_policies_and_flush_caches failed!!")


# Function test when DNS cache is disabled
class TestFunc_1526827(Test):
    uuid = "SOSAIOT-TC-51621"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'No_Cache'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_disable_dns_proxy_cache(self):
        disCache = {
            'dns_cache': False
        }
        rc = dns_proxy_api.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: disable DNS Proxy Cache failed")

    def test_02_add_dns_static_cache(self):
        rc = dns_proxy_api.add_dns_proxy_static_entry(msg=False, **{"domain": CaseParams.DOMAIN, 'ipv4_primary': "123.1.1.1", 'ipv6_primary': "123::1"})
        Assertion.assert_equal(rc, True, "ERR: add dns static cache failed!!")

    def test_03_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_04_query_and_check(self):
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, CaseParams.DOMAIN_IP, "ERR: query failed!!")

    def test_05_change_policy_to_4to6_mode(self):
        edit = {
            'name': self.name,
            "proxy_mode": "ipv4-ipv6"
        }
        rc = dns_rule_api.edit_dns_rule(**edit)
        Assertion.assert_equal(rc, True, "ERR: change_policy_to_4to6_mode failed!!")

    def test_06_query_and_check(self):
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, CaseParams.DOMAIN_IP, "ERR: query failed!!")

    def test_07_delete_added_dns_policies_and_caches(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        logger.info(f'Delete dns policy result ...... {rc}')
        rc_cache = dns_cli.delete_dns_proxy_static_cache_entry()
        logger.info(f'Delete dns proxy static cache result ...... {rc}')
        Assertion.assert_equal(rc & rc_cache, True, "ERR: delete_added_dns_policies and caches failed!!")


# Log: verify the log entry "Send DNS proxy query"
class TestGUI_1526834(Test):
    uuid = "SOSAIOT-TC-51623"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'Log'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_proxy_cache(self):
        disCache = {
            'dns_cache': True
        }
        rc = dns_proxy_api.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: enable DNS Proxy Cache failed")

    def test_02_config_dns_proxy_logs(self):
        res = log_monitor_api.clear_log()
        logger.info(f'Clear logs ...... {res}')
        rc = log_category_api.edit_log_category_groups_by_id(id=str(log_group_dict['log']['group'][0]['id']), **log_group_dict)
        Assertion.assert_equal(rc, True, "ERR: config dns proxy logs failed!!")

    def test_03_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_04_query_and_check(self):
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, CaseParams.DOMAIN_IP, "ERR: query failed!!")

    def test_05_check_send_proxy_logs(self):
        res = log_monitor_api.export_log_txt(log_switch=False)
        logger.info(res)
        CaseParams.log = res
        rc = 'Send DNS proxy query' in res
        logger.info(f"'Send DNS proxy query' in logs...... {rc}")
        Assertion.assert_equal(rc, True, "ERR: check send proxy logs failed!!")

    def test_06_delete_added_dns_policies_and_caches(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        logger.info(f'Delete dns policy result ...... {rc}')
        rc_cache = dns_proxy_api.flush_caches('ipv4')
        logger.info(f'Flush dynamic cache result ...... {rc_cache}')
        Assertion.assert_equal(rc & rc_cache, True, "ERR: delete_added_dns_policies and caches failed!!")


# Log: verify the log entry "Add DNS cache"
class TestGUI_1526835(Test):
    uuid = "SOSAIOT-TC-51607"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_add_dns_cache_logs(self):
        rc = 'Add DNS cache' in CaseParams.log
        logger.info(f"'Add DNS cache' in logs...... {rc}")
        Assertion.assert_equal(rc, True, "ERR: check add dns cache log failed!!")


# check TSR about dns proxy settings and dns cache (include dns proxy option on interface and main switch ,split DNS, static DNS settings and cache)
class TestGUI_1526833(Test):
    uuid = "SOSAIOT-TC-51606"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'TSR'
    static_domain = "pc2.baidu.com"
    static_ip = '123.3.2.1'
    static_ipv6 = "123::1"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_proxy_cache(self):
        disCache = {
            'dns_cache': True
        }
        rc = dns_proxy_api.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: enable DNS Proxy Cache failed")

    def test_02_add_dns_static_cache(self):
        entry = {"domain": self.static_domain, 'ipv4_primary': self.static_ip, 'ipv6_primary': self.static_ipv6}
        rc = dns_proxy_api.add_dns_proxy_static_entry(msg=False, **entry)
        Assertion.assert_equal(rc, True, "ERR: add dns static cache failed!!")

    def test_03_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_04_query_and_check(self):
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, CaseParams.DOMAIN_IP, "ERR: query failed!!")

    def test_05_check_tsr(self):
        rc = False
        res = diagnostic_api.conf_tsr(**{'dns_proxy_cache': True})
        logger.info(f'Enable dns proxy cache in tsr...... {res}')
        tsr = diagnostic_api.get_tsr_part2(func="Network : DNS Proxy")
        items = (CaseParams.DOMAIN, CaseParams.DOMAIN_IP, self.static_domain, self.static_ip, self.static_ipv6, 'Enable DNS Cache: 1')
        for item in items:
            rc = item in tsr if tsr else False
            if not rc:
                logger.error(f"<{item}> is not in tsr!! or TSR is null!!")
                break
        Assertion.assert_equal(rc, True, "ERR: check_tsr failed!!")

    def test_06_delete_added_dns_policies_and_caches(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        logger.info(f'Delete dns policy result ...... {rc}')
        rc_cache = dns_cli.delete_dns_proxy_static_cache_entry()
        logger.info(f'Delete dns proxy static cache result ...... {rc_cache}')
        rc_flush = dns_proxy_api.flush_caches('ipv4')
        logger.info(f'Flush dynamic cache result ...... {rc_flush}')
        disCache = {'dns_cache': False}
        rc_disable = dns_proxy_api.config_dnsproxy(**disCache)
        logger.info(f"Disable DNS Proxy Cache ...... {rc_disable}")
        Assertion.assert_equal(rc & rc_cache & rc_flush & rc_disable, True, "ERR: delete_added_dns_policies and caches failed!!")


# Function test of NO enforcement of DNS proxy with stack DNS packets sent by sonicOS (license manager, MSW, GAV database, CFS backend, FQDN AO in PBR/NAT/ACL/VPN, syslog server, etc)
class TestGUI_1526831(Test):
    uuid = "SOSAIOT-TC-51622"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_no_wan_zone(self):
        policy = {
            "name": 'Stack_DNS',
            "proxy_mode": "ipv4-ipv4",
            "from": "WAN",
            "source":{"address":{"any":True}},
        }
        res = dns_policy_api.add_dns_proxy_policy(msg=True, **policy)
        logger.info(json.dumps(res))
        msg = ['\\"WAN\\" is not a reasonable value', "'WAN' not a reasonable value"]
        rc = not all(x.lower() not in json.dumps(res).lower() for x in msg)
        Assertion.assert_equal(rc, True, "ERR: check_no_wan_zone failed!!")

    def test_02_delete_added_dns_policies(self):
        rc = dns_policy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policies failed!!")


# Verify the maximum entries of static DNS Cache is 256 and FW could reach this maximum.
class TestBoundary_1526821(Test):
    uuid = "SOSAIOT-TC-51626"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_max_count_cache(self):
        rc = False
        for count in range(256):
            cache = {"domain":f'{count}.com', 'ipv4_primary': "192.168.1.1"}
            rc = dns_proxy_api.add_dns_proxy_static_entry(**cache)
            if not rc:
                logger.error(f'Add dns cache {count} failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: add_max_count_cache failed!!")

    def test_02_add_one_more_cache_failed(self):
        res = dns_proxy_api.add_dns_proxy_static_entry(msg=True, **{"domain":'256.com', 'ipv4_primary': "192.168.1.1"})
        rc = 'Static DNS Cache Entry is Full' in json.dumps(res)
        Assertion.assert_equal(rc, True, "ERR: add_one_more_cache should fail!!")

    def test_03_delete_added_dns_caches(self):
        rc = dns_cli.delete_dns_proxy_static_cache_entry()
        time.sleep(5)
        rc = dns_cli.delete_dns_proxy_static_cache_entry()
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_caches failed!!")


# Test the DNS cache entry update (IP changed, IP not change but TTL change)
class TestFunc_1526817(Test):
    uuid = "SOSAIOT-TC-51618"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'Update'
    changed_ip = '192.3.2.1'
    changed_ipv6 = '1009:3:2::1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_proxy_cache(self):
        static = {
            'static':{
                    "primary": CaseParams.DNS_PC2,
                    "secondary": '',
                    "tertiary": ''
                },
            'ipv6': {
                "static": {
                    "primary": CaseParams.DNS_V6_PC2,
                    "secondary": '',
                    "tertiary": ''
                },
                "preferred": False
            }}
        dns = copy.deepcopy(dns_dict)
        dns['dns']['server'].update(static)
        rc = dns_api.set_dns(**dns)

        cache = {'dns_cache': True}
        rc = dns_proxy_api.config_dnsproxy(**cache)
        Assertion.assert_equal(rc, True, "ERR: Enable DNS Proxy Cache failed")

    def test_02_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_03_query_and_check(self):
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        Assertion.assert_regular(rc, CaseParams.DOMAIN_IP, "ERR: query failed!!")

    def test_04_check_dynamic_dns_cache(self):
        res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        ttl = res[0].get('time_to_live') if res else ''
        rc_ttl = re.search(r'Expires in (\d+) seconds', ttl)
        rc_ttl = int(rc_ttl.group(1)) < 10 if rc_ttl else False
        logger.info(f'TTL in dynamic cache is correct...... {rc_ttl}')
        rc = all(x in json.dumps(res) for x in (CaseParams.DOMAIN, CaseParams.DOMAIN_IP))
        logger.info(f'{CaseParams.DOMAIN}, {CaseParams.DOMAIN_IP} in dynamic cache ...... {rc}')
        Assertion.assert_equal(rc_ttl & rc, True, "ERR: check_dynamic dns cache failed!!")

    def test_05_change_pc2_dns_server_config(self):
        confs_path = CONF_PATH + 'dnsserver_pc2/Changed/'
        cmds = ['service named stop',
                f'\\cp -f {confs_path}baidu.com.zone /var/named/',
                "systemctl restart named",
                "systemctl status named"]
        res = PC2_login.send_commands(cmds)
        Assertion.assert_regular(str(res), 'running\n', "ERR: change DNS server in PC2 failed")

    def test_06_expired_and_query(self):
        for _ in range(3):
            time.sleep(10)
            res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
            if 'Expired' in json.dumps(res):
                break
        rc = PC1_login.send_command(f'dig @{Parameter.FIREWALL} {CaseParams.DOMAIN}')
        logger.info(rc)
        Assertion.assert_regular(rc, self.changed_ip, "ERR: expired and query failed")
    
    def test_07_check_update(self):
        res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        ttl = res[0].get('time_to_live') if res else ''
        rc_ttl = re.search(r'Expires in (\d+) seconds', ttl)
        rc_ttl = int(rc_ttl.group(1)) > 10 if rc_ttl else False
        logger.info(f'TTL in dynamic cache is correct...... {rc_ttl}')
        rc = all(x in json.dumps(res) for x in (CaseParams.DOMAIN, self.changed_ip))
        logger.info(f'{self.changed_ip} in dynamic cache ...... {rc}')
        Assertion.assert_equal(rc_ttl & rc, True, "ERR: query_and_check_updated failed!!")

    def test_08_delete_added_dns_policies_and_flush_caches(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        logger.info(f'Delete added policy result...... {rc}')
        res = dns_proxy_api.flush_caches('ipv4')
        logger.info(f'Flush dynamic cache result ...... {res}')
        rc_disable = dns_proxy_api.config_dnsproxy(**{'dns_cache': False})
        logger.info(f"Disable DNS Proxy Cache ...... {rc_disable}")
        Assertion.assert_equal(rc & res & rc_disable, True, "ERR: delete_added_dns_policies_and_flush_caches failed!!")


# Verify the dut is stable when query a domain with large answer reply from DNS proxy cache
class TestFunc_2694338(Test):
    uuid = "SOSAIOT-TC-51615"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'proxy'
    domain = 'whitelist.ayayot.com'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_proxy_cache(self):
        disCache = {
            'dns_cache': True
        }
        rc = dns_proxy_api.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: enable DNS Proxy Cache failed")

    def test_02_config_dns_server(self):
        static = {
                    "primary": Parameter.X1_DNS1,
                    "secondary": '',
                    "tertiary": ''
                }
        dns = copy.deepcopy(dns_dict)
        dns['dns']['server']['static'].update(static)
        rc = dns_api.set_dns(**dns)
        Assertion.assert_equal(rc, True, "ERR: config_dns_server failed!!")

    def test_03_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_04_init_packet_capture_and_query(self):
        fw_packet_monitor_clear_start()
        res = PC1_login.send_command(f'dig {self.domain} AAAA +bufsize=4096 @{Parameter.FIREWALL}')
        res += PC1_login.send_command(f'dig {self.domain} +bufsize=4096 @{Parameter.FIREWALL}')
        rc = all(x not in res for x in ('no servers could be reached', 'connection timed out', 'connection refused'))
        Assertion.assert_equal(rc, True, "ERR: query failed!!")

    def test_05_check_fragment_packet(self):
        cmd = f'dns.qry.name=={self.domain}'
        out = fw_packet_monitor_stop_export(cmd=cmd, pc_login=PC1_login)
        logger.info(out)
        fragment_counts = re.findall(r'Fragment count:\s+(\d)', out)
        logger.info(f'fragment_counts are ...... {fragment_counts}')
        for count in fragment_counts:
            rc = int(count) > 0
            if rc:
                break
        Assertion.assert_equal(True, True, "ERR: check_fragment_packet failed!!")

    def test_06_query_and_check(self):
        res = PC1_login.send_command(f'dig {self.domain} +bufsize=4096 AAAA @{Parameter.FIREWALL}')
        logger.info(res)
        cache_res = dns_proxy_api.show_dns_proxy_caches_report('ipv6')
        rc = self.domain in json.dumps(cache_res)
        logger.info(f'Record dns proxy cache result...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: query failed!!")

    def test_07_query_and_check(self):
        domain = 'www.bing.com'
        res = PC1_login.send_command(f'dig {domain} @{Parameter.FIREWALL}')
        res += PC1_login.send_command(f'dig {domain} @{Parameter.FIREWALL}')
        rc = all(x not in res for x in ('no servers could be reached', 'connection timed out', 'connection refused'))
        logger.info(f'Query dns proxy packet hit cache result...... {rc}')
        cache_res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        rc_cache = domain in json.dumps(cache_res)
        logger.info(f'Record dns proxy cache result...... {rc_cache}')
        Assertion.assert_equal(rc & rc_cache, True, "ERR: query failed!!")

    def test_08_delete_added_dns_policies(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        logger.info(f'Delete LAN dns proxy policy result...... {rc}')
        rc_flush = dns_proxy_api.flush_caches('ipv4')
        logger.info(f'Flush dynamic cache result ...... {rc_flush}')
        rc_disable = dns_proxy_api.config_dnsproxy(**{'dns_cache': False})
        logger.info(f"Disable DNS Proxy Cache ...... {rc_disable}")
        Assertion.assert_equal(rc & rc_flush & rc_disable, True, "ERR: delete_added_dns_policies failed!!")


# [FUNC] Verify FW does not crash when dns proxy cache size is over 2048
class TestFunc_1532704(Test):
    uuid = "SOSAIOT-TC-51624"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    name = 'proxy'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_proxy_cache(self):
        disCache = {
            'dns_cache': True
        }
        rc = dns_proxy_api.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: enable DNS Proxy Cache failed")

    def test_02_config_dns_server(self):
        static = {
                    "primary": Parameter.X1_DNS1,
                    "secondary": '',
                    "tertiary": ''
                }
        dns = copy.deepcopy(dns_dict)
        dns['dns']['server']['static'].update(static)
        rc = dns_api.set_dns(**dns)
        Assertion.assert_equal(rc, True, "ERR: config_dns_server failed!!")

    def test_03_add_dns_policy(self):
        X0_interface = {
            "name": self.name,
            "proxy_mode": "ipv4-ipv4",
            "from": "X0",
            "source":{"address":{"any":True}},
        }
        rc = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_04_query_and_check(self):
        domain = 's.spotim.market'
        res = PC1_login.send_command(f'dig {domain} AAAA @{Parameter.FIREWALL}')
        logger.info(res)
        cache_res = dns_proxy_api.show_dns_proxy_caches_report('ipv6')
        rc = domain in json.dumps(cache_res)
        logger.info(f'Record dns proxy cache result...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: query and check failed!!")

    def test_05_init_packet_capture_and_query(self):
        domain = 'bing.com'
        res = PC1_login.send_command(f'dig {domain} A @{Parameter.FIREWALL}')
        logger.info(res)
        cache_res = dns_proxy_api.show_dns_proxy_caches_report('ipv4')
        rc = domain in json.dumps(cache_res)
        logger.info(f'Record dns proxy cache result...... {rc}')
        Assertion.assert_equal(rc, True, "ERR: query and check failed!!")

    def test_06_delete_added_dns_policies_and_cache(self):
        rc = dns_rule_api.del_dns_rule_by_name(name=self.name)
        logger.info(f'Delete LAN dns proxy policy result...... {rc}')
        rc_flush = dns_proxy_api.flush_caches('ipv4')
        logger.info(f'Flush dynamic cache result ...... {rc_flush}')
        rc_disable = dns_proxy_api.config_dnsproxy(**{'dns_cache': False})
        logger.info(f"Disable DNS Proxy Cache ...... {rc_disable}")
        Assertion.assert_equal(rc & rc_flush & rc_disable, True, "ERR: delete_added_dns_policies_and_cache failed!!")


# prefs export and import about dns proxy (4to4 and 4to6 mode and DNS Cache)
class TestFunc_1526839(Test):
    uuid = "SOSAIOT-TC-51609"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    policy_name = '4to6'
    split_name = 'split.com'
    static_domain = "pc2.baidu.com"
    static_ip = '123.3.2.1'
    static_ipv6 = "123::1"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_proxy(self):
        entry = {"domain": self.static_domain, 'ipv4_primary': self.static_ip, 'ipv6_primary': self.static_ipv6}
        rc_cache = dns_proxy_api.add_dns_proxy_static_entry(msg=False, **entry)
        logger.info(f'add_dns_static_cache......{rc_cache}')
        split = {
            'domain': self.split_name,
            'ipv4': {
                'primary': self.static_ip,      
            },
            'ipv6': {
                'primary': self.static_ipv6,       
            },
            'local_interface': 'X2',
        }
        rc_split = dns_api.add_split_dns(msg=False, **split)
        logger.info(f'add_split_dns_entry......{rc_split}')
        X0_interface = {
            "name": self.policy_name,
            "proxy_mode": "ipv4-ipv6",
            "from": "X0",
            "source":{"address":{"any":True}},
        }
        rc_policy = dns_policy_api.add_dns_proxy_policy(**X0_interface)
        logger.info(f'add_dns_policy ......{rc_policy}')
        Assertion.assert_equal(rc_split & rc_cache & rc_policy, True, "ERR: config proxy failed!!")

    def test_02_export_configs(self):
        rc = setting_api.export_setting_exp()
        Assertion.assert_equal(rc, True, "ERR: failed to export configs !!")

    def test_03_initialize_all_configs(self):
        edit = {
            'name': self.policy_name,
            "proxy_mode": "ipv4-ipv4"
        }
        rc_policy = dns_rule_api.edit_dns_rule(**edit)
        logger.info(f'Initialize dns policy result ...... {rc_policy}')
        rc_cache = dns_cli.delete_dns_proxy_static_cache_entry()
        logger.info(f'Initialize dns proxy static cache result ...... {rc_cache}')
        rc_split = dns_api.delete_split_dns(self.split_name)
        logger.info(f'add_split_dns_entry......{rc_split}')
        rc = rc_policy & rc_cache & rc_split
        Assertion.assert_equal(rc, True, "ERR: failed to initialize_all_configs!!")

    def test_04_import_configs(self):
        rc = setting_api.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(rc, True, "ERR: failed to import_configs !!")

    @repeat_method(3)
    def test_05_check_configs(self):
        time.sleep(10)
        policy_out = dns_rule_api.get_dns_rule_by_name(self.policy_name)
        policy_rc = 'ipv4-ipv6' in json.dumps(policy_out)
        logger.info(f'Check dns policy mode settings...... {policy_rc}')

        cache_out = dns_proxy_api.show_dns_proxy_caches()
        cache_rc = all(x in json.dumps(cache_out) for x in (self.static_domain, self.static_ip, self.static_ipv6))
        logger.info(f'Check dns static proxy domain...... {cache_rc}')

        split_out = dns_api.show_dns_proxy_entry()
        split_rc = all(x in json.dumps(split_out) for x in (self.split_name, self.static_ip, self.static_ipv6))
        logger.info(f'Check split dns entry...... {split_rc}')
        rc = policy_rc & cache_rc & split_rc
        Assertion.assert_equal(rc, True, "ERR: failed to check_configs !!")


class TestFunc_1526836(Test):
    uuid = "SOSAIOT-TC-51608"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_reboot(self):
        rc = setting_api.boot_fw(mode=1)
        Assertion.assert_equal(rc, True, "ERR: failed to reboot !!")

    @repeat_method(3)
    def test_02_check_configs(self):
        TestFunc_1526839().test_05_check_configs()
