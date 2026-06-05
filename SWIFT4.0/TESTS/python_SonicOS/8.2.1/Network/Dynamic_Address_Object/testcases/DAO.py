from definition.settings import *
DAOTest = "DAOtest"
FQDNTest = "FQDNtest"
DAO_host_ip = '13.0.0.12'


class TestDAO_3229068(Test):
    uuid = "SOSAIOT-TC-57909"
    description= show_testcase_info(TESTPLAN, '3229068', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3229068')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_DAO(self):
        logger.info(Parameter.PC1_ETH0_MAC)
        ao_var = {
            "object_type": "mac",
            "name": DAOTest,
            "zone": "LAN",
            "value": Parameter.PC1_ETH0_MAC,
            "multi_homed": True,
        }
        rc = ao_obj.config_addressobject(**ao_var)
        Assertion.assert_equal(rc, True, "ERR:add ao failed")
 
    def test_02_check_DAO(self):
        flag = False
        try:
            rc = ao_obj.get_DAO_info( DAOTest )
            match = re.search(PC1_ETH0_IP, rc['data']['daoInfo'], re.I)
            if match:
                flag = True
        except:
            logger.error("get DAO info failed {}".format(rc))
        Assertion.assert_equal(flag, True, "ERR:check DAO failed")

    def test_03_delete_DAO(self):
        ao_var = {
            'object_type': 'mac',
            'object_path': 'name',
            'ip_type': 'ipv4',
            'object_name_uuid': DAOTest,
        }
        rc = ao_obj.delete_addressobject( **ao_var )
        Assertion.assert_equal(rc, True, "ERR:Delete DAO failed")


class TestDAO_3229100(Test):
    uuid = "SOSAIOT-TC-57939"
    description= show_testcase_info(TESTPLAN, '3229100', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3229100')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_DAO(self):
        logger.info(Parameter.PC1_ETH0_MAC)
        ao_var = {
            "object_type": "mac",
            "name": DAOTest,
            "zone": "LAN",
            "value": Parameter.PC1_ETH0_MAC,
            "multi_homed": True,
        }
        rc = ao_obj.config_addressobject(**ao_var)
        Assertion.assert_equal(rc, True, "ERR:add ao failed")

    def test_02_add_access_rule(self):
        flag = False
        ret = os.popen('route add -host {} gw {}'.format(PC2_ETH0_IP, FIREWALL)).read()
        logger.info(ret)
        output = os.popen("ping {} -c 5".format(PC2_ETH0_IP)).read()
        logger.info(output)
        if '100% packet loss' not in output:
            flag = True
        else:
            logger.info('ERROR: Ping failed before add access rule...')
        access_rules = {
            "uuid": "00000000-0000-0001-0700-22222",
            "name": "my_access_rule",
            "enable": True,
            "from": "LAN",
            "to": "WAN",
            "action": "deny",
            "source": {
                "address": {
                    "name": DAOTest
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "any": True
            },
            "destination": {
                "address": {
                    "any": True
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }
        rc = access_rule_obj.config_accessrule(**access_rules)
        Assertion.assert_equal(rc, True, "ERR: add access rule failed")

    def test_03_Verify_traffic(self):
        flag = False
        output = os.popen("ping {} -c 5".format(PC2_ETH0_IP)).read()
        logger.info(output)
        if '100% packet loss' in output:
            flag = True
        else:
            logger.info('ERROR:Ping success after add access rule...')
        Assertion.assert_equal(flag, True, "ERR: Verify traffic failed after add access rule")

    def test_04_remove_access_rule(self):
        rc = access_rule_obj.delete_accessrule_by_name(name = 'my_access_rule')
        Assertion.assert_equal(rc, True, "ERR: remove access rule failed")

    def test_05_delete_DAO(self):
        ret = os.popen('route del -host {} gw {}'.format(PC2_ETH0_IP, FIREWALL)).read()
        logger.info(ret)
        ao_var = {
            'object_type': 'mac',
            'object_path': 'name',
            'ip_type': 'ipv4',
            'object_name_uuid': DAOTest,
        }
        rc = ao_obj.delete_addressobject( **ao_var )
        Assertion.assert_equal(rc, True, "ERR:Delete DAO failed")


class TestDAO_3229079(Test):
    uuid = "SOSAIOT-TC-57920"
    description= show_testcase_info(TESTPLAN, '3229079', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3229079')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_FQDN_AO(self):
        ao_var = {
            "object_type": "fqdn",
            "name": FQDNTest,
            "zone": "WAN",
            "value": "www12.limitFQDN.com",
            "dns_ttl": 0,
        }
        rc = ao_obj.config_addressobject(**ao_var)
        Assertion.assert_equal(rc, True, "ERR:add fqdn ao failed")

    @repeat_method(10) 
    def test_02_check_FQDN(self):
        time.sleep(15)
        flag = False
        try:
            rc = ao_obj.get_DAO_info( FQDNTest )
            logger.info(rc)
            match = re.search(f'Host: {DAO_host_ip}; TTL=', rc['data']['daoInfo'], re.I)
            if match:
                flag = True
        except:
            logger.error("get DAO info failed {}".format(rc))
        Assertion.assert_equal(flag, True, "ERR:check DAO failed")

    def test_03_delete_FQDN(self):
        ao_var = {
            'object_type': 'fqdn',
            'object_path': 'name',
            'ip_type': 'ipv4',
            'object_name_uuid': FQDNTest,
        }
        rc = ao_obj.delete_addressobject( **ao_var )
        Assertion.assert_equal(rc, True, "ERR:Delete DAO failed")


@paramunittest.parametrized(
    {'tcid': '3229086', 'uuid': '3229086'},
    {'tcid': '3229088', 'uuid': '3229088'},
)
class TestDAO_3229086_3229088(Test):
    def setParameters(self, tcid, uuid):
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_AO(self):
        logger.info(Parameter.PC1_ETH0_MAC)
        ao_var1 = {
            "object_type": "mac",
            "name": DAOTest,
            "zone": "LAN",
            "value": Parameter.PC1_ETH0_MAC,
            "multi_homed": True,
        }
        rc1 = ao_obj.config_addressobject(**ao_var1)
        ao_var2 = {
            "object_type": "fqdn",
            "name": FQDNTest,
            "zone": "WAN",
            "value": "www12.limitFQDN.com",
            "dns_ttl": 0,
        }
        rc2 = ao_obj.config_addressobject(**ao_var2)
        ret = system_obj.diag_dns_name_lookup(cmd = "nslookup baidu.com").split("\n")
        logger.info(ret)
        Assertion.assert_equal(rc1 & rc2, True, "ERR:add ao failed")

    def test_02_add_access_rule(self):
        access_rules = {
            "uuid": "00000000-0000-0001-0700-22222",
            "name": "my_access_rule",
            "enable": True,
            "from": "LAN",
            "to": "WAN",
            "action": "deny",
            "source": {
                "address": {
                    "name": DAOTest
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "name": "HTTP"
            },
            "destination": {
                "address": {
                    "name": FQDNTest
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }
        rc = access_rule_obj.config_accessrule(**access_rules)
        Assertion.assert_equal(rc, True, "ERR: add access rule failed")

    @repeat_method(8)
    def test_03_check_result(self):
        if self.tcid == '30':
            flag = False
            ret = os.popen('route add -host {} gw {}'.format(DAO_host_ip, FIREWALL)).read()
            cmd = "sed -i '/search openstacklocal/anameserver {}' /etc/resolv.conf".format(PC2_ETH0_IP);
            ret = os.popen( cmd ).read()
            edit_log = {
                "log": {
                    "event": [
                        {
                            "id": 524,
                            "name": "Web Request Drop",
                            "category": "Network",
                            "group": "Network Access",
                            "priority_level": "alert",
                            "log_monitor": {"redundancy_interval":0},
                            "email_alert": {},
                            "syslog": {"redundancy_interval": 60},
                            "ipfix": {},
                            "event_profile": { "syslog_server_profile": 0 },
                            "log_digest": False,
                            "color": { "hex": "0x001E90FF" },
                            "alert_email": {},
                        }
                    ]
                }
            }
            rc2 = log_settings.edit_event( event_id='524', **edit_log )
            log.clear_log()
            rc4 = os.system("timeout 10 wget http://www12.limitFQDN.com")
            rc5 = log.show_log()
            logger.info(rc5)
            for log_entry in rc5:
                if "Web access Request dropped" in log_entry['message']:
                    flag = True
                    break
            Assertion.assert_equal(flag, True, "ERR: Check result failed")
        elif self.tcid == '29':
            rules = access_rule_obj.get_access_rule_statistics()
            for rule in rules:
                if rule['source'] == DAOTest and rule['destination'] == FQDNTest \
                    and rule['enable'] == 'enable':
                    flag = True
            Assertion.assert_equal(flag, True, "ERR: Check result failed")

    def test_04_remove_access_rule(self):
        rc = access_rule_obj.delete_accessrule_by_name(name = 'my_access_rule')
        Assertion.assert_equal(rc, True, "ERR: remove access rule failed")

    def test_05_delete_AO(self):
        ao_var1 = {
            'object_type': 'mac',
            'object_path': 'name',
            'ip_type': 'ipv4',
            'object_name_uuid': DAOTest,
        }
        rc1 = ao_obj.delete_addressobject( **ao_var1 )
        ao_var2 = {
            'object_type': 'fqdn',
            'object_path': 'name',
            'ip_type': 'ipv4',
            'object_name_uuid': FQDNTest,
        }
        rc2 = ao_obj.delete_addressobject( **ao_var2 )
        Assertion.assert_equal(rc1 & rc2, True, "ERR:Delete AO failed")


class TestDAO_3229074(Test):
    uuid = "SOSAIOT-TC-57915"
    description= show_testcase_info(TESTPLAN, '3229074', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3229074')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_AO(self):
        logger.info(Parameter.PC1_ETH0_MAC)
        ao_var1 = {
            "object_type": "mac",
            "name": DAOTest,
            "zone": "LAN",
            "value": Parameter.PC1_ETH0_MAC,
            "multi_homed": True,
        }
        rc1 = ao_obj.config_addressobject(**ao_var1)
        Assertion.assert_equal(rc1, True, "ERR: add DAO failed")

    def test_02_get_DAO_info(self):
        rc = ao_obj.get_DAO_info(DAOTest)
        logger.info(rc)
        Assertion.assert_regular(str(rc), r"IPv4:.*Host: 192\.168\.168\.169", 'ERR: Check DAO display ip')

    def test_03_delete_AO(self):
        ao_var1 = {
            'object_type': 'mac',
            'object_path': 'name',
            'ip_type': 'ipv4',
            'object_name_uuid': DAOTest,
        }
        rc1 = ao_obj.delete_addressobject( **ao_var1 )
        Assertion.assert_equal(rc1, True, "ERR: del DAO failed")


# class TestDAO_38(Test):
#     uuid = '1510314'
#     description= show_testcase_info(TESTPLAN, '38', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '38')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_add_AO(self):
#         ao_var2 = {
#             "object_type": "fqdn",
#             "name": FQDNTest,
#             "zone": "WAN",
#             "value": "www12.limitFQDN.com",
#             "dns_ttl": 0,
#         }
#         rc2 = ao_obj.config_addressobject(**ao_var2)
#         ret = system_obj.diag_dns_name_lookup(cmd = "nslookup baidu.com").split("\n")
#         logger.info(ret)
#         Assertion.assert_equal(rc2, True, "ERR:add ao failed")

#     def test_02_get_DAO_info(self):
#         rc = ao_obj.get_DAO_info(FQDNTest)
#         logger.info(rc)
#         Assertion.assert_regular(str(rc), r"IPv4:.*Host: 13\.0\.0\.12", 'ERR: Check DAO display ip')

#     def test_03_stop_dns_server(self):
#         PC2_login.send_command('service named stop')
#         rc = PC2_login.send_command('service named status')
#         Assertion.assert_regular(str(rc), r"named is stopped", 'ERR: Check DAO display ip')

#     def test_04_restart_FW(self):
#         rc = restart.restart_now()
#         Assertion.assert_equal(rc, True, "ERR: restart FW failed")

#     def test_05_get_DAO_info(self):
#         rc = ao_obj.get_DAO_info(FQDNTest)
#         logger.info(rc)
#         Assertion.assert_not_regular(str(rc), r"IPv4:.*Host: 13\.0\.0\.12", 'ERR: Check DAO display ip')

#     def test_06_start_dns_server(self):
#         PC2_login.send_command('service named start')
#         rc = PC2_login.send_command('service named status')
#         Assertion.assert_regular(str(rc), r"server is up and running", 'ERR: Check DAO display ip')

#     def test_07_get_DAO_info(self):
#         time.sleep(20)
#         ao_obj.resolve_all()
#         rc = ao_obj.get_DAO_info(FQDNTest)
#         logger.info(rc)
#         Assertion.assert_regular(str(rc), r"IPv4:.*Host: 13\.0\.0\.12", 'ERR: Check DAO display ip')


class TestDAO_3229097(Test):
    uuid = "SOSAIOT-TC-57936"
    description= show_testcase_info(TESTPLAN, '3229097', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3229097')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_AO(self):
        ao_var2 = {
            "object_type": "fqdn",
            "name": FQDNTest,
            "zone": "WAN",
            "value": "www12.limitFQDN.com",
            "dns_ttl": 0,
        }
        rc2 = ao_obj.config_addressobject(**ao_var2)
        ret = system_obj.diag_dns_name_lookup(cmd = "nslookup baidu.com").split("\n")
        logger.info(ret)
        Assertion.assert_equal(rc2, True, "ERR:add ao failed")

    def test_02_add_access_rule(self):
        access_rules = {
            "uuid": "00000000-0000-0001-0700-22222",
            "name": "my_FQDNaccess_rule",
            "enable": True,
            "from": "LAN",
            "to": "WAN",
            "action": "deny",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "name": "HTTP"
            },
            "destination": {
                "address": {
                    "name": FQDNTest
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }
        rc = access_rule_obj.config_accessrule(**access_rules)
        Assertion.assert_equal(rc, True, "ERR: add access rule failed")

    def test_03_get_ipv4_acl(self):
        rc = access_rule_obj.get_accessrule()
        logger.info(rc)
        Assertion.assert_regular(str(rc), r'name.*my_FQDNaccess_rule.*', "ERR: add access rule failed")
        
    def test_04_get_ipv4_acl(self):
        rc = access_rule_obj_ipv6.get_accessrule_ipv6()
        logger.info(rc)
        Assertion.assert_not_regular(str(rc), r'name.*my_FQDNaccess_rule.*', "ERR: add access rule failed")