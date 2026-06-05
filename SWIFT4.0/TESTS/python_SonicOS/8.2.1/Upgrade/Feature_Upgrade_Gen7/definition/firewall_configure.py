from definition.settings import *


class FWFunctionConfigure:
    cfs_object_name1 = 'auto_cfs_object_01'

    def cfs_configure(self):
        object_dict = {
            "object_name": self.cfs_object_name1,
            "domain": ["baidu.com"]
        }
        output1, msg = cfoobjectapi.configure_cfo_object(msg=True, **object_dict)
        if 'Already exists' in str(msg):
            output1 = True

        profile_dict = {
            "content_filter": {
                "profile": [{
                    "name": "CFS Default Profile",
                    "uri_list": {
                        "forbidden": [
                            {
                                "name": self.cfs_object_name1
                            }
                        ],
                        "search_order": "allowed-first",
                        "forbidden_operation": "block"
                    },
                    "categories": "default",
                    "https_filtering": False,
                    "smart_filter": False,
                    "safe_search": False,
                    "threat_api": False,
                    "google_force_safe_search": False,
                    "youtube_restrict_mode": False,
                    "bing_force_safe_search": False,
                    "consent": {
                        "required": False
                    },
                    "custom_header": {
                        "insertion": False
                    }
                }]
            }
        }
        output2 = cfoprofileapi.edit_cfo_profile_by_name(name="CFS Default Profile", **profile_dict)
        logger.info(f'add cfo object result: {output1}, edit profile result: {output2}')
        return output1 & output2

    def spyware_configure(self):
        antispy_json = {
            'enable': True,
            'high_danger_prevent': True,
            'medium_danger_prevent': True,
            'low_danger_prevent': True,
            'high_danger_detect': True,
            'medium_danger_detect': True,
            'low_danger_detect': True,
        }
        output = spywareapi.config_antispyware(**antispy_json)
        return output

    def gav_configure(self):
        gav_dict = {
            'enable_GAV': True,
            'inbound_ftp': True,
        }
        output = gavapi.config_gav(**gav_dict)
        return output

    def ips_configure(self):
        enable_ips_dict = {
            "intrusion_prevention": {
                "enable": True,
                "signature_group": {
                    "high_priority": {
                        "detect_all": True,
                        "log_redundancy": {},
                        "prevent_all": True
                    },
                    "low_priority": {
                        "detect_all": True,
                        "log_redundancy": {
                            "value": 60
                        },
                        "prevent_all": True
                    },
                    "medium_priority": {
                        "detect_all": True,
                        "log_redundancy": {},
                        "prevent_all": True
                    }
                }
            }
        }
        output = ipsapi.config_IPS_global(**enable_ips_dict)
        return output

    def zones_configure(self):
        zone_dict = {
            "zones": [
                {
                    "name": CaseParams.custom_zone_name,
                    "security_type": "public",
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
        output, msg = zonesapi.add_zone_object(msg=True, **zone_dict)
        if not output:
            output = True if 'Already exists' in json.dumps(msg) else False
        return output

    def interface_configure(self):
        x2_dict = {
            'if': 'X2',
            'zone': CaseParams.custom_zone_name,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_snmp': True,
        }
        output = interfaceapi.config_interface(**x2_dict)
        return output

    def nat_configure(self):
        logger.info(" {} ".center(50, '-').format('PC4 Route Configure'))
        cmds = [f'route add -net {Parameter.X0_SUBNET}/24 gw {Parameter.X1_IP}',
                'ip -4 r']
        output = PC4_login.send_commands(cmds)
        res4 = True if f'{Parameter.X0_SUBNET}/24 via {Parameter.X1_IP}' in output else False

        res3 = False
        getres = accessruleapi.get_accessrule_via_zones(srczone='WAN', dstzone='LAN')
        try:
            for rule in getres['access_rules']:
                if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'deny':
                    logger.info(f'get target rule successful: {rule}')
                    acl_dict = copy.deepcopy(default_acl_dict)
                    acl_dict.update({"from": "WAN", "to": "LAN"})
                    res3 = accessruleapi.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                    break
            else:
                logger.info('Default Access Rule is allow, not need configure')
                res3 = True
        except exception as e:
            logger.info(f'get wan to lan acl failed: {repr(e)}')

        ao_dict = {
            "object_type": "host",
            "name": PC2_ETH1_IP,
            "zone": "LAN",
            "value": PC2_ETH1_IP
        }
        res1, msg = aoapi.config_addressobject(msg=True, **ao_dict)
        if 'Already exists' in str(msg):
            res1 = True
        nat_dict = {
            "nat_policies": [
                {
                    "ipv4": {
                        "uuid": "00000000-0000-0001-0800-2cb8ed6d8008",
                        "name": CaseParams.custom_nat_name,
                        "enable": True,
                        "comment": "",
                        "dns_doctoring": False,
                        "inbound": "X1",
                        "outbound": "any",
                        "source": {
                            "any": True
                        },
                        "translated_source": {
                            "original": True
                        },
                        "destination": {
                            "name": "X1 IP"
                        },
                        "translated_destination": {
                            "name": PC2_ETH1_IP
                        },
                        "service": {
                            "any": True
                        },
                        "translated_service": {
                            "original": True
                        }
                    }
                }
            ]
        }
        res2, msg = natpolicyapi.add_nat_policy(msg=True, **nat_dict)
        if 'Already exists' in str(msg):
            res2 = True
        logger.info(f'add ao: {res1}, add nat policy: {res2}, edit acl: {res3}, add route: {res4}')
        return res1 & res2 & res3 & res4

    def route_configure(self):
        ao_dict = {
            "object_type": "host",
            "name": PC4_ETH1_IP,
            "zone": "WAN",
            "value": PC4_ETH1_IP
        }
        res1, msg = aoapi.config_addressobject(msg=True, **ao_dict)
        if 'Already exists' in str(msg):
            res1 = True
        res2, msg = routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
        if 'Already exists' in str(msg):
            res2 = True
        logger.info(f'add wan ao: {res1}, add route policy: {res2}')
        return res1 & res2

    def access_rules_configure(self):
        output, msg = accessruleapi.add_accessrule(msg=True, **wan_lan_acl_dict)
        if 'Already exists' in str(msg):
            output = True
        return output

    def app_rules_configure(self):
        match_object = {
            "object_type": "http-host",
            "name": CaseParams.custom_march_name,
            "match_type": "partial",
            "input_representation": "alphanumeric",
            "negative_matching": False,
            "content_entry": [{"content_entry": PC4_ETH1_IP}]
        }
        res2, msg = matchobjectapi.config_matchobject(msg=True, **match_object)
        if 'Already exists' in str(msg):
            res2 = True

        apprule_object = {
            "name": CaseParams.custom_apprule_name,
            "enable": True,
            "type": {"http": "client"},
            "source": {
                "address": {"any": True},
                "service": {"any": True}
            },
            "destination": {
                "address": {"any": True},
                "service": {"name": "HTTP"}
            },
            "exclusion": {"address": {}},
            "match_object": {'included': CaseParams.custom_march_name, 'excluded': ''},
            "action_object": "Reset/Drop",
            "users": {
                "included": {"all": True},
                "excluded": {}
            },
            "schedule": {"always_on": True},
            "flow_reporting": False,
            "logging": True,
            "log": {'individual': False, 'redundancy': {'global': True}},
            "connection_side": "client",
            "direction": {
                "basic": "outgoing"
            }
        }
        res3, msg = appruleapi.add_apprule_object(msg=True, **apprule_object)
        if 'Already exists' in str(msg):
            res3 = True
        logger.info(f'add march object: {res2}, add app rule: {res3}')
        return res2 & res3

    def dns_configure(self):
        dns_setting_dict = {
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
        output = dnssettingapi.set_dns(**dns_setting_dict)
        return output

    def syslog_configure(self):
        syslog_dict = {
            'name': PC4_ETH1_IP,
            'port': 514,
            'profile': 0,
            'format': 'default',
            "data_rate_limiting": {
                "enabled": True,
                "maximum_events": {
                    "value": 1000
                }
            },
            "event_rate_limiting": {
                "enabled": True,
                "maximum_bytes": {
                    "value": 10000000
                }
            }
        }
        output, msg = syslogsettingsapi.add_syslog_server(msg=True, **syslog_dict)
        if 'Already exists' in str(msg):
            output = True
        return output

    def time_configure(self):
        time_dict = {
            "time": {
                "use_ntp": True,
                "time_zone": "china,philippines",
                "daylight_savings": True,
                "only_custom_ntp": False,
                "ntp_update_interval": 30
            }
        }
        output = timeapi.set_time(**time_dict)
        return output

    def logging_configure(self):
        log_dict = {
            "log": {
                "event": [
                    {
                        "id": 602,
                        "name": "DNS Allow",
                        "priority_level": "alert",
                        "log_email": {},
                        "log_monitor": {
                            "redundancy_interval": 123
                        },
                        "email_alert": {},
                        "syslog": {},
                        "trap": {},
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": False,
                        "color": {
                            "hex": "0x00000000"
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        output = logsettingsapi.edit_event(event_id='602', **log_dict)
        return output

    def snmp_configure(self):
        output1 = snmpapi.enable_snmp()
        logger.info(f'enable snmp in fw: {output1}')

        x2_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'mgmt_snmp': True
        }
        output2 = interfaceapi.config_interface(**x2_dict)
        logger.info(f'enable mgmt snmp in x2: {output2}')

        snmp_user_group = "snmpgGroup"

        snmp_user_dict = {
            "user_name": "snmpUser",
            "user_security": "",
            "user_group": snmp_user_group,
        }

        snmp_acc_dict = {
            "access_name": "snmpAcc",
            "access_security": "",
            "access_view": "root",
            "access_group": snmp_user_group,
        }

        logger.info("Add SNMP config")
        rc_gp = snmpapi.add_snmp_group(name=snmp_user_group)
        logger.info(f"Add SNMP group result = {rc_gp}")
        rc_user = snmpapi.snmp_user_add(**snmp_user_dict)
        logger.info(f"Add SNMP user result = {rc_user}")
        rc_acc = snmpapi.snmp_access_add(**snmp_acc_dict)
        logger.info(f"Add SNMP access result = {rc_acc}")
        logger.info(f'rc_gp: {rc_gp}, rc_user: {rc_user}, rc_acc: {rc_acc}')

        resp = snmpapi.show_snmp()
        if resp:
            snmp_v3 = resp["snmp"]
            snmp_v3["snmp3"]["mandatory"] = True
            rc_set = snmpapi.snmp_base_settings(**snmp_v3)
            rc_enable = snmpapi.enable_snmp()
            logger.info(f'rc_set: {rc_set}, rc_enable: {rc_enable}')
        return output1 & output2


    def dhcp_server_configure(self):
        output1 = dhcpserverapi.config_dhcp_server_settings(**dhcp_seting_dict)

        dhcp_dict = {
            "dhcp_server":
                {"ipv4": {
                    "scope": {
                        "dynamic": [{
                            "from": "192.168.2.80",
                            "to": "192.168.2.85",
                            "enable": True,
                            "lease_time": 60,
                            "default_gateway": "",
                            "netmask": "255.255.255.0",
                            "comment": "",
                            "domain_name": "",
                            "dns": {"server": {"inherit": True}},
                        }
                    ]}}}}
        output2, msg = dhcpserverapi.add_dhcp_server_scope_dynamic(msg=True, **dhcp_dict)
        if 'Already exists' in str(msg):
            output2 = True
        logger.info(f'disable dhcp: {output1}, add dhcp scope: {output2}')
        return output1 & output2




