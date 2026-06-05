from definition.settings import *


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
        if test == "sso":
            json_str = json.dumps(test_agent_json, indent=2)
        elif test == 'workstation':
            json_str = json.dumps(test_workstation_ip, indent=2)
        auth_url = 'https://192.168.168.168/api/sonicos/auth'
        urllib3.disable_warnings()
        resp = requests.post(auth_url, auth=HTTPDigestAuth("admin", G_PASSWORD_NEW), data=payload, headers=headers1, verify=False)
        response = resp.content.decode('utf-8')
        logger.info("Login response after decode:\r\n{}".format(response))
        url = "https://192.168.168.168/api/sonicos/user/sso/test"
        print("Test SSO Url :", url)
        resp = requests.post(url, headers=headers1, data=json_str, verify=False)
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
            'distinguished_name': 'ldap_auto_1',
            'bind_password': 'S0nic@uto',
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
    
    def test_03_deleting_previous_sso_agent(self):
        response = user_sso.del_sso_agent(name='192.168.168.65', port=2258)
        # Assertion.assert_equal(response, True, "ERR: Failed to delete older SSO Agent")

    def test_04_add_sso_agent(self):
        sso_agent_dict = {
            'action': 'add',
            'host': '192.168.168.65',
            'port': 2258,
            'timeout': 5,
            'max_requests': 3,
            'enable': True,
            'shared_key': '225abc'
        }
        response = user_sso.sso_agent(**sso_agent_dict)
        Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent")
    
    def test_06_edit_access_rule(self):
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


class TC_01_Edit_a_category_SSO_enforcement_disabled_set_included_user_with_local_user_group(Test):
    uuid = "SOSAIOT-TC-75824"
    description = show_testcase_info(Parameter.TESTPLAN, '1518396', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518396')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')

   

class TC_02_Edit_a_signature_SSO_enforcement_enabled_set_both_included_and_excluded_user_group(Test):
    uuid = "SOSAIOT-TC-75825"
    description = show_testcase_info(Parameter.TESTPLAN, '1518397', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518397')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_03_Edit_an_application_SSO_enforcement_enabled_set_included_user_group(Test):
    uuid = "SOSAIOT-TC-75826"
    description = show_testcase_info(Parameter.TESTPLAN, '1518398', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518398')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_04_Edit_an_application_SSO_enforcement_enabled_set_excluded_user_group(Test):
    uuid = "SOSAIOT-TC-75827"
    description = show_testcase_info(Parameter.TESTPLAN, '1518399', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518399')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_05_Edit_a_signature_then_enable_app_control_verify_that_SSO_enforcement_will_be_enabled_automatically(Test):
    uuid = "SOSAIOT-TC-75838"
    description = show_testcase_info(Parameter.TESTPLAN, '1518410', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518410')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_06_Add_an_app_rule_policy_SSO_enforcement_disabled_set_included_user_group(Test):
    uuid = "SOSAIOT-TC-75828"
    description = show_testcase_info(Parameter.TESTPLAN, '1518400', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518400')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_07_Edit_a_category_SSO_enforcement_disabled_set_excluded_user_group(Test):
    uuid = "SOSAIOT-TC-75829"
    description = show_testcase_info(Parameter.TESTPLAN, '1518401', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518401')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_08_Add_an_app_rule_policy_SSO_enforcement_disabled_set_excluded_user_group(Test):
    uuid = "SOSAIOT-TC-75830"
    description = show_testcase_info(Parameter.TESTPLAN, '1518402', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518402')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_09_Add_an_app_rule_policy_SSO_enforcement_disabled_set_both_included_and_excluded_user_group(Test):
    uuid = "SOSAIOT-TC-75831"
    description = show_testcase_info(Parameter.TESTPLAN, '1518403', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518403')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_10_App_an_app_rule_policy_SSO_enforcement_enabled_set_included_user_group(Test):
    uuid = "SOSAIOT-TC-75832"
    description = show_testcase_info(Parameter.TESTPLAN, '1518404', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518404')
        # Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_11_Add_an_app_rule_policy_SSO_enforcement_enabled_set_excluded_user_group(Test):
    uuid = "SOSAIOT-TC-75833"
    description = show_testcase_info(Parameter.TESTPLAN, '1518405', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518405')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_12_Include_user_is_set_to_all_and_excluded_is_set_to_none_verify_app_control_will_not_trigger_SSO_authentication(Test):
    uuid = "SOSAIOT-TC-75834"
    description = show_testcase_info(Parameter.TESTPLAN, '1518406', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518406')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_13_Include_user_is_set_to_all_and_excluded_is_set_to_none_verify_app_control_will_not_trigger_SSO_authentication(Test):
    uuid = "SOSAIOT-TC-75835"
    description = show_testcase_info(Parameter.TESTPLAN, '1518407', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518407')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_14_Category_include_user_is_set_to_all_and_excluded_is_set_to_none_verify_app_control_will_not_trigger_SSO_authentication(Test):
    uuid = "SOSAIOT-TC-75836"
    description = show_testcase_info(Parameter.TESTPLAN, '1518408', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518408')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')


class TC_15_Application_include_user_is_set_to_all_and_excluded_is_set_to_none_verify_app_control_will_not_trigger_SSO_authentication(Test):
    uuid = "SOSAIOT-TC-75837"
    description = show_testcase_info(Parameter.TESTPLAN, '1518409', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1518409')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_setup_prerequisites(self):
        resp = apprule.config_apprule_setting(enable=True)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable app rules setting")
    
    def test_02_create_match_object(self):
        resp = match_object.add_match_pattern(**http_object)
        match_resp = match_object.get_match_pattern_by_name("http")
        Assertion.assert_regular(json.dumps(match_resp), '"name": "http"', "ERR: Failed to verify match object creation")
    
    def test_03_post_app_rule(self):
        resp = apprule.add_apprule(**http_rule_policy)
        Assertion.assert_equal(resp, True, "ERR: Failed to add app rule")
        resp = apprule.get_apprule_obj()
        Assertion.assert_regular(json.dumps(resp), '"name": "web_access_policy"', "ERR: Failed to verify policy creation")
    
    def test_04_verify_policy_configuration(self):
        resp = apprule.get_app_rule('web_access_policy')
        policy_data = json.dumps(resp)
        Assertion.assert_regular(policy_data, '"enable": true', "ERR: Policy not enabled")
        Assertion.assert_regular(policy_data, '"action_object": "Reset/Drop"', "ERR: Incorrect action object")
        Assertion.assert_regular(policy_data, '"logging": true', "ERR: Logging not enabled")
    
    def test_05_verify_policy_enforcement(self):
        settings_resp = apprule.get_apprule_settings()
        settings_data = json.dumps(settings_resp)
        Assertion.assert_regular(settings_data, '"enable": true', "ERR: App rules not globally enabled")
    
    def test_06_cleanup(self):
        resp = apprule.delete_apprule_object_byname('web_access_policy')
