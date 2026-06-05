from definition.settings import *

class TestConfigureULA(Test):
    uuid = 'NonTC'
    
    def test_01_add_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'testuser1',
            'userpassword': 'S0nic@uto1',
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['Everyone'],
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
            'member_of': ['Everyone'],
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"name": "testuser2"', "ERR: failed to add Local User")

    def test_03_add_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'testuser3',
            'userpassword': 'S0nic@uto3',
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['Everyone', 'SonicWALL Administrators'],
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"name": "testuser3"', "ERR: failed to add Local User")
    
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
    
    def test_04_add_customized_zone(self):
        cuz_dict = {
            "zones": [
                {
                "name": "zone1",
                "security_type": "public",
                }
            ]
        }
        add_zone = zone_object.add_zone_object(**cuz_dict)
        Assertion.assert_equal(add_zone,True,"Err: Failed to add zone.")
    
    def test_05_add_local_super_group(self):
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


class TC01_Access_the_VPN_from_the_LAN_allow_Group(Test):
    uuid = "SOSAIOT-TC-76034"
    description = show_testcase_info(Parameter.TESTPLAN, '1524260', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524260')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_01_edit_lan_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'VPN')
        lan_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                lan_vpn_rule["access_rules"][0] = rule
                break
        lan_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'group1'}
        uuid = lan_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **lan_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_02_ula_login(self):
        pc2.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")

        # expecting failure
        pc2.send_command('pkill firefox')
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser2 -pwd S0nic@uto2 -failure True'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        

class TC02_Access_the_VPN_from_the_DMZ_allow_Everyone(Test):
    uuid = "SOSAIOT-TC-76035"
    description = show_testcase_info(Parameter.TESTPLAN, '1524267', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524267')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_01_edit_dmz_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'VPN')
        dmz_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                dmz_vpn_rule["access_rules"][0] = rule
                break
        dmz_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = dmz_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **dmz_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_02_ula_login(self):
        pc2.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")


class TC03_Access_the_VPN_from_the_Custom_Zone_allow_Group(Test):
    uuid = "SOSAIOT-TC-76036"
    description = show_testcase_info(Parameter.TESTPLAN, '1524275', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524275')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_Set_X2_Interface(self):
        rc = interface.config_interface(**x2_cus)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_02_edit_zone1_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('zone1', 'VPN')
        zone1_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                zone1_vpn_rule["access_rules"][0] = rule
                break
        zone1_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'group1'}
        uuid = zone1_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **zone1_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_ula_login(self):
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")

        # expecting failure
        pc3.send_command('pkill firefox')
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser2 -pwd S0nic@uto2 -failure True'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()
    
    def test_04_Set_X2_Interface(self):
        rc = interface.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")


class TC04_Access_From_Remote_End_of_the_Tunnel_Deny_All(Test):
    uuid = "SOSAIOT-TC-76037"
    description = show_testcase_info(Parameter.TESTPLAN, '1524286', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524286')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_wan_acl(self):
        access_rule = {
            'name': 'vpn_wan_deny',
            'from': 'VPN',
            'to': 'WAN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True}
        }
        output = accessrule.add_ipv4_access_rule(**access_rule)
        Assertion.assert_equal(output, True, "ERR: Failed to add access rule")

    def test_02_check_wan_access(self):
        output = pc4.send_command(f'ping -c 5 {Parameter.WAN_IP}')
        Assertion.assert_regular(json.dumps(output), '100% packet loss', f"ERR: Ping passed from VPN to WAN.")
    
    def test_03_delete_rule(self):
        output = accessrule.del_ipv4_access_rule('vpn_wan_deny')
        Assertion.assert_equal(output, True, "ERR: Failed to delete access rule")


class TC05_Access_VPN_From_LAN_Allow_All(Test):
    uuid = "SOSAIOT-TC-76038"
    description = show_testcase_info(Parameter.TESTPLAN, '1524257', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524257')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")   

    def test_01_edit_lan_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'VPN')
        lan_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                lan_vpn_rule["access_rules"][0] = rule
                break
        lan_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'all': True}
        uuid = lan_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **lan_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        pc2.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -direct True'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")


class TC06_Access_VPN_From_LAN_Allow_Admin(Test):
    uuid = "SOSAIOT-TC-76039"
    description = show_testcase_info(Parameter.TESTPLAN, '1524258', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524258')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_lan_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'VPN')
        lan_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                lan_vpn_rule["access_rules"][0] = rule
                break
        lan_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'SonicWALL Administrators'}
        uuid = lan_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **lan_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        # verify failure
        pc2.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -failure True -direct True'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        # verify access
        pc2.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + f' -user admin -pwd {Params.G_NEW_PASSWORD}'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()

    
class TC07_Access_VPN_From_LAN_Allow_Everyone(Test):
    uuid = "SOSAIOT-TC-76040"
    description = show_testcase_info(Parameter.TESTPLAN, '1524259', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524259')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_lan_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'VPN')
        lan_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                lan_vpn_rule["access_rules"][0] = rule
                break
        lan_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = lan_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **lan_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_02_ula_login(self):
        pc2.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")


class TC08_Access_VPN_From_LAN_Deny_All(Test):
    uuid = "SOSAIOT-TC-76041"
    description = show_testcase_info(Parameter.TESTPLAN, '1524263', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524263')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_lan_vpn_acl(self):
        access_rule = {
            'name': 'lan_vpn_deny',
            'from': 'LAN',
            'to': 'VPN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True}
        }
        output = accessrule.add_ipv4_access_rule(**access_rule)
        Assertion.assert_equal(output, True, "ERR: Failed to add access rule")

    def test_02_check_wan_access(self):
        output = pc2.send_command(f'ping -c 5 {Parameter.VPN_IP}')
        Assertion.assert_regular(json.dumps(output), '100% packet loss', f"ERR: Ping passed from LAN to VPN.")
    
    def test_03_delete_rule(self):
        output = accessrule.del_ipv4_access_rule('lan_vpn_deny')
        Assertion.assert_equal(output, True, "ERR: Failed to delete access rule")


class TC09_Access_VPN_From_DMZ_Allow_All(Test):
    uuid = "SOSAIOT-TC-76042"
    description = show_testcase_info(Parameter.TESTPLAN, '1524264', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524264')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")   

    def test_01_edit_dmz_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'VPN')
        dmz_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                dmz_vpn_rule["access_rules"][0] = rule
                break
        dmz_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'all': True}
        uuid = dmz_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **dmz_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -direct True'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")


class TC10_Access_VPN_From_DMZ_Allow_Admin(Test):
    uuid = "SOSAIOT-TC-76043"
    description = show_testcase_info(Parameter.TESTPLAN, '1524266', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524266')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_dmz_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'VPN')
        dmz_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                dmz_vpn_rule["access_rules"][0] = rule
                break
        dmz_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'SonicWALL Administrators'}
        uuid = dmz_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **dmz_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        # verify failure
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -failure True -direct True'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        # verify access
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + f' -user admin -pwd {Params.G_NEW_PASSWORD}'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()


class TC11_Access_VPN_From_DMZ_Deny_All(Test):
    uuid = "SOSAIOT-TC-76046"
    description = show_testcase_info(Parameter.TESTPLAN, '1524271', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524271')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dmz_vpn_acl(self):
        access_rule = {
            'name': 'dmz_vpn_deny',
            'from': 'DMZ',
            'to': 'VPN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True}
        }
        output = accessrule.add_ipv4_access_rule(**access_rule)
        Assertion.assert_equal(output, True, "ERR: Failed to add access rule")

    def test_02_check_wan_access(self):
        output = pc3.send_command(f'ping -c 5 {Parameter.VPN_IP}')
        Assertion.assert_regular(json.dumps(output), '100% packet loss', f"ERR: Ping passed from DMZ to VPN.")
    
    def test_03_delete_rule(self):
        output = accessrule.del_ipv4_access_rule('dmz_vpn_deny')
        Assertion.assert_equal(output, True, "ERR: Failed to delete access rule")


class TC12_Access_VPN_From_DMZ_Allow_Super_Group(Test):
    uuid = "SOSAIOT-TC-76044"
    description = show_testcase_info(Parameter.TESTPLAN, '1524269', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524269')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 
    def test_01_edit_dmz_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'VPN')
        dmz_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                dmz_vpn_rule["access_rules"][0] = rule
                break
        dmz_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'group2'}
        uuid = dmz_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **dmz_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_02_ula_login(self):
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser2 -pwd S0nic@uto2 -failure True'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")

        # expecting failure
        pc3.send_command('pkill firefox')
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()


class TC13_Access_VPN_From_DMZ_Allow_User(Test):
    uuid = "SOSAIOT-TC-76045"
    description = show_testcase_info(Parameter.TESTPLAN, '1524270', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524270')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_dmz_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'VPN')
        dmz_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                dmz_vpn_rule["access_rules"][0] = rule
                break
        dmz_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'name': 'testuser1'}
        uuid = dmz_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **dmz_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")


class TC14_Login_Redirect_Upon_the_VPN_Access_from_Cus_Zone(Test):
    uuid = "SOSAIOT-TC-76048"
    description = show_testcase_info(Parameter.TESTPLAN, '1524307', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524307')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_Set_X2_Interface(self):
        rc = interface.config_interface(**x2_cus)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_02_edit_zone1_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('zone1', 'VPN')
        zone1_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                zone1_vpn_rule["access_rules"][0] = rule
                break
        zone1_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = zone1_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **zone1_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_ula_login(self):
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")


class TC15_Access_VPN_From_Cus_Zone_Allow_All(Test):
    uuid = "SOSAIOT-TC-76047"
    description = show_testcase_info(Parameter.TESTPLAN, '1524272', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524272')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")   

    def test_01_edit_zone1_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('zone1', 'VPN')
        zone1_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                zone1_vpn_rule["access_rules"][0] = rule
                break
        zone1_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'all': True}
        uuid = zone1_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **zone1_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -direct True'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")


class TC16_Access_VPN_From_Cus_Zone_Allow_Admin(Test):
    uuid = "SOSAIOT-TC-76049"
    description = show_testcase_info(Parameter.TESTPLAN, '1524273', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524273')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")   

    def test_01_edit_zone1_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('zone1', 'VPN')
        zone1_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                zone1_vpn_rule["access_rules"][0] = rule
                break
        zone1_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'SonicWALL Administrators'}
        uuid = zone1_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **zone1_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        # verify failure
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -failure True -direct True'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        # verify access
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + f' -user admin -pwd {Params.G_NEW_PASSWORD}'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()


class TC17_Access_the_VPN_from_the_Cus_Zone_Allow_Everyone(Test):
    uuid = "SOSAIOT-TC-76050"
    description = show_testcase_info(Parameter.TESTPLAN, '1524274', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524274')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_01_edit_zone1_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('zone1', 'VPN')
        zone1_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                zone1_vpn_rule["access_rules"][0] = rule
                break
        zone1_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = zone1_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **zone1_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_02_ula_login(self):
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")


class TC18_Access_VPN_From_Cus_Zone_Allow_User(Test):
    uuid = "SOSAIOT-TC-76052"
    description = show_testcase_info(Parameter.TESTPLAN, '1524278', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524278')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_zone1_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('zone1', 'VPN')
        zone1_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                zone1_vpn_rule["access_rules"][0] = rule
                break
        zone1_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'name': 'testuser1'}
        uuid = zone1_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **zone1_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_02_ula_login(self):
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")


class TC19_Access_VPN_From_Cus_Zone_Deny_All(Test):
    uuid = "SOSAIOT-TC-76053"
    description = show_testcase_info(Parameter.TESTPLAN, '1524279', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524279')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_zone1_vpn_acl(self):
        access_rule = {
            'name': 'zone1_vpn_deny',
            'from': 'zone1',
            'to': 'VPN',
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True}
        }
        output = accessrule.add_ipv4_access_rule(**access_rule)
        Assertion.assert_equal(output, True, "ERR: Failed to add access rule")

    def test_02_check_wan_access(self):
        output = pc3.send_command(f'ping -c 5 {Parameter.VPN_IP}')
        Assertion.assert_regular(json.dumps(output), '100% packet loss', f"ERR: Ping passed from zone1 to VPN.")
    
    def test_03_delete_rule(self):
        output = accessrule.del_ipv4_access_rule('zone1_vpn_deny')
        Assertion.assert_equal(output, True, "ERR: Failed to delete access rule")


class TC20_Access_VPN_From_Cus_Zone_Allow_Super_Group(Test):
    uuid = "SOSAIOT-TC-76051"

    def test_01_edit_zone1_vpn_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('zone1', 'VPN')
        zone1_vpn_rule ={"access_rules":[{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "group" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['group'] == 'local_group':
                zone1_vpn_rule["access_rules"][0] = rule
                break
        zone1_vpn_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'group2'}
        uuid = zone1_vpn_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **zone1_vpn_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_02_ula_login(self):
        pc3.send_command('pkill firefox')
        time.sleep(10)
        url=f'http://{Parameter.VPN_IP}'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser2 -pwd S0nic@uto2 -failure True'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")

        # expecting failure
        pc3.send_command('pkill firefox')
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user testuser1 -pwd S0nic@uto1'
        out = pc3.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()


class TC21_Access_VPN_From_Remote_End_Allow_Admin(Test):
    uuid = "SOSAIOT-TC-76054"
    description = show_testcase_info(Parameter.TESTPLAN, '1524281', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524281')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_vpn_lan_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('VPN', 'LAN')
        vpn_lan_rule = {"access_rules": [{}]}
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
        vpn_lan_rule = {"access_rules": [{}]}
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
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser3 -pwd S0nic@uto3'
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

    def test_01_add_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'testuser4',
            'userpassword': 'Password@4',
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['Everyone', 'SonicWALL Administrators'],
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"name": "testuser3"', "ERR: failed to add Local User")

    def test_02_add_local_group(self):
        group_json = {
            "user": {
                "local": {
                    "group": [
                        {
                            "name": "group_vpn",
                            "member": [{"name": "testuser3"}]
                        }
                    ]
                }
            }
        }

        resp = user_local.add_local_group(**group_json)
        added_user = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(added_user), '"name": "group_vpn"', "ERR: failed to add Local User Group")

    def test_03_edit_vpn_lan_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('VPN', 'LAN')
        vpn_lan_rule = {"access_rules": [{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "name" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['name'] == 'local_vpn':
                vpn_lan_rule["access_rules"][0] = rule
                break
        vpn_lan_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'group_vpn'}
        uuid = vpn_lan_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **vpn_lan_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_04_ula_login(self):
        # verify access
        pc4.send_command('pkill firefox')
        time.sleep(10)
        url = f"https://{Parameter.LAN_IP}"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser3 -pwd S0nic@uto3'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()

        # expecting failure
        pc4.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser4 -pwd Password@4 -failure True'
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

    def test_01_add_local_super_group(self):
        group_json = {
            "user": {
                "local": {
                    "group": [
                        {
                            "name": "super_grp_vpn",
                            "member": [{"name": "group_vpn"}]
                        }
                    ]
                }
            }
        }
        resp = user_local.add_local_group(**group_json)
        added_user = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(added_user), '"name": "group2"', "ERR: failed to add Local User Group")

    def test_02_edit_vpn_lan_rule(self):
        rules = accessrule.get_ipv4_access_rule_given_from_to('VPN', 'LAN')
        vpn_lan_rule = {"access_rules": [{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "name" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['name'] == 'local_vpn':
                vpn_lan_rule["access_rules"][0] = rule
                break
        vpn_lan_rule["access_rules"][0]['ipv4']['users']['included'] = {'group': 'super_grp_vpn'}
        uuid = vpn_lan_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **vpn_lan_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_ula_login(self):
        # verify access
        pc4.send_command('pkill firefox')
        time.sleep(10)
        url = f"https://{Parameter.LAN_IP}"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser3 -pwd S0nic@uto3'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()

        # expecting failure
        pc4.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser4 -pwd Password@4 -failure True'
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
        vpn_lan_rule = {"access_rules": [{}]}
        logger.info(f"rule - {rules['access_rules'][0]}")
        for rule in rules['access_rules']:
            if "name" in rule['ipv4']['source']['address'] and rule['ipv4']['source']['address']['name'] == 'local_vpn':
                vpn_lan_rule["access_rules"][0] = rule
                break
        vpn_lan_rule["access_rules"][0]['ipv4']['users']['included'] = {'name': 'testuser3'}
        uuid = vpn_lan_rule["access_rules"][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **vpn_lan_rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_02_ula_login(self):
        # verify access
        pc4.send_command('pkill firefox')
        time.sleep(10)
        url = f"https://{Parameter.LAN_IP}"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser3 -pwd S0nic@uto3'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()

        # expecting failure
        pc4.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/fw_login.py ' + '-url ' + f'{url}' + ' -user testuser4 -pwd Password@4 -failure True'
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
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/definition/aup_login.py ' + '-url ' + f'{url}' + ' -user testuser3 -pwd S0nic@uto3'
        out = pc4.send_command(cmd)
        logger.info("response: \n" + out)
        Assertion.assert_not_regular(out, 'Exception', "ERR: Exception Occured!")
        user_local.logout_all_users()