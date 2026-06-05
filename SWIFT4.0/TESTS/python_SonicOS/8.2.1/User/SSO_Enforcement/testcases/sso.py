from definition.settings import *


def run_io_tasks_in_parallel(tasks):
    results = []
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            results.append(running_task.result())
    return results

def ssh_execute_command(host, username, password, command, port=22, timeout=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
   
    errors = []

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    logger.info(f"{output}")
    error = stderr.read().decode()
    errors.append(error)

    if timeout:
        time.sleep(timeout)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        logger.info(f"{output}")
        error = stderr.read().decode()
        errors.append(error)

    ssh.close()
    for error in errors:
        if error:
            raise Exception(f"Error executing command: {error}")
    return output

# def verify_logs(log_text, failure=False):
#     logs = log_monitor.export_log_txt()
#     # if failure:
#     #     Assertion.assert_not_regular(logs, log_text, "Err: Did not find the logs.")
#     # else:
#     #     Assertion.assert_regular(logs, log_text, "Err: Did not find the logs.")

def test_sso_agent():
    url = 'api/sonicos/user/sso/test'
    sso_test = {
        "user":{
            "sso":{
                "test":{
                    "agent":{
                        "name_or_ip_addr":Parameter.SSO_SERV,
                        "port": 2258
                        }
                    }
                    }
                }
        } 
    resp, msg = fw_api.api_post(url, msg=True, data={**sso_test})
    return json.dumps(msg)

def check_active_user_status(name, failure=False, timeout=0):
    time.sleep(timeout)
    active_sessions = user_status.show_user_status()
    # if failure:
    #     Assertion.assert_not_regular(json.dumps(active_sessions), name, "ERR: user does exist in active sessions.")
    # else:
    #     Assertion.assert_regular(json.dumps(active_sessions), name, "ERR: user does not exist in active sessions.")

def add_enforce_on_zone_json(**kwargs):
        resp = fw_api.api_post('api/sonicos/user/sso/enforce-on-zones', False, data=kwargs)
        return resp

def del_enforce_on_zone(delete_zone):
        url = 'api/sonicos/user/sso/enforce-on-zones/name/' + delete_zone
        output = fw_api.api_delete(url)
        return output

def verify_logs_and_session(failure=False):
    time.sleep(30)
    check_active_user_status(Parameter.DOMAIN_U1, failure)


class NonTC(Test):
    uuid = 'NonTC'

    def test_01_create_ldapuser(self):
        ldap_server["user"]["ldap"]["server"][0]["host"] = Parameter.SSO_SERV
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), f'"host": "{Parameter.SSO_SERV}"', "ERR: Failed to config the ldap server.")

    def test_02_Ldap_user_settings(self):
        input_data = {
            "auth_method": "ldap",
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        ldap_auth = user_setting.user_method_authentication(**input_data)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR: LDAP method is not selected successfully.")
    
    def test_03_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
        lan_wan_rule['user_included']= {"group": "Everyone"}
        accessrule.edit_ipv4_access_rule_uuid(uuid, **lan_wan_rule)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to update access rule.')
    
    def test_04_add_user_sso_agent(self):
        sso_agent["user"]["sso"]["agent"][0]["host"] = Parameter.SSO_SERV
        sso_agents_resp = fw_api.api_post('api/sonicos/user/sso/agents', msg=False, data=sso_agent)
        # Assertion.assert_equal(sso_agents_resp, True, "ERR: Unable to Add User SSO Agent.")
        time.sleep(30)
        resp = test_sso_agent()
        # Assertion.assert_regular(resp, "Agent is ready", "ERR: SSO agent is down.")
    
    def test_05_import_user_from_ldap(self):
        input_data = {
            "user": {
                "local": {
                    "user": [{
                        "name": Parameter.DOMAIN_U1,
                        "domain": f"{Parameter.DOMAIN}.com"
                    }]
                }
            }
        }
        resp = user_local.import_local_usr_from_ldap(**input_data)
        logger.info(resp)
        Assertion.assert_equal(resp, True, "ERR: Failed to import LDAP user.")
    
    def test_06_user_logout_log_setting(self):
        user_logout ={
            "log": {
                "event": [
                    {
                        "id": 31,
                        "name": "Successful User Login",
                        "category": "Users",
                        "group": "Authentication Access",
                        "priority_level": "debug",
                        "log_monitor": {
                            "redundancy_interval": 60
                        }
                    }
                ]
            }
        }
        resp = log_category.logging_level(level='debug')
        Assertion.assert_equal(resp, True, "ERR: Config log settings failed.")
        resp = log_settings.edit_event(event_id='31', **user_logout)
        resp = log_settings.show_event(event_id='31')
        Assertion.assert_regular(json.dumps(resp), '{"redundancy_interval": 60}', 'err: log event not changed.')
    
    def test_07_enable_security_services_lan(self):
        lan = {
            "zones":[
                {
                'name': 'LAN',
                'anti_spyware':True,
                'intrusion_prevention': True,
                'app_control': True
               }
            ]
        }
        resp = zone_object.edit_zone_object('LAN', **lan)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable security service on LAN.")
    
    def test_08_enable_security_services_dmz(self):
        dmz = {
            "zones":[
                {
                'name': 'DMZ',
                'anti_spyware':True,
                'intrusion_prevention': True,
                'app_control': True
               }
            ]
        }
        resp = zone_object.edit_zone_object('DMZ', **dmz)
        Assertion.assert_equal(resp, True, "ERR: Failed to enable security service on DMZ.")


class TC_01_SSO_enforcement_enabled_on_DMZ_zone_access_rule_can_trigger_SSO_authentication_for_DMZ_traffic_partition_in_DMZ_zone(Test):
    uuid = "SOSAIOT-TC-75215"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75215', description=True)['title']

    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75215')
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_enforcement(self):
        input_data = {
            'user': {
                'sso': {
                 'enforce_on_zone':[{
                     'zone_name': 'DMZ'
                 }]
                }
            }
        }
        response = add_enforce_on_zone_json(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to enable SSO enforcement on DMZ.")
    
    def test_02_edit_dmz_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_sso_login(self):
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.DMZ_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session()

        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)
    
    def test_04_edit_dmz_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included']={'all': True}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')


class TC_02_SSO_enforcement_disabled_on_DMZ_zone_access_rule_can_trigger_SSO_authentication_for_DMZ_traffic_partition_in_DMZ_zone(Test):
    uuid = "SOSAIOT-TC-75217"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75217', description=True)['title']
    
    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75217')
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_sso_enforcement(self):
        response = del_enforce_on_zone('DMZ')
        Assertion.assert_equal(response, True, "ERR: Failed to disable SSO enforcement on DMZ.")

    def test_02_edit_dmz_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_03_sso_login(self):
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.DMZ_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session()

    def test_04_edit_dmz_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included']={'all': True}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')


class TC_03_SSO_enforcement_disabled_on_DMZ_zone_no_access_rule_no_security_service_traffic_from_DMZ_will_not_trigger_SSO_authentication_partition_DMZ_zone(Test):
    uuid = "SOSAIOT-TC-75219"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75219True)['title']
    
    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75219
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_sso_enforcement(self):
        response = del_enforce_on_zone('DMZ')
        Assertion.assert_equal(response, True, "ERR: Failed to disable SSO enforcement on DMZ.")

    def test_02_edit_dmz_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')
    
    def test_03_sso_login(self):
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.DMZ_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session(failure=True)



class TC_04_SSO_enforcement_disabled_on_LAN_zone_access_rule_can_trigger_SSO_authentication_for_LAN_traffic_partition_in_LAN_zone(Test):
    uuid = "SOSAIOT-TC-75208"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75208', description=True)['title']
    
    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75208')
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_disable_sso_enforcement(self):
        response = del_enforce_on_zone('LAN')
        Assertion.assert_equal(response, True, "ERR: Failed to disable SSO enforcement on LAN.")
    
    def test_02_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included']={'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_sso_login(self):
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.LAN_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session()
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)
    
    def test_04_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included'] = {'all': True}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')


class TC_05_SSO_enforcement_disabled_on_LAN_zone_access_rule_can_trigger_SSO_authentication_for_LAN_traffic_multiple_partition_in_LAN_zone(Test):
    uuid = "SOSAIOT-TC-75212"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75212', description=True)['title']
    
    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75212')
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_disable_sso_enforcement(self):
        response = del_enforce_on_zone('LAN')
        Assertion.assert_equal(response, True, "ERR: Failed to disable SSO enforcement on LAN.")
    
    def test_02_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included']={'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_sso_login(self):
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.LAN_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session()
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)
    
    def test_04_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included'] = {'all': True}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')


class TC_06_SSO_enforcement_disabled_on_LAN_zone_no_access_rule_no_security_service_traffic_from_LAN_will_not_trigger_SSO_authentication_partition_LAN_zone(Test):
    uuid = "SOSAIOT-TC-75210"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75210', description=True)['title']
    
    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75210')
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_sso_enforcement(self):
        response = del_enforce_on_zone('LAN')
        Assertion.assert_equal(response, True, "ERR: Failed to disable SSO enforcement on LAN.")

    def test_02_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included']={'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_sso_login(self):
        user_local.logout_all_users()
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.LAN_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session(failure=True)
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)


class TC_07_SSO_enforcement_enabled_on_LAN_zone_access_rule_can_trigger_SSO_authentication_for_LAN_traffic_partition_in_LAN_zone(Test):
    uuid = "SOSAIOT-TC-75206"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75206', description=True)['title']

    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75206')
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_enforcement(self):
        input_data = {
            'user': {
                'sso': {
                 'enforce_on_zone':[{
                     'zone_name': 'LAN'
                 }]
                }
            }
        }
        response = add_enforce_on_zone_json(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to enable SSO enforcement on LAN.")
    
    def test_02_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included']={'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_sso_login(self):
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.LAN_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session()
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)
    
    def test_04_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included'] = {'all': True}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')


class TC_08_SSO_enforcement_enabled_on_LAN_zone_no_access_rule_no_security_service_traffic_from_LAN_will_trigger_SSO_authentication_multiple_partition_LAN_zone(Test):
    uuid = "SOSAIOT-TC-75214"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75214', description=True)['title']
    
    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75214')
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_enforcement(self):
        input_data = {
            'user': {
                'sso': {
                 'enforce_on_zone':[{
                     'zone_name': 'LAN'
                 }]
                }
            }
        }
        response = add_enforce_on_zone_json(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to enable SSO enforcement on LAN.")

    def test_02_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included']={'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_sso_login(self):
        user_local.logout_all_users()
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.LAN_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session(failure=True)
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)


class TC_09_SSO_enforcement_enabled_on_LAN_zone_no_access_rule_no_security_service_traffic_from_LAN_will_trigger_SSO_authentication_partition_LAN_zone(Test):
    uuid = "SOSAIOT-TC-75207"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75207', description=True)['title']
    
    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75207')
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_enforcement(self):
        input_data = {
            'user': {
                'sso': {
                 'enforce_on_zone':[{
                     'zone_name': 'LAN'
                 }]
                }
            }
        }
        response = add_enforce_on_zone_json(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to enable SSO enforcement on LAN.")

    def test_02_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included']={'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_sso_login(self):
        user_local.logout_all_users()
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.LAN_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session(failure=True)
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)


class TC_10_SSO_enforcement_disabled_on_LAN_zone_CFS_IPS_Application_FW_from_LAN_can_trigger_SSO_authentication_partition_in_LAN_zone(Test):
    uuid = "SOSAIOT-TC-75209"

    # description = show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75209', description=True)['title']
    
    # def test_00_show_testcase_info(self):
    #     show_testcase_info(Parameter.TESTPLAN, 'SOSAIOT-TC-75209')
    #     Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_disable_sso_enforcement(self):
        response = del_enforce_on_zone('LAN')
        Assertion.assert_equal(response, True, "ERR: Failed to disable SSO enforcement on LAN.")
    
    def test_02_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included']={'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_03_sso_login(self):
        log_monitor.clear_log()
        # ssh_execute_command(Parameter.LAN_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',Parameter.DOMAIN_UP1, f'ping {Parameter.PC5_WAN_IP}', timeout=50),
        verify_logs_and_session()
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)
    
    def test_04_edit_lan_wan_rule(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rule['access_rules'][0]['ipv4']['users']['included'] = {'all': True}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

