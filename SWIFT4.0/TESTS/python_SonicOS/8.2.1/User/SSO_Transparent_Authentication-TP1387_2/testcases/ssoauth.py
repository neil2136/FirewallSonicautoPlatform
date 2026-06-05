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

def verify_logs(log_text):
    logs = log_monitor.export_log_txt()
    Assertion.assert_regular(logs, log_text, "Err: Did not find the logs.")

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

def del_agent():
    response = user_sso.del_sso_agent(name=Parameter.SSO_SERV, port=2258)
    Assertion.assert_equal(response, True, "ERR: Failed to delete sso agent.")

class NonTC(Test):
    uuid = 'NonTC'

    def test_01_create_ldapuser(self):
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
        sso_agents_resp = fw_api.api_post('api/sonicos/user/sso/agents', msg=False, data=sso_agent)
        Assertion.assert_equal(sso_agents_resp, True, "ERR: Unable to Add User SSO Agent.")
        time.sleep(30)
        resp = test_sso_agent()
        Assertion.assert_regular(resp, "Agent is ready", "ERR: SSO agent is down.")
    
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
    
    def test_07_enable_security_services(self):
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


class TC_01_SSO_Login_With_Local_Config_Mechanism(Test):
    uuid = "SOSAIOT-TC-75907"
    description = show_testcase_info(Parameter.TESTPLAN, '1522304', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522304')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_allow_only_local_users(self):
        input_data = {
            'user': {
                'sso': {
                 'local_users_only':False,
                 'user_group_mechanism':{
                     'local_only': True
                 }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to enable local users only in sso.")

    def test_02_sso_login(self):
        log_monitor.clear_log()
        resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')
        Assertion.assert_not_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN.")
        verify_logs(f"{Parameter.DOMAIN}\\\\{Parameter.DOMAIN_U1}")
        verify_logs(Parameter.WORKSTATION_IP)
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)


class TC_02_SSO_Login_Only_Local_listed_Users(Test):
    uuid = "SOSAIOT-TC-75908"
    description = show_testcase_info(Parameter.TESTPLAN, '36', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_enable_allow_only_local_users(self):
        input_data = {
            'user': {'sso': {'local_users_only':True}}
        }
        response = user_sso.config_sso_base_settings(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to enable local users only in sso.")
        
    def test_02_sso_login_using_local_listed(self):
        log_monitor.clear_log()
        resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')
        Assertion.assert_not_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN.")
        verify_logs(f"{Parameter.DOMAIN}\\\\{Parameter.DOMAIN_U1}")
        verify_logs(Parameter.WORKSTATION_IP)
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)
    
    def test_03_sso_login_using_non_local_listed(self):
        resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U2}', Parameter.DOMAIN_UP2, f'ping {Parameter.WAN_PC4_IP}')
        Assertion.assert_regular(resp, "100% loss", "ERR: Ping Passed from LAN to WAN.")
        user_status.user_logout_by_admin(Parameter.DOMAIN_U2)
    
    def test_04_disable_allow_only_local_users(self):
        input_data = {
            'user': {'sso': {'local_users_only':False}}
        }
        response = user_sso.config_sso_base_settings(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to disable local users only in sso.")


class TC_03_SS0_Login_Ldap_configuration_Allow_Only_Local_Listed_Users(Test):
    uuid = "SOSAIOT-TC-75867"
    description = show_testcase_info(Parameter.TESTPLAN, '1522312', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522312')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_allow_only_local_users_with_ldap_config(self):
        input_data = {
            'user': {
                'sso': {
                 'local_users_only':True,
                 'user_group_mechanism':{
                     'ldap': True
                 }
                }
            }
        }
        response = user_sso.config_sso_base_settings(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to enable local users only in sso.")
    
    def test_02_sso_login_using_local_listed(self):
        log_monitor.clear_log()
        resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')
        Assertion.assert_not_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN.")
        verify_logs(f"{Parameter.DOMAIN}\\\\{Parameter.DOMAIN_U1}")
        verify_logs(Parameter.WORKSTATION_IP)
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)
    
    def test_03_sso_login_using_non_local_listed(self):
        resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U2}', Parameter.DOMAIN_UP2, f'ping {Parameter.WAN_PC4_IP}')
        Assertion.assert_regular(resp, "100% loss", "ERR: Ping Passed from LAN to WAN.")
        user_status.user_logout_by_admin(Parameter.DOMAIN_U2)
    
    def test_04_disable_allow_only_local_users(self):
        input_data = {
            'user': {'sso': {'local_users_only':False}}
        }
        response = user_sso.config_sso_base_settings(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to disable local users only in sso.")


class TC_04_Login_Session_Limit_Effect_On_SSO_User(Test):
    uuid = "SOSAIOT-TC-75868"
    description = show_testcase_info(Parameter.TESTPLAN, '1522313', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522313')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_user_session_time_limit(self):
        session = {
            'heartbeat_time_in_minutes': 10,
            'age_out_time_in_minutes': 60,
            'inactivity_time_in_minutes': 15,
            'terminateMinute':15,
            "web_login_session_limit": 1
        }
        response = user_setting.user_session(**session)
        Assertion.assert_equal(response, True, "ERR: Unable to modify user session time limit.")

    def test_02_sso_login_using_local_listed(self):
        log_monitor.clear_log()
        resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}', timeout=120)
        Assertion.assert_not_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN.")
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)


class TC_05_Sonicwall_SSO_Agent_Is_Used(Test):
    uuid = "SOSAIOT-TC-75873"
    description = show_testcase_info(Parameter.TESTPLAN, '1522318', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522318')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_enable_allow_only_local_users_with_ldap_config(self):
        input_data = {
            'user': {
                'sso': { 'user_group_mechanism':{ 'local_only': True}}
            }
        }
        response = user_sso.config_sso_base_settings(**input_data)
        Assertion.assert_equal(response, True, "ERR: Failed to enable local users only in sso.")

    def test_02_test_sso_workstation(self):
        url = 'api/sonicos/user/sso/test'
        sso_test = {
            "user":{
                "sso":{
                    "test":{
                        "agent":{
                            "name_or_ip_addr":Parameter.SSO_SERV,
                            "port":2258,
                            "user_ip":Parameter.WORKSTATION_IP,
                            "mechanism":{"via_netapi_or_wmi":True}
                            }
                        }
                     }
                 }
           } 
        resp = fw_api.api_post(url, data={**sso_test})
        Assertion.assert_equal(resp, True, "ERR: Failed to test sso workstation.")
    
    def test_03_sso_login(self):
        log_monitor.clear_log()
        resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')
        Assertion.assert_not_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN.")
        user_status.user_logout_by_admin(Parameter.DOMAIN_U1)

def disable_enable_sso_agent(enable=True):
    time.sleep(10)
    sso_agent = {
            "user": { 
                "sso": { 
                    "agent": [{ 
                        'enable': enable,
                        'host': Parameter.SSO_SERV,
                        'port': 2258,
                        'timeout': 10,
                        'retries': 3,
                        'max_requests': 32, 
                         }]
                     }
               }
        }
    resp = user_sso.edit_sso_agent_name_port(name=Parameter.SSO_SERV, port="2258", **sso_agent)
    Assertion.assert_equal(resp, True, "ERR: Failed to edit SSO agent.")


class TC_06_SSO_User_Activation_With_Previous_SSO_Failure(Test):
    uuid = "SOSAIOT-TC-75898"
    description = show_testcase_info(Parameter.TESTPLAN, '1522345', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522345')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_sso_user_activation(self):
        disable_enable_sso_agent(enable=False)
        ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')

        users = user_status.get_unauthenticated_users()
        Assertion.assert_regular(json.dumps(users), Parameter.WORKSTATION_IP, "ERR: Failed to verify unauthenticated user.")

        disable_enable_sso_agent(enable=True)
        time.sleep(30)
        resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')
        Assertion.assert_not_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN")

        users = user_status.get_unauthenticated_users()
        Assertion.assert_not_regular(json.dumps(users), Parameter.WORKSTATION_IP, "ERR: Still user is unauthenticated.")
        
    def test_02_enable_sso_agent(self):
        disable_enable_sso_agent(enable=True)

def verify_tsr():
    time.sleep(20)
    tsr_content = diag_api.get_tsr_part('Users', 'Status')
    Assertion.assert_regular(tsr_content, Parameter.WORKSTATION_IP, "ERR: Failed to verify ip.")
    Assertion.assert_regular(tsr_content, f"SSO agent {Parameter.SSO_SERV}", "ERR: Failed to verify sso agent.")


class TC_07_Check_SSO_Authentication_In_TSR(Test):
    uuid = "SOSAIOT-TC-75909"
    description = show_testcase_info(Parameter.TESTPLAN, '1522351', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522351')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_tsr(self):
        run_io_tasks_in_parallel([
        lambda: ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}'),
        lambda: verify_tsr()
        ])


def logout_user_from_status_page(name):
    time.sleep(20)
    active_sessions = user_status.show_user_status()
    Assertion.assert_regular(json.dumps(active_sessions), name, "ERR: user does not exist in active sessions.")
    user_status.user_logout_by_admin(name)

class TC_08_SSO_Multiple_Connetions_From_User(Test):
    uuid = "SOSAIOT-TC-75876"
    description = show_testcase_info(Parameter.TESTPLAN, '1522322', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522322')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_sso_login(self):
        command = f'ping -l 1024 -w 5000 {Parameter.WAN_PC4_IP}& ping -l 512 -w 5000 {Parameter.WAN_PC4_IP}'
        output = run_io_tasks_in_parallel([
        lambda: ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, command, timeout=30),
        lambda: logout_user_from_status_page(Parameter.DOMAIN_U1)
        ])
        text_pattern = r'\b' + re.escape('0% loss') + r'\b'
        matches = re.findall(text_pattern, output[0])
        Assertion.assert_equal(len(matches), 2, "ERR: Failed to verify ping from LAN to WAN.")


class TC_09_User_Not_Logged_Into_Network_With_CFS_Enabled(Test):
    uuid = "SOSAIOT-TC-75879"
    description = show_testcase_info(Parameter.TESTPLAN, '1522326', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522326')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
        lan_wan_rule['user_included']= {"all": True}
        accessrule.edit_ipv4_access_rule_uuid(uuid, **lan_wan_rule)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"all": True', 'ERR: Failed to update access rule.')
    
    def test_02_access_resource(self):
        resp = ssh_execute_command(Parameter.WORKSTATION_IP, Parameter.PC2_USER, Parameter.PC2_UP, f'ping {Parameter.WAN_PC4_IP}')
        Assertion.assert_regular(resp, "(0% loss)", "ERR: Ping failed from LAN to WAN")
        
    def test_03_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
        lan_wan_rule['user_included']= {"group": "Everyone"}
        accessrule.edit_ipv4_access_rule_uuid(uuid, **lan_wan_rule)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to update access rule.')

def check_user_in_status_page(name):
    time.sleep(25)
    active_sessions = user_status.show_user_status()
    Assertion.assert_regular(json.dumps(active_sessions), name, "ERR: user does not exist in active sessions.")
    
    
class TC_10_IPS_Trigger_SSO_Authentication(Test):
    uuid = "SOSAIOT-TC-75895"
    description = show_testcase_info(Parameter.TESTPLAN, '1522342', description=True)['title']
    jira = 'GEN8-8566'
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522342')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
        lan_wan_rule['user_included']= {"all": True}
        accessrule.edit_ipv4_access_rule_uuid(uuid, **lan_wan_rule)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"all": True', 'ERR: Failed to update access rule.')

    def test_02_enable_ips(self):
        ips = {
            'ips_enable': True,
            'high_detect_all': True,
            'medium_detect_all': True,
            'low_detect_all': True,
            'high_prevent_all': False,
            'medium_prevent_all': False,
            'low_prevent_all': False
        }
        resp = ips_api.config_base_IPS(**ips)
        Assertion.assert_equal(resp, True, "ERR: Failed to config ips")
    
    def test_03_config_ips_signatures(self):
        signature = {
            "intrusion_prevention": {
                "policy": [{
                    "id": 293,
                    "included": {
                        "ip": {
                            "category": True
                        },
                        "users": {
                            "group": "Everyone"
                        }
                    },
                    "excluded": {
                        "ip": {
                            "category": True
                        },
                        "users": {
                            "category": True
                        }
                    },
                    "schedule": {
                        "category": True
                    },
                    "log_redundancy": {
                        "category": True
                    },
                    "category": "ICMP",
                    "name": "PING",
                    "prevention": {},
                    "detection": {}
                }]
            }
        }
        resp = ips_api.config_ips_signatures('293', **signature)
        Assertion.assert_equal(resp, True, "ERR:  Modification ips signature failed.")

    def test_04_access_resource(self):
        output = run_io_tasks_in_parallel([
        lambda: ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}', Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}', timeout=30),
        lambda: check_user_in_status_page(Parameter.DOMAIN_U1)
        ])
        Assertion.assert_not_regular(output[0], "100% loss", "ERR: Failed to verify ping from LAN to WAN.")
        
    def test_05_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
        lan_wan_rule['user_included']= {"group": "Everyone"}
        accessrule.edit_ipv4_access_rule_uuid(uuid, **lan_wan_rule)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to update access rule.')
    
    def test_06_disable_ips(self):
        ips = {
            'ips_enable': False
        }
        resp = ips_api.config_base_IPS(**ips)
        Assertion.assert_equal(resp, True, "ERR: Failed to config ips.")


class TC_11_Show_Unauthenticated_Users(Test):
    uuid = "SOSAIOT-TC-75900"
    jira = 'GEN8-8566'
    description = show_testcase_info(Parameter.TESTPLAN, '1522347', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522347')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_sso_login(self):
        ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.WORKSTATION_U}', Parameter.WORKSTATION_P,
                            f'ping {Parameter.WAN_PC4_IP}')
        users = user_status.get_unauthenticated_users()
        Assertion.assert_regular(json.dumps(users), Parameter.WORKSTATION_IP,
                                 "ERR: Failed to verify unauthenticated user.")

class TC_12_Timeout_Field_Boundaries(Test):
    uuid = "SOSAIOT-TC-75904"
    jira = 'GEN8-8566'
    description = show_testcase_info(Parameter.TESTPLAN, '1825413', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825413')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sso_agent(self):
        agent = copy.deepcopy(sso_agent)
        agent["user"]["sso"]["agent"][0]["host"] = Parameter.WORKSTATION_IP
        agent["user"]["sso"]["agent"][0]["timeout"] = 0
        res, sso_agent_resp1 = fw_api.api_post('api/sonicos/user/sso/agents', msg=True, data=agent)
        Assertion.assert_regular(str(sso_agent_resp1), 'timeout', "ERR: Added User SSO Agent with inavlid value (0).")
        agent["user"]["sso"]["agent"][0]["timeout"] = 301
        res, sso_agent_resp2 = fw_api.api_post('api/sonicos/user/sso/agents', msg=True, data=agent)
        Assertion.assert_regular(str(sso_agent_resp2), 'out of bounds',
                                 "ERR: Added User SSO Agent with inavlid value (301).")


class TC_13_Application_Firewall_Triggers_SSO(Test):
    uuid = "SOSAIOT-TC-75897"
    jira = 'GEN8-8566'
    description = show_testcase_info(Parameter.TESTPLAN, '1522344', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1522344')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_application_firewall(self):
        json_data = {
            "app_control": {
                "enable": True,
            }
        }
        resp = appcontrol_api.config_app_control_base(**json_data)
        Assertion.assert_equal(resp, True, "ERR: Failed enable app control")

    def test_02_edit_access_rule(self):
        resp = accessrule.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
        lan_wan_rule['user_included'] = {"all": True}
        accessrule.edit_ipv4_access_rule_uuid(uuid, **lan_wan_rule)
        resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"all": true', 'ERR: Failed to update access rule.')

    def test_03_sso_login(self):
        output = run_io_tasks_in_parallel([
            lambda: ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',
                                        Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}', timeout=30),
            lambda: check_user_in_status_page(Parameter.DOMAIN_U1)
        ])
        Assertion.assert_not_regular(output[0], "100% loss", "ERR: Failed to verify ping from LAN to WAN.")


