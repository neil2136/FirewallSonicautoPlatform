import json
import subprocess
from definition.settings import *


class TC001_Ula_Auth_combinations(Test):
    uuid = "NonTC"

    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        access_rule_option = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_02_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

class TC075_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76928"
    description = show_testcase_info(TESTPLAN, '2477742', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477742')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user is not created successfully")
        tacacs_user_info = user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_tacacs_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        # Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'user1', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.guest_user_login()
        # Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with tacacs user")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        # Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC076_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76929"
    description = show_testcase_info(TESTPLAN, '2477743', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477743')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user is not created successfully")
        tacacs_user_info = user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_tacacs_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'user1', 'wpassword')
        time.sleep(60)
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with wrong tacacs user")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC077_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76938"
    description = show_testcase_info(TESTPLAN, '2477752', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477752')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user is not created successfully")
        tacacs_user_info = user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user test got failed")

    def test_03_enable_tacacslocal_user_auth_method(self):
        logger.info('Select tacacs local authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select tacacs-local authentication method.")

    def test_04_tacacs_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        # Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'user1', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.guest_user_login()
        # Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with tacacs user")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        # Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC078_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76939"
    description = show_testcase_info(TESTPLAN, '2477753', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477753')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user is not created successfully")
        tacacs_user_info = user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user test got failed")

    def test_03_enable_tacacslocal_user_auth_method(self):
        logger.info('Select tacacs local authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select tacacs-local authentication method.")

    def test_04_tacacs_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'user1', 'wpassword')
        time.sleep(60)
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with wrong tacacs user")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC079_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76940"
    description = show_testcase_info(TESTPLAN, '2477754', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477754')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user is not created successfully")
        tacacs_user_info = user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user test got failed")

    def test_03_enable_tacacslocal_user_auth_method(self):
        logger.info('Select tacacs local authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select tacacs-local authentication method.")

    def test_04_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth_1",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth_1', 'S0nic@uto')
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_not_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth_1")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

    def test_06_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC080_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76941"
    description = show_testcase_info(TESTPLAN, '2477755', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477755')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user is not created successfully")
        tacacs_user_info = user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs user test got failed")

    def test_03_enable_tacacslocal_user_auth_method(self):
        logger.info('Select tacacs local authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select tacacs-local authentication method.")

    def test_04_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth_1",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth_1', 'wS0nic@uto')
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with wrong local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth_1")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

    def test_06_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")
