from definition.settings_vpn import *

class TestConfigureULA(Test):
    uuid = 'NonTC'
    
    def test_01_add_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'testuser1',
            'userpassword': 'S0nic@uto1',
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['Everyone', 'SonicWALL Administrators'],
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"name": "testuser1"', "ERR: failed to add Local User")
    
    def test_02_add_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'testuser2',
            'userpassword': 'S0nic@uto2',
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['Everyone', 'SonicWALL Administrators'],
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"name": "testuser2"', "ERR: failed to add Local User")

    def test_03_add_local_group(self):
        group_json = {
            "user":{
                "local":{
                    "group":[
                        {
                         "name":"group1",
                         "member":[{"name":"testuser1"}]
                         }
                      ]
                    }
                }
            }

        resp = user_local.add_local_group(**group_json)
        added_user = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(added_user), '"name": "group1"', "ERR: failed to add Local User Group")
    
    def test_04_add_local_super_group(self):
        group_json = {
            "user":{
                "local":{
                    "group":[
                        {
                         "name":"group2",
                         "member":[{"name":"group1"}]
                         }
                      ]
                    }
                }
            }
        resp = user_local.add_local_group(**group_json)
        added_user = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(added_user), '"name": "group2"', "ERR: failed to add Local User Group")


class TC21_Access_VPN_From_Remote_End_Allow_Admin(Test):
    uuid = "SOSAIOT-TC-76054"
    description = show_testcase_info(Parameter.TESTPLAN, '1524281', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524281')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_vpn_lan_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('VPN', 'LAN')
        vpn_lan_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "name" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['name'] == 'local_vpn':
                vpn_lan_rule["access_rules"][0] = rule
                break
        vpn_lan_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'SonicWALL Administrators'}
        uuid = vpn_lan_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **vpn_lan_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        # expecting failure
        output = pc4.send_command(f'ping -c 5 {Parameter.LAN_IP}')
        Assertion.assert_regular(json.dumps(output), '100% packet loss', f"ERR: Ping passed from LAN to VPN.")

        # verify access
        pc4.send_command('pkill firefox')
        time.sleep(10)
        url = f"https://{Parameter.LAN_IP}"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + f' -user admin -pwd {Params.G_NEW_PASSWORD}'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()


class TC22_Access_VPN_From_Remote_End_Allow_Everyone(Test):
    uuid = "SOSAIOT-TC-76055"
    description = show_testcase_info(Parameter.TESTPLAN, '1524282', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524282')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_vpn_lan_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('VPN', 'LAN')
        vpn_lan_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "name" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['name'] == 'local_vpn':
                vpn_lan_rule["access_rules"][0] = rule
                break
        vpn_lan_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = vpn_lan_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **vpn_lan_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        # expecting failure
        output = pc4.send_command(f'ping -c 5 {Parameter.LAN_IP}')
        Assertion.assert_regular(json.dumps(output), '100% packet loss', f"ERR: Ping passed from LAN to VPN.")

        # verify access
        pc4.send_command('pkill firefox')
        time.sleep(10)
        url = f"https://{Parameter.LAN_IP}"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()


class TC23_Access_VPN_From_Remote_End_Allow_Group(Test):
    uuid = "SOSAIOT-TC-76056"
    description = show_testcase_info(Parameter.TESTPLAN, '1524283', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524282')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_edit_vpn_lan_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('VPN', 'LAN')
        vpn_lan_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "name" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['name'] == 'local_vpn':
                vpn_lan_rule["access_rules"][0] = rule
                break
        vpn_lan_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'group1'}
        uuid = vpn_lan_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **vpn_lan_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        # verify access
        pc4.send_command('pkill firefox')
        time.sleep(10)
        url = f"https://{Parameter.LAN_IP}"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()

        # expecting failure
        pc4.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser2 -pwd S0nic@uto2 -failure True'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()


class TC24_Access_VPN_From_Remote_End_Allow_Super_Group(Test):
    uuid = "SOSAIOT-TC-76057"
    description = show_testcase_info(Parameter.TESTPLAN, '1524284', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524284')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_edit_vpn_lan_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('VPN', 'LAN')
        vpn_lan_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "name" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['name'] == 'local_vpn':
                vpn_lan_rule["access_rules"][0] = rule
                break
        vpn_lan_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'group2'}
        uuid = vpn_lan_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **vpn_lan_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        # verify access
        pc4.send_command('pkill firefox')
        time.sleep(10)
        url = f"https://{Parameter.LAN_IP}"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()

        # expecting failure
        pc4.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser2 -pwd S0nic@uto2 -failure True'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()

class TC25_Access_VPN_From_Remote_End_Allow_User(Test):
    uuid = "SOSAIOT-TC-76058"
    description = show_testcase_info(Parameter.TESTPLAN, '1524285', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524285')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_edit_vpn_lan_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('VPN', 'LAN')
        vpn_lan_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "name" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['name'] == 'local_vpn':
                vpn_lan_rule["access_rules"][0] = rule
                break
        vpn_lan_rule["access_rules"][0]['ipv4']['users']['included'] = {'name': 'testuser1'}
        uuid = vpn_lan_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **vpn_lan_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        # verify access
        pc4.send_command('pkill firefox')
        time.sleep(10)
        url = f"https://{Parameter.LAN_IP}"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()

        # expecting failure
        pc4.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser2 -pwd S0nic@uto2 -failure True'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()


class TC26_AUP_Displayed_On_Login_From_VPN(Test):
    uuid = "SOSAIOT-TC-76059"
    description = show_testcase_info(Parameter.TESTPLAN, '1524319', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524319')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_aup(self):
        json_input = {
            'policy_banner_before_login': True,
            'pocontent': 'Acceptable User Policy'
        }
        resp = user_setting.customization(**json_input)
        Assertion.assert_equal(resp, True, "ERR: Failed to config AUP.")
    
    def test_02_verify_aup_prompt(self):
        pc4.send_command('pkill firefox')
        time.sleep(10)
        url = f"https://{Parameter.FIREWALL}"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/aup_login.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()