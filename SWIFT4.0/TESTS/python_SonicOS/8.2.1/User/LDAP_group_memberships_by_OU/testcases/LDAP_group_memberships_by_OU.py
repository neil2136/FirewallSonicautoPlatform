from definition.settings import *
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')


class ldap_config(Test):
    uuid = 'NonTC'
    
    def test_01_configure_dns(self):
        dns_dict = {
            "dns": {
                "server": {
                    "inherit": False,
                    "static": {
                        "primary": "192.168.168.85"
                    }
                }
            }
        }
        rc = dnssettingapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_02_config_ldap_server(self):
        add_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
            'bind': 'distinguished_name',
            'distinguished_name': 'test',
            'bind_password': 'password',
            'referred_bind_with_account': 'other-servers',
            'primary_domain': 'os-autosnwl.com',
            'users_tree': ['Users', 'os-autosnwl.com/Users'],
            'user_groups_tree': ['os-autosnwl.com/Users'],
            'directory': True,
            'schema': 'microsoft-active-directory/network-information-service'
        }
        ldap.add_ldap_server(**add_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "OS-WSV.os-autosnwl.com"', "ERR: Failed to config LDAP Server")

    def test_03_config_auth_method_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR: LDAP method is not selected successfully")

    def test_04_add_CA_cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = certobj.import_ca_cert(file=ca_cert)
        Assertion.assert_equal(rc, True, 'ERR: Add CA Cert failed')
    
    def test_05_create_sslvpn_address_object(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_range",
            "zone": "SSLVPN",
            "value": "192.168.168.10,192.168.168.20"
        }
        address_objects.config_addressobject(**address_object)
        resp = address_objects.get_addressobject_by_name("sslvpn_range", "ipv4")
        Assertion.assert_regular(json.dumps(resp), '"name": "sslvpn_range"', "Err: failed to create address object")

    def test_06_sslserver_settings_with_port_enabled(self):
        ssl_vpn_server = {
            'port': 4433,
            'use_self_signed': True,
            'user_domain': 'LocalDomain',
            'web': True,
            'ssh': False,
            'session_timeout': 10,
            'default': True,
            'mschap': True,
            'inactivity_check': True
        }
        server_settings = sslvpnserver.edit_server_setting(**ssl_vpn_server)
        Assertion.assert_equal(server_settings, True, "Err: failed to config server settings")

    def test_07_enable_sslvpn_access(self):
        enable = {
            'WAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_08_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_09_add_all_ldap_users_to_sslvpn_services(self):
        member = {
            'action': 'add',
            'groupname': 'SSLVPN Services',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        user_local.group_member_of(**member)
        resp1 = user_local.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp1), '"name": "All LDAP Users"', 'ERR: All LDAP Users not added to SSLVPN Services')


class Test_LDAP_TSR_support(Test):
    uuid = "SOSAIOT-TC-77130"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825598')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    def test_02_download_tsr(self):
        rc = system_api.download_tsr()
        logger.info(rc)
        file_size = 0
        if os.path.exists('/tmp/techSupport'):
            file_size = os.path.getsize("/tmp/techSupport")
            logger.info("tsr file size is " + str(file_size))
            if file_size:
                pass
            else:
                Assertion.assert_equal(False, True, "ERR: Download tsr failed")
        else:
            Assertion.assert_equal(False, True, "ERR: Download tsr failed")

    def test_03_verify_tsr_for_ipv4_access_rule(self):
        flag = False 
        if os.path.exists("/tmp/techSupport"):
            tsr_content = os.popen('cat /tmp/techSupport').read()
            pattern = r"testgp1:(.*?)\-\-User Object Table\-\-"
            match = re.search(pattern, tsr_content, re.DOTALL)
            if match:
                captured_text = match.group(1).strip()
                logger.info("##########################")
                logger.info(captured_text)
                logger.info("##########################")
                if "LDAP location: shvl.com/qa" in captured_text:
                    flag = True
            else:
                logger.info("Not found the target tsr content part")
        else:
            logger.info("download tsr file failed")
        Assertion.assert_equal(flag, True, "ERR: Verify tsr failed")

    def test_04_delete_local_group(self):
        response = user_local.delete_local_group_no_domain("testgp1")
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Failed to delete local group")

class Test_LDAP_Restart_FW(Test):
    uuid = "SOSAIOT-TC-77138"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825604')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    def test_02_restart_firewall(self):
        cmds = ['restart']
        rc1 = fw_cli.do_cli_commands(cmds)

        time.sleep(30)

    def test_03_verify_local_group_after_reboot(self):
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    def test_04_delete_local_group(self):
        response = user_local.delete_local_group_no_domain("testgp1")
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Failed to delete local group")

class Test_LDAP_export_import_pref(Test):
    uuid = "SOSAIOT-TC-77128"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825597')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    def test_02_export_exp(self):
        res = settingObj.export_setting_exp()
        Assertion.assert_equal(res, True, 'ERR: export exp file failed.')

    def test_03_local_group(self):
        response = user_local.delete_local_group_no_domain("testgp1")
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Failed to delete local group")

    def test_04_import_exp(self):
        res = settingObj.import_setting_exp('/tmp/test.exp')
        Assertion.assert_equal(res, True, 'ERR: import exp file failed')

    def test_05_delete_local_group(self):
        response = user_local.delete_local_group_no_domain("testgp1")
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Failed to delete local group")

class Test_LDAP_memberships_set_by_OU_Can_be_enable_and_Disable(Test):
    uuid = "SOSAIOT-TC-77120"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1507158')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)

    def test_02_verify_local_group_membership(self):
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    def test_03_delete_local_group(self):
        response = user_local.delete_local_group_no_domain("testgp1")
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Failed to delete local group")

    def test_04_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                # "memberships_by_ldap_location": {
                #     "under_or_at": ''
                # },
                "name": "testgp1"
                # "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)

    def test_05_verify_local_group_membership(self):
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    def test_06_delete_local_group(self):
        add_local_group = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
        }
        rc = user_local.local_group(**add_local_group)

class Test_LDAP_different_format_to_set_location(Test):
    uuid = "SOSAIOT-TC-77121"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1507159')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    def test_02_delete_local_group(self):
        response = user_local.delete_local_group_no_domain("testgp1")
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Failed to delete local group")

    def test_03_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "ou=qa,dc=shvl,dc=com"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    def test_04_delete_local_group(self):
        response = user_local.delete_local_group_no_domain("testgp1")
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Failed to delete local group")

class Test_LDAP_For_users_at_or_under_the_given_location(Test):
    uuid = "SOSAIOT-TC-77133"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825600')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')


class Test_LDAP_For_users_at_given_location(Test):
    uuid = "SOSAIOT-TC-77122"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1507161')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')


class Test_LDAP_For_users_access_rules(Test):
    uuid = "SOSAIOT-TC-77123"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1507162')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "testgp1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, "ERR: cannot added access rule")

class Test_LDAP_For_logs_support(Test):
    uuid = "SOSAIOT-TC-77125"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1507160')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "testgp1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, "ERR: cannot added access rule")

class Test_LDAP_locations_configured_used_in_App_rules(Test):
    uuid = "SOSAIOT-TC-77129"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825599')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "testgp1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, "ERR: cannot added access rule")

class Test_LDAP_locations_configured_used_in_SSO(Test):
    uuid = "SOSAIOT-TC-77131"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825601')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "testgp1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, "ERR: cannot added access rule")


class Test_LDAP_locations_configured_used_in_CFS(Test):
    uuid = "SOSAIOT-TC-77134"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825603')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "testgp1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, "ERR: cannot added access rule")


class Test_LDAP_locations_configured_used_in_GAV(Test):
    uuid = "SOSAIOT-TC-77135"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825605')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "testgp1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, "ERR: cannot added access rule")


class Test_LDAP_locations_configured_used_in_SSLVPN(Test):
    uuid = "SOSAIOT-TC-77136"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825606')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "testgp1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, "ERR: cannot added access rule")


class Test_LDAP_locations_configured_used_in_DPI_SSL(Test):
    uuid = "SOSAIOT-TC-77139"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825608')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "testgp1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, "ERR: cannot added access rule")


class Test_LDAP_locations_configured_used_in_Radius(Test):
    uuid = "SOSAIOT-TC-77140"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825610')

    def test_01_add_local_group(self):
        add_local_group = {
        "user": {
            "local": {
            "group": [
                {
                "memberships_by_ldap_location": {
                    "under_or_at": True
                },
                "name": "testgp1",
                "ldap_location": "shvl.com/qa"
                }
            ]
            }
        }
        }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testgp1"', 'err: Failed to create local group')

    
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "testgp1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, "ERR: cannot added access rule")

class TC_imported_groups_auto_filled(Test):
    uuid = "SOSAIOT-TC-77141"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825611')

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

    # configure ldap

    def test_02_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")

    def test_03_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'test',
                'bind_password': 'password',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            res = json.dumps(resp)
            res = None 
            if '"host": "OS-WSV.os-autosnwl.com"' or '"host": "192.168.168.85"'  in res:
                res = True
            Assertion.assert_equal(res, True, "ERR: failed to config ldap server")

    def test_04_add_user(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        resp = user_local.group_member_of(**member)
        resp1 = user_local.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"',
                                 'err: ldap users not added to sonicwall administrators')

    def test_05_enable(self):
        enable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': True
        }
        resp = user_local.group_administration_tab(**enable)
        resp1 = user_local.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": true',
                                 'err: enable to_management_on_login failed.')
    
    @repeat_method(4)
    def test_06_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "SonicWALL Administrators"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"',
                                 'err: access rules not updated.')
    def test_07_Import_ldap_user(self):
        user_json = {
            'action': 'add',
            'username': 'test',
            'userpassword': 'password',
            'domain': 'os-autosnwl.com',

        }

        resp = user_local.local_user(**user_json)
        
    #     resp1 = user.show_local_users()
    # @repeat_method(5)
    # def test_08_login(self):
    #     static_client.send_command('pkill firefox')
    #     time.sleep(10)
    #     url = "https://13.0.0.100"
    #     cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293/lib/ui_ldap.py ' + \
    #           '-url ' + url + ' -user test -pwd password'
    #     out = static_client.send_command(cmd)
    #     logger.info("login with user\n" + out)
    #     # check user status
    #     status = user_status.show_user_status_by_name('test')
    #     Assertion.assert_regular(json.dumps(status), '13.0.0.4', "failed to get user status")

    # # logout user
    # def test_08_logout(self):
    #     rc = user.logout_all_users()
    #     Assertion.assert_equal(rc, True, "ERR: logout user failed")

class delete_ldap(Test):
    uuid = 'NonTC'

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

class TC_AA_support(Test):
    uuid = "SOSAIOT-TC-77137"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825607')

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

    # configure ldap

    def test_02_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")

    def test_03_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'test',
                'bind_password': 'password',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            res = json.dumps(resp)
            res = None 
            if '"host": "OS-WSV.os-autosnwl.com"' or '"host": "192.168.168.85"'  in res:
                res = True
            Assertion.assert_equal(res, True, "ERR: failed to config ldap server")

    def test_04_add_user(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        resp = user_local.group_member_of(**member)
        resp1 = user_local.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"',
                                 'err: ldap users not added to sonicwall administrators')

    def test_05_enable(self):
        enable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': True
        }
        resp = user_local.group_administration_tab(**enable)
        resp1 = user_local.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": true',
                                 'err: enable to_management_on_login failed.')
    
    @repeat_method(4)
    def test_06_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "SonicWALL Administrators"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"',
                                 'err: access rules not updated.')

    def test_07_Import_ldap_user(self):
        user_json = {
            'action': 'add',
            'username': 'test',
            'userpassword': 'password',
            'domain': 'os-autosnwl.com',

        }

        resp = user_local.local_user(**user_json)
    #     resp1 = user.show_local_users()
    # @repeat_method(5)
    # def test_08_login(self):
    #     static_client.send_command('pkill firefox')
    #     time.sleep(10)
    #     url = "https://13.0.0.100"
    #     cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293/lib/ui_ldap.py ' + \
    #           '-url ' + url + ' -user test -pwd password'
    #     out = static_client.send_command(cmd)
    #     logger.info("login with user\n" + out)
    #     # check user status
    #     status = user_status.show_user_status_by_name('test')
    #     Assertion.assert_regular(json.dumps(status), '13.0.0.4', "failed to get user status")

    # # logout user
    # def test_08_logout(self):
    #     rc = user.logout_all_users()
    #     Assertion.assert_equal(rc, True, "ERR: logout user failed")

class delete_ldap(Test):
    uuid = 'NonTC'

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

