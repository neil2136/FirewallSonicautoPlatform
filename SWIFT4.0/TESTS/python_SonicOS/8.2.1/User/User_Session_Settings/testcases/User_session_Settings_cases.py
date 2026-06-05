import sys
import os
import json
from runner.settings import logger
from definition.settings import *
from utm import Firewall
import time
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/User_Session_Settings')
headers = OrderedDict([('Accept', 'application/json'),
					   ('Content-Type', 'application/json'),
					   ('Accept-Encoding', 'application/json'),
					   ('charset', 'UTF-8')])


def run_io_tasks_in_parallel(tasks):
	results = []
	with ThreadPoolExecutor() as executor:
		running_tasks = [executor.submit(task) for task in tasks]
		for running_task in running_tasks:
			results.append(running_task.result())
	return results

def test_sso_agent():
	url = 'api/sonicos/user/sso/test'
	sso_test = {
		"user": {
			"sso": {
				"test": {
					"agent": {
						"name_or_ip_addr": Parameter.SSO_SERV,
						"port": 2258
					}
				}
			}
		}
	}
	resp, msg = fw_api.api_post(url, msg=True, data={**sso_test})
	return json.dumps(msg)

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

# Non TC for SSO configuration
class NonTC(Test):
	uuid = 'NonTC'

	def test_01_create_ldapuser(self):
		ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
		resp = user_ldap.show_ldap_servers()
		Assertion.assert_regular(json.dumps(resp), f'"host": "{Parameter.SSO_SERV}"',
								 "ERR: Failed to config the ldap server.")

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
		lan_wan_rule['user_included'] = {"group": "Everyone"}
		accessrule.edit_ipv4_access_rule_uuid(uuid, **lan_wan_rule)
		resp1 = accessrule.get_ipv4_access_rule_by_uuid(uuid)
		Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to update access rule.')

	def test_04_add_user_sso_agent(self):
		input_data = {
			'action': 'add',
			'host': Parameter.SSO_SERV,
			'port': 2258,
			'timeout': 5,
			'max_requests': 3,
			'enable': False, #sso need to be disbaled
			'shared_key': '225abc',
			'retries': 3,
			"log_user_name": "Unknown (SSO bypassed)",
			"dummy_user": {
				"enable": True,
				"name": "Unknown (SSO bypassed)",
				"timeout": 15
			},
		}
		response = user_sso.sso_agent(**input_data)
		Assertion.assert_equal(response, True, "ERR: Unable to Add User SSO Agent.")
		logger.info("SSO agent configured as false")

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
		resp = local_user.import_local_usr_from_ldap(**input_data)
		logger.info(resp)
		Assertion.assert_equal(resp, True, "ERR: Failed to import LDAP user.")

#  verify when SSO fails to identify one user, log user name as "unkonwn(SSO failed)" works fine
class unknow_sso(Test):
	uuid = "SOSAIOT-TC-76094"

	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '1')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_enable_allow_only_local_users_with_ldap_config(self):
		input_data = {
			'user': {
				'sso': {
					'local_users_only': True,
					'user_group_mechanism': {
						'ldap': True
					}
				}
			}
		}
		response = user_sso.config_sso_base_settings(**input_data)
		Assertion.assert_equal(response, True, "ERR: Failed to enable local users only in sso.")

	def test_02_sso_login_generating_traffic(self):
		resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',
								   Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')
		Assertion.assert_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN.")
		logger.info("SSO failed")

	def test_03_session_details(self):

		response_get = user_status.show_user_status()
		Assertion.assert_not_regular(json.dumps(response_get), Parameter.DOMAIN_U1, 'err: User is still active')
		logger.info("User not active")

		logger.info("************************************")
		logger.info(response_get)
		logger.info("***********************************")

	def test_04_appflow_details(self):
		app_flow.login_ui()
		app_flow.go_to_appflow()
		app_flow.go_to_users()
		app_flow.verified_user_details("UNKNOWN")
		app_flow.logout_ui()

# verify when SSO bypass fails to identify one user, log user name as "unkonwn(SSO bypass)" works fine
class sso_bypass(Test):
	uuid = "SOSAIOT-TC-76095"

	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '2')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_get_sso_details(self):
		response_get = user_setting.show_user_setting()
		logger.info(response_get)
		bypass_sso_value = response_get["user"]["auth"]["log_user_name"]["bypass_sso"]
		Assertion.assert_equal(bypass_sso_value, "Unknown (SSO bypassed)",
								 'err: "dummy_user": "Unknown (SSO bypassed)" not enabled')

		logger.info("Dummy user enable")
		sso_fail_value = response_get["user"]["auth"]["log_user_name"]["sso_fail"]

		Assertion.assert_equal(sso_fail_value, "Unknown (SSO failed)",
								'err: "dummy_user": "Unknown (SSO bypassed)" not enabled')
		logger.info("SSO bypass user name for logging enable")

	def test_02_sso_login_generating_traffic(self):
		resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',
								   Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')
		Assertion.assert_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN.")


	def test_03_session_details(self):

		response_get = user_status.show_user_status()
		Assertion.assert_not_regular(json.dumps(response_get), Parameter.DOMAIN_U1, 'err: User is still active')
		logger.info("User session not present")

		logger.info("************************************")
		logger.info(response_get)
		logger.info("***********************************")

# verify for other unidentified connections, log user name as "unknown" works fine
class sso_lan_only(Test):
	uuid = "SOSAIOT-TC-76097"

	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '3')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_set_user_session_setting(self):
		logger.info("login")
		app_flow.login_ui()
		logger.info("go to user session page")
		app_flow.go_to_user_session_page()
		logger.info("set login")
		app_flow.set_logging()
		logger.info("log out")
		app_flow.logout_ui()

	def test_02_sso_login_generating_traffic(self):
		resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',
								   Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')
		Assertion.assert_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN.")

	def test_03_appflow_details(self):
		app_flow.login_ui()
		app_flow.go_to_appflow()
		app_flow.go_to_users()
		app_flow.verified_user_details("unknow(internal)")
		app_flow.logout_ui()

# verify for connections originating externally, log user name as "unknown (external)" works fine
class unidentified_login(Test):
	uuid = "SOSAIOT-TC-76096"

	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '4')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_sso_login_generating_traffic(self):
		resp = ssh_execute_command(Parameter.WORKSTATION_IP, f'{Parameter.DOMAIN}\\{Parameter.DOMAIN_U1}',
								   Parameter.DOMAIN_UP1, f'ping {Parameter.WAN_PC4_IP}')
		Assertion.assert_regular(resp, "100% loss", "ERR: Ping Failed from LAN to WAN.")

	def test_02_appflow_details(self):
		app_flow.login_ui()
		app_flow.go_to_appflow()
		app_flow.go_to_users()
		app_flow.verified_user_details("unknow(external)")
		app_flow.logout_ui()

# User connection logout: Inactivity authentication terminate keep-alive, inactivity other keep-alive
class user_connection_logout(Test):

	uuid = "SOSAIOT-TC-76098"

	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '5')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_set_unknow_sso(self):
		user_session = {
			"user_connections_logout": {
				"inactivity": {
					"authentication": {
						"keep_alive": True
					},
					"other": {
						"keep_alive": True
					}
				}
			}
		}

		user_setting.user_session(**user_session)
		resp = user_setting.show_user_setting()
		Assertion.assert_regular(json.dumps(resp), 'keep_alive',
								 "ERR:Failed to select Local authentication method.")

# User connection logout: Reported authentication keep-alive, reported other keep-alive
class user_connection_logout_others(Test):
	uuid = "SOSAIOT-TC-76099"


	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '6')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_set_unknow_sso(self):
		user_session = {
			"user_connections_logout": {
				"inactivity": {
					"authentication": {
						"terminate": {
							"now": True
						}
					},
					"other": {
						"terminate": {
							"now": True
						}
					}
				}
			},
			"reported": {
				"authentication": {
					"keep_alive": True
				},
				"other": {
					"keep_alive": True
				}
			}
		}

		user_setting.user_session(**user_session)
		resp = user_setting.show_user_setting()
		Assertion.assert_regular(json.dumps(resp), 'keep_alive',
								 "ERR:Failed to select Local authentication method.")

# Navigate to GUI->Users->Settings page, in "User session settings" section, in the inactivity timeout field,
# enter the number of minutes or use the default value 5 minutes
class inactive_timeout(Test):
	uuid = "SOSAIOT-TC-76091"

	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '7')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_set_inactive_time(self):
		user_session = {
			"inactivity_time_in_minutes": 5
		}

		user_setting.user_session(**user_session)
		resp = user_setting.show_user_setting()
		Assertion.assert_regular(json.dumps(resp), '"inactivity_timeout": 5',
								 "ERR:Failed to select Local authentication method.")

	def test_02_guest_user_login(self):
		guest_user = users.UserLoginApi(headers, '192.168.168.168', 'test', 'password')
		is_authenticated, bearer_token = guest_user.local_user_login()
		logger.info(bearer_token)
		for remaining in range(300, 0, -1):
			sys.stdout.write(f"\rWaiting for {remaining} seconds...")
			sys.stdout.flush()
			time.sleep(1)  # Sleep for 1 min
		sys.stdout.write("\rTime's up! \n")
		logger.info("Inactive more then 5 mins")

	def test_03_session_details(self):
		response_get = user_status.show_user_status()
		Assertion.assert_not_regular(json.dumps(response_get), '"name": "test"', 'err: User is still active')
		logger.info("test user already inactive")

		logger.info("************************************")
		logger.info(response_get)
		logger.info("***********************************")

# verify the configuration for User session settings should be included in the TSR file.
class validate_user_session_inTSR(Test):
	uuid = "SOSAIOT-TC-76090"

	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '8')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_check_tsr(self):
		output = tsr_ojb.download_tsr()
		with open('/tmp/techSupport', 'r') as tsr:
			doc = tsr.read()
			flag = True if re.search(r'test', doc) else False
			Assertion.assert_equal(flag, True, "ERR: User deatils not correct in tsr")
			logger.info("User details present")

			flag = True if re.search(r'User Session Setting', doc) else False
			Assertion.assert_equal(flag, True, "ERR: User setting session are not correct in tsr")
			logger.info("User session setting present")

			os.remove('/tmp/techSupport')

#  Verify empty the user log name is not allowed
class empty_text_error(Test):
	uuid = "SOSAIOT-TC-76093"

	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '9')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_appflow_details(self):
		app_flow.login_ui()
		app_flow.go_to_user_session_page()
		app_flow.verify_empty_text_error(error = "You must enter a user name for logging with'If SSO fails to identify the user'")
		app_flow.logout_ui()

# Don't allow traffic from these services to prevent user logout on inactivity
class prevent_connection_logout(Test):
	uuid = "SOSAIOT-TC-76092"

	def test_00_show_testcase_info(self):
		show_testcase_info(Parameter.TESTPLAN, '10')
		Assertion.assert_equal(True, True, "ERR: show testcase info failed")

	def test_01_set_unknow_sso(self):
		user_session = {
			"prevent_inactivity_logout": {
				"service": "ftp"
			}
		}

		user_setting.user_session(**user_session)
		resp = user_setting.show_user_setting()
		Assertion.assert_regular(json.dumps(resp), "prevent_inactivity_logout",
								 "ERR:Failed to select Local authentication method.")
		logger.info("prevent_inactivity_logout configured")






