import sys
import os
import json
import time

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login/')

from definition.settings import *


class TC01_Local_User(Test):

    jira = "GEN7-45939"
    uuid = "SOSAIOT-TC-75382"
    description = show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test",
            "userpassword": "password",
            "force_password_change": True,
            "member_of": ["Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test"', 'err: Failed to create localuser') 
        Assertion.assert_regular(json.dumps(response_get), '"force_password_change": true,', 'err: Failed to enable ') 

    def test_03_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('WAN', 'LAN')
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
            'from': 'WAN',
            'to': 'LAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Trusted Users"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Trusted Users"','err: access rules not updated.')


    def test_03_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://172.17.1.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login/lib/ui_user_change_pw.py ' + '-url ' + url + ' -user test -pwd password'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('test')
        Assertion.assert_regular(json.dumps(status), '172.17.1.20', "failed to get user status")

    # logout user
    def test_04_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_05_show_local_user(self):
        response = local_user.show_local_user_by_name("test")
        Assertion.assert_regular(json.dumps(response), '"force_password_change": "false"', 'err: Failed to enable ')

                   
class TC02_Local_User(Test):
    uuid = "SOSAIOT-TC-75384"
    description = show_testcase_info(Parameter.TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_restart_fw(self):
      response = setting.boot_fw(mode=2)
      Assertion.assert_equal(response, True, "failed to do factory default")
      time.sleep(120)

    def test_02_Set_X1_Interface(self):
        x1_static = {
            'if': 'x1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_03_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test_user",
            "userpassword": "sonicauto",
            "member_of": ["Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test_user"', 'err: Failed to create localuser') 
        Assertion.assert_regular(json.dumps(response_get), '"force_password_change": false,', 'err: Failed to enable ') 

    @repeat_method(3)
    def test_04_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('WAN', 'LAN')
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
            'from': 'WAN',
            'to': 'LAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Trusted Users"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        time.sleep(120)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Trusted Users"','err: access rules not updated.')

    def test_05_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://172.17.1.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login/lib/ui_user.py ' + '-url ' + url + ' -user test_user -pwd sonicauto'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('test_user')
        Assertion.assert_regular(json.dumps(status), '172.17.1.20', "failed to get user status")

    # logout user
    def test_06_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_07_show_local_user(self):
        response = local_user.show_local_user_by_name("test_user")
        Assertion.assert_regular(json.dumps(response), '"force_password_change": false,', 'err: Failed to enable ')  
        

        
        
        
        
        
        
        
        
                        
                
