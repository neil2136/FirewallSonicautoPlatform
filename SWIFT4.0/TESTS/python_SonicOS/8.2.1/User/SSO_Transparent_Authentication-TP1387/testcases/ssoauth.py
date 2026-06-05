from definition.settings import *

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_Transparent_Authentication-TP1387')

def test_sso_agent_connectivity(sso_ip, test): 
    try:
        test_agent_json = {
            "user": {
                "sso": {
                    "test": {
                        "agent": {
                        "name_or_ip_addr": f"{sso_ip}",
                        "port": 2258
                        }
                    }
                }
            }
        }

        test_workstation_ip = {
            "user": {
                "sso": {
                    "test": {
                        "agent": {
                            "name_or_ip_addr": f"{sso_ip}",
                            "user_ip": f"{sso_ip}",
                            "mechanism": {
                                "via_netapi_or_wmi": True
                            }
                        }
                    }
                }
            }
        }
        headers1 = OrderedDict([('Accept', 'application/json'),
                            ('Content-Type', 'application/json'),
                            ('Accept-Encoding', 'application/json'),
                            ('charset', 'UTF-8')])   
        payload = {"override": True}
        payload = json.dumps(payload)
        if test == "sso" :
            json_str = json.dumps(test_agent_json, indent=2)
        elif test == 'workstation':
            json_str = json.dumps(test_workstation_ip, indent=2)
        auth_url = 'https://192.168.168.168/api/sonicos/auth'
        urllib3.disable_warnings()
        resp = requests.post(auth_url, auth = HTTPDigestAuth("admin", G_PASSWORD_NEW), data = payload, headers = headers1, verify = False)
        response = resp.content.decode('utf-8')
        logger.info("Login response after decode:\r\n{}".format(response))
        url = "https://192.168.168.168/api/sonicos/user/sso/test"
        print("Test SSO Url :", url)
        resp = requests.post(url, headers = headers1, data = json_str, verify = False)
        logger.info(resp.status_code)
        result = True if resp.status_code == 200 else False
        return resp.json()
    except:
        return False


class NonTC(Test):
    uuid = 'NonTC'

    def test_01_create_ldapuser(self):
        add_ldap_server = {
            'role': 'primary',
            'host': '192.168.168.65',
            'enable': True,
            'port_num': 389,
            'use_tls': False,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': True,
            'bind': 'distinguished_name',
            'distinguished_name': 'sslvpntest',
            'bind_password': 'password',
            'referred_bind_with_account': 'other-servers',
            'primary_domain': 'os-autosnwl.com',
            'users_tree': ['Users', 'os-autosnwl.com/Users'],
            'user_groups_tree': ['os-autosnwl.com/Users'],
            'directory': True,
            'schema': 'microsoft-active-directory/network-information-service'
        }
        ldap_user = user_ldap.add_ldap_server(**add_ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.65"', "ERR: Failed to config the ldap server")

    def test_02_Ldap_user_settings(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR: LDAP method is not selected successfully")
    
    def test_03_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule_json = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        accessrule.edit_ipv4_access_rule_uuid(uuid, **accessrule_json)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to update access rule')


class TC01_Enable_User_SSO_Settings(Test):
    uuid = "SOSAIOT-TC-75847"
    description = show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_user_sso_settings(self):
        user_sso_settings = {
            'user': {
                'sso': {
                    'user_group_mechanism': {
                        'local_only': True
                    },
                    'hold_time': {
                        'after_failure': 1,
                        'after_no_user': 1
                    },
                    'poll': {
                        'rate': {
                            'minutes': 1
                        },
                        'same_agent': False
                    }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**user_sso_settings)
        Assertion.assert_equal(response, True, "ERR: Unable to Enable User SSO Settings")


class TC02_Incorrectly_Formatted_SSO_User_Agent(Test):
    uuid = "SOSAIOT-TC-75848"
    description = show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_incorrect_sso_agent(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': '1.1.1.1',
                 'port': 2220,
                 'timeout': 10,
                 'max_requests': 32,
                 'enable': True,
                 'shared_key':'##'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, False, "ERR: Able to Add Incorrect Formatted User SSO Agent")

    def test_02_adding_incorrect_sso_agent(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': '1.1.1.1',
                 'port': 2220,
                 'timeout': 10,
                 'max_requests': 32,
                 'enable': True,
                 'shared_key':'%%'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, False, "ERR: Able to Add Incorrect Formatted User SSO Agent")


class TC03_Configure_Button_Not_Dimmed_After_Use_LDAP(Test):
    uuid = "SOSAIOT-TC-75849"
    description = show_testcase_info(Parameter.TESTPLAN, '3', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_user_sso_agent(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': '192.168.168.65',
                 'port': 2258,
                 'timeout': 10,
                 'max_requests': 3,
                 'enable': True,
                 'shared_key':'225abc'
        }

        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")

    def test_02_enabling_ldap_user_group_for_sso(self):
        option = "LDAP"
        response = firewallUI.verify_configure_sso_ldap_user_group_button(option)
        Assertion.assert_equal(response[0], True, "ERR: Configure button is dimmed after selecting LDAP User Group")


class TC04_Configure_Button_Dimmed_After_Local_Configurations(Test):
    uuid = "SOSAIOT-TC-75850"
    description = show_testcase_info(Parameter.TESTPLAN, '4', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enabling_local_configuration_user_for_sso(self):
        option = "Local Configuration"
        response = firewallUI.verify_configure_sso_ldap_user_group_button(option)
        Assertion.assert_equal(response[0], False, "ERR: Configure button is not dimmed after selecting Local Configurations")


class TC05_Incorrect_Formatted_Polling_Rate_Value(Test):
    uuid = "SOSAIOT-TC-75851"
    description = show_testcase_info(Parameter.TESTPLAN, '5', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_checking_incorrect_formatted_polling_rate(self):
        response = firewallUI.verify_updating_polling_rate_minutes_value(value = "#")
        Assertion.assert_equal(response[0], False, "ERR: Able to update the incorrect formatted polling rate")
        
    def test_02_checking_incorrect_formatted_polling_rate(self):
        response = firewallUI.verify_updating_polling_rate_minutes_value(value = "%")
        Assertion.assert_equal(response[0], False, "ERR: Able to update the incorrect formatted polling rate")
    
    def test_03_checking_incorrect_formatted_polling_rate(self):
        response = firewallUI.verify_updating_polling_rate_minutes_value(value = "n")
        Assertion.assert_equal(response[0], False, "ERR: Able to update the incorrect formatted polling rate")


class TC06_Test_SSO_Agent_Connectivity(Test):
    uuid = "SOSAIOT-TC-75852"
    description = show_testcase_info(Parameter.TESTPLAN, '6', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_test_sso_agent_connectivity(self):
        response = test_sso_agent_connectivity(sso_ip="192.168.168.65", test="sso")
        Assertion.assert_regular(json.dumps(response), "Agent is ready", "ERR: Failed to check SSO Agent Connectivity")


class TC07_Test_Set_Workstation_IP_SSO(Test):
    uuid = "SOSAIOT-TC-75853"
    description = show_testcase_info(Parameter.TESTPLAN, '7', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(3)
    def test_01_test_workstation_ip_connectivity(self):
        response = test_sso_agent_connectivity(sso_ip="192.168.168.65", test="workstation")
        Assertion.assert_regular(json.dumps(response), "OS-AUTOSNWL", "ERR: Failed to check SSO Workstation IP Connectivity")


class TC08_Connectivity_Test(Test):
    uuid = "SOSAIOT-TC-75854"
    description = show_testcase_info(Parameter.TESTPLAN, '8', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_packet_capture(self):
        packet.clear_packets()
        response1 = packet.start_capture()
        Assertion.assert_equal(response1, True, "ERR: Failed to start packet capture")
    
    def test_02_test_connectivity(self):
        response = test_sso_agent_connectivity(sso_ip="192.168.168.65", test="sso")
        Assertion.assert_regular(json.dumps(response), "Agent is ready", "ERR: Failed to check SSO Agent Connectivity")

    def test_03_assert_respective_packets(self):
        packet.stop_capture()
        response = packet.export_captured_packets()
        logger.info(response)
        if re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.FIREWALL, Parameter.sso_server), str(response), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.sso_server, Parameter.FIREWALL), str(response), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: SSO Test Packets are not present")


class TC09_User_Connectivity_Test(Test):
    uuid = "SOSAIOT-TC-75855"
    description = show_testcase_info(Parameter.TESTPLAN, '9', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_packet_capture(self):
        packet.clear_packets()
        response1 = packet.start_capture()
        Assertion.assert_equal(response1, True, "ERR: Failed to start packet capture")
    
    @repeat_method(3)
    def test_02_test_connectivity(self):
        response = test_sso_agent_connectivity(sso_ip="192.168.168.65", test="workstation")
        Assertion.assert_regular(json.dumps(response), "OS-AUTOSNWL", "ERR: Failed to check SSO Workstation IP Connectivity")

    def test_03_assert_respective_packets(self):
        packet.stop_capture()
        response = packet.export_captured_packets()
        logger.info(response)
        if re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.FIREWALL, Parameter.client), str(response), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.client, Parameter.FIREWALL), str(response), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: SSO User Test Packets are not present")


class TC10_Using_IP_Address_For_Auth_Agent(Test):
    uuid = "SOSAIOT-TC-75856"
    description = show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_local_configurations(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"', "ERR: Failed to select LDAP Configurations")

    def test_02_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule_json = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        accessrule.edit_ipv4_access_rule_uuid(uuid, **accessrule_json)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to update access rule')

    def test_03_checking_traffic_in_domain_client(self):  
        response = LAN_HOST.ping(Parameter.client)
        Assertion.assert_equal(response, True, "ERR: Internet is not accessible at domain client")  


class TC11_Using_FQDN_For_Auth_Agent(Test):
    uuid = "SOSAIOT-TC-75857"
    description = show_testcase_info(Parameter.TESTPLAN, '11', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_local_configurations(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"', "ERR: Failed to select LDAP Configurations")

    def test_02_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule_json = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        accessrule.edit_ipv4_access_rule_uuid(uuid, **accessrule_json)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to update access rule')
    
    def test_03_checking_sso_domain_status(self):
        status = user_status.show_user_status()
        if '192.168.168.2 0' or '192.168.168.3 0' or '192.168.168.4 0' in status:
            res = True
        Assertion.assert_equal(res, True, "ERR: Failed to get sso domain user status")


class TC12_Timeout_Reply_Agent(Test):
    uuid = "SOSAIOT-TC-75858"
    description = show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name=Parameter.sso_server, port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_02_add_sso_agent_wrong_secret_key(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': '192.168.168.65',
                 'port': 2258,
                 'timeout': 5,
                 'max_requests': 32,
                 'enable': True,
                 'shared_key':'225aba'
        }

        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")

    @repeat_method(3)
    def test_03_test_connectivity(self):
        packet.clear_packets()
        packet.start_capture()
        response = test_sso_agent_connectivity(sso_ip="192.168.168.65", test="sso")
        Assertion.assert_regular(json.dumps(response), "Failed to start the SSO daemon", "ERR: SSO Agent Connectivity passed with wrong shared key")

    def test_04_editing_sso_agent_timeout(self):
        put_sso_agent = {
            "user": {
                "sso": {
                    "agent": [
                        {
                            'host': '192.168.168.65',
                            'port': 2258,
                            'timeout': 10,
                            'max_requests': 32,
                            'enable': True,
                            'shared_key':'225aba'
                        }
                    ]
                }
            }    
        }
        response = user_sso.edit_sso_agent(name="192.168.168.65", port = 2258, **put_sso_agent)
        Assertion.assert_equal(response, True, "ERR: Unable to updated timeout for User SSO Agent")
   
    @repeat_method(3)
    def test_05_test_connectivity(self):
        response = test_sso_agent_connectivity(sso_ip="192.168.168.65", test="sso")
        packet.stop_capture()
        Assertion.assert_regular(json.dumps(response), "Failed to start the SSO daemon", "ERR: SSO Agent Connectivity passed with wrong shared key")

    
class TC13_Retry_Timeout_Request_Agent(Test):
    uuid = "SOSAIOT-TC-75859"
    description = show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name=f'{Parameter.sso_server}', port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_02_add_sso_agent_3_max_retry(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': '192.168.168.65',
                 'port': 2258,
                 'timeout': 5,
                 'max_requests': 3,
                 'enable': True,
                 'shared_key':'225aba'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")
    
    @repeat_method(3)
    def test_03_test_connectivity(self):
        packet.clear_packets()
        packet.start_capture()
        response = test_sso_agent_connectivity(sso_ip="192.168.168.65", test="sso")
        print(response)
        Assertion.assert_regular(json.dumps(response), "Failed to start the SSO daemon", "ERR: SSO Agent Connectivity passed with wrong shared key")

    def test_04_assert_respective_packets_for_max_retries(self):
        packet.stop_capture()
        response = packet.export_captured_packets()
        logger.info(response)
        if re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.client, Parameter.FIREWALL), str(response), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.client, Parameter.FIREWALL), str(response), re.S|re.I) and \
             re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.client, Parameter.FIREWALL), str(response), re.S|re.I):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: SSO User Test Packets are not present")

    def test_05_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name=f'{Parameter.sso_server}', port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_06_edit_sso_agent_6_max_retry(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': '192.168.168.65',
                 'port': 2258,
                 'timeout': 5,
                 'max_requests': 6,
                 'enable': True,
                 'shared_key':'225aba'
        }

        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")
    
    @repeat_method(3)
    def test_07_test_connectivity(self):
        packet.clear_packets()
        packet.start_capture()
        response = test_sso_agent_connectivity(sso_ip="192.168.168.65", test="sso")
        print(response)
        Assertion.assert_regular(json.dumps(response), "Failed to start the SSO daemon", "ERR: SSO Agent Connectivity passed with wrong shared key")


class TC14_SSO_Configure_Enabled(Test):
    uuid = "SOSAIOT-TC-75860"
    description = show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name=f'{Parameter.sso_server}', port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_02_enable_sso_agent_configuration(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"sso_agent": true', "ERR: Failed to enable sso agent")


class TC15_Shared_Key_MisMatch(Test):
    uuid = "SOSAIOT-TC-75861"
    description = show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_sso_agent_with_mismatch_key(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': '192.168.168.65',
                 'port': 2258,
                 'timeout': 5,
                 'max_requests': 6,
                 'enable': True,
                 'shared_key':'225aba'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")
    
    @repeat_method(3)
    def test_02_test_connectivity(self):
        packet.clear_packets()
        packet.start_capture()
        response = test_sso_agent_connectivity(sso_ip="192.168.168.65", test="sso")
        print(response)
        Assertion.assert_regular(json.dumps(response), "Failed to start the SSO daemon", "ERR: SSO Agent Connectivity passed with wrong shared key")

    def test_03_assert_respective_packets_for_max_retries(self):
        packet.stop_capture()
        response = packet.export_captured_packets()
        logger.info(response)
        if not re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.FIREWALL, Parameter.client), str(response), re.S|re.I) and \
              re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.client, Parameter.FIREWALL), str(response), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: SSO User Test Packets are not present")


class TC16_Domain_User_Logged_With_Accessing_Resources(Test):
    uuid = "SOSAIOT-TC-75862"
    description = show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name=f'{Parameter.sso_server}', port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_02_add_sso_agent_3_max_retry(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': '192.168.168.65',
                 'port': 2258,
                 'timeout': 5,
                 'max_requests': 3,
                 'enable': True,
                 'shared_key':'225abc'
        }

        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")

    def test_03_enable_sso_agent_configuration(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"sso_agent": true', "ERR: Failed to enable sso agent")

    def test_04_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule_json = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        accessrule.edit_ipv4_access_rule_uuid(uuid, **accessrule_json)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to update access rule')

    def test_05_accessing_internet_from_domain(self):
        response = LAN_HOST.ping(Parameter.client)
        Assertion.assert_equal(response, True, "ERR: Internet is not accessible at domain client")  


class TC17_Local_User_Logged_Not_Accessing_Resources(Test):
    uuid = "SOSAIOT-TC-75863"
    description = show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_agent_configuration(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"sso_agent": true', "ERR: Failed to enable sso agent")

    def test_02_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule_json = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        accessrule.edit_ipv4_access_rule_uuid(uuid, **accessrule_json)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to update access rule')

    def test_03_accessing_internet_from_local_user(self):
        response = LAN_HOST.ping(Parameter.client)
        Assertion.assert_equal(response, True, "ERR: Internet is not accessible at domain client")  


class TC18_FQDN_Auth_Agent_Name_Setup(Test):
    uuid = "SOSAIOT-TC-75865"
    description = show_testcase_info(Parameter.TESTPLAN, '18', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name=f'{Parameter.sso_server}', port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_02_sso_agent_FQDN_config(self):
        sso_agent_dict = {
                 'action': 'add',
                 'host': 'os-wsv.os-autosnwl.com',
                 'port': 2258,
                 'timeout': 5,
                 'max_requests': 6,
                 'enable': False,
                 'shared_key':'225abc'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")


class TC19_Auth_Agent_IP_Address(Test):
    uuid = "SOSAIOT-TC-75874"
    description = show_testcase_info(Parameter.TESTPLAN, '19', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_local_configurations(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"sso_agent": true', "ERR: Failed to enable SSO Configurations")

    def test_02_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name='os-wsv.os-autosnwl.com', port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_03_add_sso_agent(self):
        sso_agent_dict = {
            'action': 'add',
            'host': '192.168.168.65',
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key':'225abc'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")
    

class TC20_User_Name_Window_Services(Test):
    uuid = "SOSAIOT-TC-75881"
    description = show_testcase_info(Parameter.TESTPLAN, '20', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name=f'{Parameter.sso_server}', port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_02_adding_sso_agent(self):
        sso_agent_dict = {
            'action': 'add',
            'host': '192.168.168.65',
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key':'225abc'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")

    def test_03_adding_verifying_options_window_service_agent(self):
        response = firewallUI.verify_updating_windows_service_agent(user="NEW", options=True)
        Assertion.assert_equal(response[0], True, "ERR: Unable to Add and Verify Windows Service User")

    
class TC21_Adding_Window_Services_Username(Test):
    uuid = "SOSAIOT-TC-75882"
    description = show_testcase_info(Parameter.TESTPLAN, '21', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_verifying_options_window_service_agent(self):
        response = firewallUI.verify_updating_windows_service_agent(user="NEW")
        Assertion.assert_equal(response[0], True, "ERR: Unable to Add Windows Service User")


class TC22_Updating_Port_Number_SSO_Agent(Test):
    uuid = "SOSAIOT-TC-75883"
    description = show_testcase_info(Parameter.TESTPLAN, '22', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name=f'{Parameter.sso_server}', port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_02_add_sso_agent(self):
        sso_agent_dict = {
            'action': 'add',
            'host': '192.168.168.65',
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key':'225abc'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")


class TC23_Adding_Window_Services_Username_Apply_SSO(Test):
    uuid = "SOSAIOT-TC-75884"
    description = show_testcase_info(Parameter.TESTPLAN, '23', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_verifying_options_window_service_agent(self):
        response = firewallUI.verify_updating_windows_service_agent(user="test1")
        Assertion.assert_equal(response[0], True, "ERR: Unable to Add Windows Service User")


class TC24_Adding_Special_Window_Services_Username(Test):
    uuid = "SOSAIOT-TC-75885"
    description = show_testcase_info(Parameter.TESTPLAN, '24', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_special_window_service_agent(self):
        response = firewallUI.verify_updating_windows_service_agent(user="yili\\test")
        Assertion.assert_equal(response[0], True, "ERR: Unable to Add Windows Service User")


class TC25_Edit_Window_Services_Username(Test):
    uuid = "SOSAIOT-TC-75886"
    description = show_testcase_info(Parameter.TESTPLAN, '25', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_editing_window_service_username(self):
        response = firewallUI.verify_editing_windows_service_agent(user="test1", new_user="test2")
        Assertion.assert_equal(response[0], True, "ERR: Unable to Edit Windows Service User")


class TC26_Edit_SSO_Window_Services_User(Test):
    uuid = "SOSAIOT-TC-75887"
    description = show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_editing_window_service_agent(self):
        response = firewallUI.verify_editing_windows_service_agent(user="NEW", new_user="test3")
        Assertion.assert_equal(response[0], True, "ERR: Unable to Edit Windows Service User")


class TC27_Edit_Special_Window_Services_Username(Test):
    uuid = "SOSAIOT-TC-75888"
    description = show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_editing_special_window_service_agent(self):
        response = firewallUI.verify_editing_windows_service_agent(user="yili\\test", new_user="sli\\test")
        Assertion.assert_equal(response[0], True, "ERR: Unable to Edit Windows Service User")


class TC28_Remove_Window_Services_Username(Test):
    uuid = "SOSAIOT-TC-75889"
    description = show_testcase_info(Parameter.TESTPLAN, '28', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_removing_window_service_agent(self):
        response = firewallUI.verify_deleting_windows_service_user(user="test2")
        Assertion.assert_equal(response[0], True, "ERR: Unable to Delete Windows Service User")


class TC29_Remove_And_Verify_Window_Services_User(Test):
    uuid = "SOSAIOT-TC-75890"
    description = show_testcase_info(Parameter.TESTPLAN, '29', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_removing_window_service_agent(self):
        response = firewallUI.verify_deleting_windows_service_user(user="test3")
        Assertion.assert_equal(response[0], True, "ERR: Unable to Delete Windows Service User")

    def test_02_verifying_window_service_agent(self):
        response = firewallUI.verify_windows_service_user(user="test3")
        Assertion.assert_equal(response[0], False, "ERR: Unable to Verify Windows Service User")


class TC30_Agent_Can_Remove_All_Users(Test):
    uuid = "SOSAIOT-TC-75892"
    description = show_testcase_info(Parameter.TESTPLAN, '30', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_deleting_all_names_through_agent(self):
        response = firewallUI.verify_deleting_all_windows_service_user()
        Assertion.assert_equal(response[0], True, "ERR: Unable to Delete All Windows Service User")


class TC31_Setting_SSO_Shared_Key(Test):
    uuid = "SOSAIOT-TC-75893"
    description = show_testcase_info(Parameter.TESTPLAN, '31', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name=f'{Parameter.sso_server}', port=2258)
        Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_02_add_sso_agent(self):
        sso_agent_dict = {
            'action': 'add',
            'host': '192.168.168.65',
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key':'225abc'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")


class TC32_Age_Out_Inactivity_Timeout(Test):
    uuid = "SOSAIOT-TC-75903"
    description = show_testcase_info(Parameter.TESTPLAN, '32', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_updating_hold_timeout_10_minutes(self):
        logger.info('Enable SSO by RADIUS accounting......')
        edit_timeout = {
            "user": {
                "sso": {
                "hold_time": {
                    "after_failure": 1,
                    "after_no_user": 10
                    }
                }
            }
        }
        response =  user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, True, "ERR: Updating the hold timeout value failed")


class TC33_Age_Timeout_Field_Boundaries(Test):
    uuid = "SOSAIOT-TC-75904"
    description = show_testcase_info(Parameter.TESTPLAN, '33', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_updating_hold_timeout_1_minutes(self):
        logger.info('Enable SSO by RADIUS accounting......')
        edit_timeout = {
            "user": {
                "sso": {
                "hold_time": {
                    "after_failure": 1,
                    "after_no_user": 1
                    }
                }
            }
        }
        response =  user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, True, "ERR: Updating the hold timeout value failed")

    def test_02_updating_hold_timeout_10_minutes(self):
        logger.info('Enable SSO by RADIUS accounting......')
        edit_timeout = {
            "user": {
                "sso": {
                "hold_time": {
                    "after_failure": 1,
                    "after_no_user": 10
                    }
                }
            }
        }
        response =  user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, True, "ERR: Updating the hold timeout value failed")

    def test_03_updating_hold_timeout_60_minutes(self):
        logger.info('Enable SSO by RADIUS accounting......')
        edit_timeout = {
            "user": {
                "sso": {
                "hold_time": {
                    "after_failure": 1,
                    "after_no_user": 60
                    }
                }
            }
        }
        response =  user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, True, "ERR: Updating the hold timeout value failed")


class TC34_User_Listed_Checkbox(Test):
    uuid = "SOSAIOT-TC-75905"
    description = show_testcase_info(Parameter.TESTPLAN, '34', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_updating_hold_timeout_1_minutes(self):
        logger.info('Enable SSO by RADIUS accounting......')
        edit_timeout = {
            "user": {
                "sso": {
                "hold_time": {
                    "after_failure": 1,
                    "after_no_user": 1
                    }
                }
            }
        }
        response =  user_sso.config_sso_base_settings(**edit_timeout)
        Assertion.assert_equal(response, True, "ERR: Updating the hold timeout value failed")


class TC35_SSO_Configuration_Present_In_Prefs(Test):
    uuid = "SOSAIOT-TC-75906"
    description = show_testcase_info(Parameter.TESTPLAN, '35', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_sso_config(self):
        response = tsr.download_tsr()
        with open('/tmp/techSupport', 'r') as tech_doc:
            doc = tech_doc.read()
            flag = True if re.search(r'New="192.168.168.65"', doc) else False
            Assertion.assert_equal(flag, True, "ERR: Details not found in TSR")
            os.remove('/tmp/techSupport')


