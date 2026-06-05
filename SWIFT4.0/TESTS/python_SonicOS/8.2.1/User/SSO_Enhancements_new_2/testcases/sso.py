from definition.settings import *

class NonTC(Test):
    uuid = 'NonTC'

    def test_01_local_user_settings(self):
        input_data = {
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        ldap_auth = user_setting.user_method_authentication(**input_data)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"sso_agent": true',
                                 "ERR: Failed to edit settings.")
    
    def test_02_add_user_sso_agent(self):
        sso_agent["user"]["sso"]["agent"][0]["host"] = Parameter.SSO_SERV
        sso_agents_resp = fw_api.api_post('api/sonicos/user/sso/agents', msg=False, data=sso_agent)
        Assertion.assert_equal(sso_agents_resp, True, "ERR: Unable to Add User SSO Agent.")


class TC_03_Auto_Added_NAT_Policy_And_Access_Rule(Test):
    uuid = "SOSAIOT-TC-75232"
    jira = 'GEN8-8566'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825568')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_verify_nat_and_rule(self):
        nat_policies = nat_policy.get_nat_policy()
        nat = None
        for item in nat_policies['nat_policies']:
            if 'group' in item['ipv4']['source'] and 'SSO Agent' in item['ipv4']['source']['group']:
                nat = item['ipv4']
                break
        logger.info(f"Auto Added NAT Policy for SSO Agents: {nat}")
        Assertion.assert_equal('SonicWALL SSO Agents' in nat['service']['group'], True,
                               "ERR: Failed to verify auto added NAT Policy for SSO Agents.")
        
        rules = accessrule.get_ipv4_access_rule_given_from_to("LAN", "LAN")
        rule = None
        for item in rules['access_rules']:
            if 'group' in item['ipv4']['source']['address'] and 'SSO Agent' in item['ipv4']['source']['address']['group']:
                rule = item['ipv4']
                break
        logger.info(f"Auto Added Access Rule for SSO Agents: {rule}")
        Assertion.assert_equal('SonicWALL SSO Agents' in rule['service']['group'], True,
                               "ERR: Failed to verify auto added Access Rule for SSO Agents.")


class TC_06_Auto_Delete_Service_Object_After_Agent_Deletion(Test):
    uuid = "SOSAIOT-TC-75236"
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825572')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_delete_sso_agent(self):
        resp = fw_api.api_delete(f'api/sonicos/user/sso/agents/name/{Parameter.SSO_SERV}/port/2258')
        Assertion.assert_equal(resp, True, "ERR: Failed to delete SSO agent.")
    
    def test_02_verify_serv_group(self):
        serv_objs = service_object.get_serviceobject()
        flag = False
        for item in serv_objs['service_objects']:
            if 'SSO Agent' in item['name']:
                flag = True
        Assertion.assert_equal(flag, False, "ERR: Auto added SSO port Service Object still exists.")
        
        serv_grps = service_Group.get_servicegroup()
        serv_grp = None
        for item in serv_grps['service_groups']:
            if 'SSO Agent' in item['name']:
                serv_grp = item
        Assertion.assert_equal('service_object' in serv_grp, False,
                               "ERR: Auto added SSO port Service Object still exists in Service Group.")
    
    def test_03_add_user_sso_agent(self):
        sso_agent["user"]["sso"]["agent"][0]["host"] = Parameter.SSO_SERV
        sso_agents_resp = fw_api.api_post('api/sonicos/user/sso/agents', msg=False, data=sso_agent)
        Assertion.assert_equal(sso_agents_resp, True, "ERR: Unable to Add User SSO Agent.")


class TC_07_Auto_Delete_Access_Rule_After_Agent_Deletion(Test):
    uuid = "SOSAIOT-TC-75237"
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825573')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_sso_agent(self):
        resp = fw_api.api_delete(f'api/sonicos/user/sso/agents/name/{Parameter.SSO_SERV}/port/2258')
        Assertion.assert_equal(resp, True, "ERR: Failed to delete SSO agent.")
    
    def test_02_verify_access_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to("LAN", "LAN")
        flag = False
        for item in rules['access_rules']:
            if 'group' in item['ipv4']['source']['address'] and 'SSO Agent' in item['ipv4']['source']['address']['group']:
                flag = True
                break
        Assertion.assert_equal(flag, False, "ERR: Auto added Access Rule for SSO Agents still exists.")
    
    def test_03_add_user_sso_agent(self):
        sso_agent["user"]["sso"]["agent"][0]["host"] = Parameter.SSO_SERV
        sso_agents_resp = fw_api.api_post('api/sonicos/user/sso/agents', msg=False, data=sso_agent)
        Assertion.assert_equal(sso_agents_resp, True, "ERR: Unable to Add User SSO Agent.")


class TC_08_Import_Configuration_File(Test):
    uuid = "SOSAIOT-TC-75238"
    jira = 'GEN8-8566'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825575')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_export_config_file(self):
        resp = settings_obj.export_setting_exp()
        Assertion.assert_equal(resp, True, "ERR: Failed to export config file")

    def test_02_delete_sso_agent(self):
        resp = fw_api.api_delete(f'api/sonicos/user/sso/agents/name/{Parameter.SSO_SERV}/port/2258')
        Assertion.assert_equal(resp, True, "ERR: Failed to delete SSO agent.")
    
    def test_03_import_config_file(self):
        resp = settings_obj.import_setting_exp('/tmp/test.exp')
        logger.info(f"**** {resp}")
        Assertion.assert_equal(resp, True, "ERR: Failed to import config file")
    
    def test_04_verify_sso_agent(self):
        resp = fw_api.api_get('api/sonicos/user/sso/agents')
        Assertion.assert_equal(Parameter.SSO_SERV in str(resp), True, "ERR: Failed to verify sso agent.")


class TC_09_Agents_Configured_In_Diff_Zones(Test):
    uuid = "SOSAIOT-TC-75233"
    jira = 'GEN8-8566'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825569')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_sso_agent(self):
        agent = copy.deepcopy(sso_agent)
        agent["user"]["sso"]["agent"][0]["host"] = Parameter.DMZ_SERV
        sso_agents_resp = fw_api.api_post('api/sonicos/user/sso/agents', msg=False, data=agent)
        Assertion.assert_equal(sso_agents_resp, True, "ERR: Unable to Add User SSO Agent.")
    
    def test_02_verify_nat_and_rule(self):
        nat_policies = nat_policy.get_nat_policy()
        nat = None
        for item in nat_policies['nat_policies']:
            if 'group' in item['ipv4']['source'] and 'SSO Agent' in item['ipv4']['source']['group']:
                nat = item['ipv4']
                break
        logger.info(f"Auto Added NAT Policy for SSO Agents: {nat}")
        Assertion.assert_equal('SonicWALL SSO Agents' in nat['service']['group'], True,
                               "ERR: Failed to verify auto added NAT Policy for SSO Agents.")
        Assertion.assert_equal('DMZ Interface IP' in nat['destination']['group'], True,
                               "ERR: Failed to verify auto added NAT Policy for SSO Agents.")
        
        rules = accessrule.get_ipv4_access_rule_given_from_to("DMZ", "DMZ")
        rule = None
        for item in rules['access_rules']:
            if 'group' in item['ipv4']['source']['address'] and 'SSO Agent' in item['ipv4']['source']['address']['group']:
                rule = item['ipv4']
                break
        logger.info(f"Auto Added Access Rule for SSO Agents: {rule}")
        Assertion.assert_equal('SonicWALL SSO Agents' in rule['service']['group'], True,
                               "ERR: Failed to verify auto added Access Rule for SSO Agents.")
        Assertion.assert_equal('DMZ Interface IP' in rule['destination']['address']['group'], True,
                               "ERR: Failed to verify auto added Access Rule for SSO Agents.")
    
    def test_03_delete_sso_agent(self):
        resp = fw_api.api_delete(f'api/sonicos/user/sso/agents/name/{Parameter.DMZ_SERV}/port/2258')
        Assertion.assert_equal(resp, True, "ERR: Failed to delete SSO agent.")

