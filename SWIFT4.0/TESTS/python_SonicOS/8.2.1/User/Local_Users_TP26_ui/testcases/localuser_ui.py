import sys
import os
import json
import time
import datetime

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui')

from definition.settings import *

class TC01_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75528"
    description = show_testcase_info(Parameter.TESTPLAN, '1514446', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514446')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test4',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SSLVPN Services','SonicWALL Administrators','Trusted Users','Everyone']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test4"', 'err: Failed to create localuser')
    
    def test_02_verify_exapnd_veiw_of_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method verify_exapnd_veiw ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"

    def test_03_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test4')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test4"', 'err: Failed to create localuser')

class TC02_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75537"
    description = show_testcase_info(Parameter.TESTPLAN, '1514455', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514455')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_user_with_sslvpn_service(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method add_user_with_sslvpn_service ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"

    def test_02_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test12')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test12"', 'err: Failed to create localuser')

class TC03_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75538"
    description = show_testcase_info(Parameter.TESTPLAN, '1514456', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514456')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test12',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SSLVPN Services']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test12"', 'err: Failed to create localuser')

    def test_02_remove_user_with_sslvpn_service(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method remove_user_with_sslvpn_service ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'False', "Testcase failed"
    
    def test_03_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test12')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test12"', 'err: Failed to create localuser')

class TC04_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75518"
    description = show_testcase_info(Parameter.TESTPLAN, '1514436', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514436')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method add_user ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)

        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test_user"', 'err: Failed to create localuser')

    def test_02_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test_user')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test_user"', 'err: Failed to create localuser')
                  
class TC05_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75520"
    description = show_testcase_info(Parameter.TESTPLAN, '1514438', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514438')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': G_PASSWORD_NEW
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')
    
    def test_02_edit_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method edit_add_user_privilage ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out) 
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"
        resp1 = local_user.show_local_user_by_name('test1')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"', 'err: Failed to create localuser')

    def test_03_login_with_local_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method login_ui ' + '-url ' + url + ' -user test1 -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out) 
        status = user_status.show_user_status_by_name('test1')
        Assertion.assert_regular(json.dumps(status), '"name": "test1"', "failed to get user status")  

    def test_04_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

class TC06_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75521"
    description = show_testcase_info(Parameter.TESTPLAN, '1514439', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514439')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test2',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SonicWALL Administrators']
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test2"', 'err: Failed to create localuser')
    
    def test_02_edit_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method edit_remove_user_privilage ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'False', "Testcase failed"
        resp1 = local_user.show_local_user_by_name('test2')
        time.sleep(10)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"', 'err: Failed to create localuser')
    
    def test_03_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test2')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test2"', 'err: Failed to create localuser')
            
class TC07_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75524"
    description = show_testcase_info(Parameter.TESTPLAN, '1514442', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514442')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test3',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SonicWALL Administrators']
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test3"', 'err: Failed to create localuser')

    def test_02_delete_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method delete_user ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'False', "Testcase failed"
        resp1 = local_user.show_local_user_by_name('test3')
        time.sleep(10)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test3"', 'err: Failed to create localuser')

class TC08_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75522"
    description = show_testcase_info(Parameter.TESTPLAN, '1514440', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514440')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test19',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SonicWALL Administrators']
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test19"', 'err: Failed to create localuser')

    def test_02_adding_vpn_access_for_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method adding_vpn_access_for_user ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"
        resp1 = local_user.show_local_user_by_name('test19')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Firewalled Subnets"', 'err: Failed to create localuser')

    def test_03_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test19')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test19"', 'err: Failed to create localuser')

class TC09_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75523"
    description = show_testcase_info(Parameter.TESTPLAN, '1514441', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514441')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test20',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SonicWALL Administrators']
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test20"', 'err: Failed to create localuser')

    def test_02_add_vpn_access_client_for_users(self):
        user_json = {
            'action': 'add',
            'username': 'test20',
            'userpassword': G_PASSWORD_NEW,
            'vpn_client_access':['Firewalled Subnets']
        }
        resp = local_user.add_user_vpn_client_access(**user_json)
        Assertion.assert_equal(resp, True, "ERR: add vpn access client for user failed")


    def test_03_removing_vpn_access_for_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method removing_vpn_access_for_user ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
       
        resp1 = local_user.show_local_user_by_name('test20')
        time.sleep(10)
        Assertion.assert_not_regular(json.dumps(resp1), '"group": "Firewalled Subnets"', 'err: Failed to create localuser')

    def test_04_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test20')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test20"', 'err: Failed to create localuser')

class TC10_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75525"
    description = show_testcase_info(Parameter.TESTPLAN, '1514443', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514443')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test21',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SonicWALL Administrators']
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test21"', 'err: Failed to create localuser')

    def test_02_adding_multiple_vpn_access_for_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method adding_multiple_vpn_access_for_user ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"
        resp1 = local_user.show_local_user_by_name('test21')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"LAN Interface IP"', 'err: Failed to create localuser')
        Assertion.assert_regular(json.dumps(resp1), '"WAN Interface IP"', 'err: Failed to create localuser')

    def test_03_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test21')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test21"', 'err: Failed to create localuser')

class TC11_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75526"
    description = show_testcase_info(Parameter.TESTPLAN, '1514444', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514444')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test22',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SonicWALL Administrators']
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test22"', 'err: Failed to create localuser')

    def test_02_add_vpn_access_client_for_users(self):
        user_json = {
            'action': 'add',
            'username': 'test22',
            'userpassword': G_PASSWORD_NEW,
            'vpn_client_access':['LAN Interface IP','WAN Interface IP']
        }
        resp = local_user.add_user_vpn_client_access(**user_json)
        Assertion.assert_equal(resp, True, "ERR: add vpn access client for user failed")

    def test_03_removing_multiple_vpn_access_for_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method removing_multiple_vpn_access_for_user ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)
        resp1 = local_user.show_local_user_by_name('test22')
        time.sleep(10)
        Assertion.assert_not_regular(json.dumps(resp1), '"LAN Interface IP"', 'err: Failed to create localuser')
        Assertion.assert_not_regular(json.dumps(resp1), '"WAN Interface IP"', 'err: Failed to create localuser')

    def test_04_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test22')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test22"', 'err: Failed to create localuser')

class TC12_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75529"
    description = show_testcase_info(Parameter.TESTPLAN, '1514447', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514447')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test5',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['Everyone','SonicWALL Administrators','Trusted Users']
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test5"', 'err: Failed to create localuser')
    
    def test_02_delete_user_using_button(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method delete_user_using_button ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)

        resp1 = local_user.show_local_user_by_name('test5')
        time.sleep(10)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test5"', 'err: Failed to create localuser')

class TC13_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75530"
    description = show_testcase_info(Parameter.TESTPLAN, '1514448', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514448')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_apply_password_constraints_of_all_user(self):
        settings = {
            "apply_password_constraints": True
        }
        resp = local_user.local_settings(**settings)
        Assertion.assert_equal(resp, True, "ERR: failed to enable apply password constraints for all users")
        res = local_user.show_local_settings()
        Assertion.assert_regular(json.dumps(res), '"apply_password_constraints": True',"failed to disable apply password constraints for all users")

    def test_02_disable_apply_password_constraints_of_all_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method disable_apply_password_constraints_of_all_user ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)

    def test_03_verify_local_users_settings(self):
        resp = local_user.show_local_settings()
        Assertion.assert_regular(json.dumps(resp), '"apply_password_constraints": False',"failed to disable apply password constraints for all users")

class TC14_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75531"
    description = show_testcase_info(Parameter.TESTPLAN, '1514449', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514449')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_prune_on_expiry_for_user(self):
        settings = {
            "prune_on_expiry": True
        }
        resp = local_user.local_settings(**settings)
        Assertion.assert_equal(resp, True, "ERR: failed to enable_prune_on_expiry_for_user")
        res = local_user.show_local_settings()
        Assertion.assert_regular(json.dumps(res), '"prune_on_expiry": True',"failed to enable_prune_on_expiry_for_user")

    def test_02_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test6',
            'userpassword': G_PASSWORD_NEW,
            'account_lifetime':True,
            'lifetype':'minutes',
            'accountlifetime':1,
            'prune_on_expiry':True

        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test6"', 'err: Failed to create localuser')  
    
    @repeat_method(3)
    def test_03_verify_local_users(self):
        time.sleep(60)
        resp = local_user.show_local_user_by_name('test6')
        Assertion.assert_not_regular(json.dumps(resp), '"expired": " True"', 'err: Failed to create localuser')

class TC15_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75532"
    description = show_testcase_info(Parameter.TESTPLAN, '1514450', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514450')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_user(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method add_user_with_sonicwall_administrator_and_check_admin_column ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"
        resp1 = local_user.show_local_user_by_name('test7')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"', 'err: Failed to create localuser')

    def test_02_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test7')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test7"', 'err: Failed to create localuser')
        
class TC16_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75533"
    description = show_testcase_info(Parameter.TESTPLAN, '1514451', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514451')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test8',
            'userpassword': G_PASSWORD_NEW,
            'one_time_password': 'otp',
            'email_address': 'test@sonicwall.com'
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test8"', 'err: Failed to create localuser')

    def test_02_verify_local_users(self):
        resp = local_user.show_local_user_by_name('test8')
        Assertion.assert_regular(json.dumps(resp), '"one_time_password": {"otp": true}', 'err: Failed to create localuser')
        Assertion.assert_regular(json.dumps(resp), '"email_address": "test@sonicwall.com"', 'err: Failed to create localuser')

    def test_03_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test8')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test8"', 'err: Failed to create localuser')
    
class TC17_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75534"
    description = show_testcase_info(Parameter.TESTPLAN, '1514452', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514452')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test9',
            'userpassword': G_PASSWORD_NEW,
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test9"', 'err: Failed to create localuser') 
    
    def test_02_config_time_setting(self):
        time_ob = time_obj.show_time()
        time = time_ob['time']['time']
        date_1 = time_ob['time']['date']
        current_time = date_1+" "+time

        # Convert the string to a datetime object
        datetime_object = datetime.datetime.strptime(current_time, "%Y:%m:%d %H:%M:%S")

        time_delta = datetime.timedelta(days=5)  
        new_time = datetime_object + time_delta

        # Convert the datetime object to separate date and time strings
        date_string = new_time.strftime("%Y-%m-%d")
        time_string = new_time.strftime("%H:%M:%S")

        # Split the date string by the hyphen
        date = date_string.split("-")

        # Join the date components using colons
        new_date_string = ":".join(date)

        time_setting = {            
            "time": {               
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "use_ntp": False,
                "ntp_update_interval": 60,
                "time_zone": "pacific-time",
                "time": time_string,
                "date": new_date_string,
            }
        }
        resp = time_obj.set_time(**time_setting)
        resp1 = time_obj.show_time()
        Assertion.assert_regular(json.dumps(resp1), '"use_ntp": False','err: time config failed')
    
    @repeat_method(7)
    def test_03_verify_local_users(self):
        resp1 = local_user.show_local_user_by_name('test9')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test9"', 'err: Failed to create localuser')

    def test_04_config_time_setting(self):
        time_setting = {            
            "time": {               
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "use_ntp": True,
                "ntp_update_interval": 60,
                "time_zone": "pacific-time"
            }
        }
        resp = time_obj.set_time(**time_setting)
        resp1 = time_obj.show_time()
        Assertion.assert_regular(json.dumps(resp1), '"use_ntp": True','err: time config failed')

    def test_05_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test9')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test9"', 'err: Failed to create localuser')
    
class TC18_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75535"
    description = show_testcase_info(Parameter.TESTPLAN, '1514453', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514453')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test10',
            'userpassword': G_PASSWORD_NEW,
            'account_lifetime':True,
            'lifetype':'hours',
            'accountlifetime':1,
            'prune_on_expiry':True

        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test10"', 'err: Failed to create localuser') 
    
    @repeat_method(7)
    def test_02_config_time_setting(self):
        time_ob = time_obj.show_time()
        time = time_ob['time']['time']
        date_1 = time_ob['time']['date']
        current_time = date_1+" "+time

        # Convert the string to a datetime object
        datetime_object = datetime.datetime.strptime(current_time, "%Y:%m:%d %H:%M:%S")

        time_delta = datetime.timedelta(hours=1)  
        new_time = datetime_object + time_delta

        # Convert the datetime object to separate date and time strings
        date_string = new_time.strftime("%Y-%m-%d")
        time_string = new_time.strftime("%H:%M:%S")
        # Split the date string by the hyphen
        date = date_string.split("-")

        # Join the date components using colons
        new_date_string = ":".join(date)

        time_setting = {            
            "time": {               
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "use_ntp": False,
                "ntp_update_interval": 60,
                "time_zone": "pacific-time",
                "time": time_string,
                "date": new_date_string,
            }
        }
        resp = time_obj.set_time(**time_setting)
        resp1 = time_obj.show_time()
        Assertion.assert_regular(json.dumps(resp1), '"time": '+ '"'+time_string+'"','err: time config failed')
    
    @repeat_method(5)
    def test_03_verify_local_users(self):
        resp1 = local_user.show_local_user_by_name('test10')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"expired": true', 'err: Failed to create localuser')

    def test_04_config_time_setting(self):
        time_setting = {            
            "time": {               
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "use_ntp": True,
                "ntp_update_interval": 60,
                "time_zone": "pacific-time"
            }
        }
        resp = time_obj.set_time(**time_setting)
        resp1 = time_obj.show_time()
        Assertion.assert_regular(json.dumps(resp1), '"use_ntp": True','err: time config failed')

    def test_05_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test10')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test10"', 'err: Failed to create localuser')

class TC19_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75536"
    description = show_testcase_info(Parameter.TESTPLAN, '1514454', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514454')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test11',
            'userpassword': G_PASSWORD_NEW,
            'account_lifetime':True,
            'lifetype':'days',
            'accountlifetime':1,
            'prune_on_expiry':True

        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test11"', 'err: Failed to create localuser') 
    
    @repeat_method(5)
    def test_02_config_time_setting(self):
        time_ob = time_obj.show_time()
        time = time_ob['time']['time']
        date_1 = time_ob['time']['date']
        current_time = date_1+" "+time

        # Convert the string to a datetime object
        datetime_object = datetime.datetime.strptime(current_time, "%Y:%m:%d %H:%M:%S")

        time_delta = datetime.timedelta(days=1)  
        new_time = datetime_object + time_delta

        # Convert the datetime object to separate date and time strings
        date_string = new_time.strftime("%Y-%m-%d")
        time_string = new_time.strftime("%H:%M:%S")

        # Split the date string by the hyphen
        date = date_string.split("-")

        # Join the date components using colons
        new_date_string = ":".join(date)
        print('*************')
        print('new_date_string', new_date_string)
        time_setting = {            
            "time": {               
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "use_ntp": False,
                "ntp_update_interval": 60,
                "time_zone": "pacific-time",
                "time": time_string,
                "date": new_date_string,
            }
        }
        resp = time_obj.set_time(**time_setting)
        resp1 = time_obj.show_time()
        Assertion.assert_regular(json.dumps(resp1), '"date": '+ '"'+new_date_string+'"','err: time config failed')
    
    @repeat_method(5)
    def test_03_verify_local_users(self):
        resp1 = local_user.show_local_user_by_name('test11')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"expired": true', 'err: Failed to create localuser')

    def test_04_config_time_setting(self):
        time_setting = {            
            "time": {               
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "use_ntp": True,
                "ntp_update_interval": 60,
                "time_zone": "pacific-time"
            }
        }
        resp = time_obj.set_time(**time_setting)
        resp1 = time_obj.show_time()
        Assertion.assert_regular(json.dumps(resp1), '"use_ntp": True','err: time config failed')
    
    def test_05_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test11')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test11"', 'err: Failed to create localuser')

class TC20_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75539"
    description = show_testcase_info(Parameter.TESTPLAN, '1514457', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514457')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_user_with_guest_service_and_verify_tab(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method add_user_with_guest_service_and_verify_tab ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"
    
    def test_02_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test13')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test13"', 'err: Failed to create localuser')

class TC21_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75540"
    description = show_testcase_info(Parameter.TESTPLAN, '1514458', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514458')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test14',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['Everyone','Trusted Users','Guest Services'],
            'guest_login_uniqueness':True,
            'guest_idle_timeout':True,
            'timeout_type':'minutes',
            'guestidletimeout':15,

        }   
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test14"', 'err: Failed to create localuser') 

    def test_02_verify_local_users(self):
        resp = local_user.show_local_user_by_name('test14')
        Assertion.assert_regular(json.dumps(resp), '"guest_idle_timeout": {"minutes": 15}', 'err: Failed to create localuser')
    
    def test_03_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test14')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test14"', 'err: Failed to delete localuser')
        
class TC22_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75541"
    description = show_testcase_info(Parameter.TESTPLAN, '1514459', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514459')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_book_mark_without_sslvpn_serviceuser(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method verify_book_mark_without_sslvpn_serviceuser ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"
    
    def test_02_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test15')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test15"', 'err: Failed to create localuser')

class TC23_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75542"
    description = show_testcase_info(Parameter.TESTPLAN, '1514460', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514460')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test16',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SSLVPN Services']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test16"', 'err: Failed to create localuser')

    def test_02_add_bookmark(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method add_bookmark ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)

    def test_03_verify_local_users(self):
        resp1 = local_user.show_local_user_by_name('test16')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Book_mark"', 'err: Failed to create localuser')
        Assertion.assert_regular(json.dumps(resp1), '"host": "10.10.10.10"', 'err: Failed to create localuser')
    
    def test_04_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test16')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test16"', 'err: Failed to create localuser')

class TC24_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75543"
    description = show_testcase_info(Parameter.TESTPLAN, '1514461', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514461')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test17',
            'userpassword': G_PASSWORD_NEW,
            'member_of': ['SSLVPN Services']
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test17"', 'err: Failed to create localuser')
    
    def test_02_edit_user(self):
        user_json ={
            "user": {
                "local": {
                    "user": [
                        {
                            "name": "test17",
                            "password": "sonicauto",
                            "member_of": [
                                {
                                    "name": "Trusted Users"
                                },
                                {
                                    "name": "SSLVPN Services"
                                },
                                {
                                    "name": "Everyone"
                                }
                            ],
                            "bookmark": [
                                {
                                    "name": "10.10.10.15",
                                    "host": "Book_mark",
                                }
                            ]
                        }
                    ]
                }
            }
        }
        resp = local_user.edit_local_user_using_name(name="test17", **user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test17"', 'err: Failed to create localuser')

    def test_03_delete_bookmark(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method delete_bookmark ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'False', "Testcase failed"
    
    def test_04_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test17')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test17"', 'err: Failed to create localuser')

class TC25_LocalUsers(Test):
    uuid = "SOSAIOT-TC-75544"
    description = show_testcase_info(Parameter.TESTPLAN, '1532785', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1532785')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test18",
            "userpassword": G_PASSWORD_NEW,
            "force_password_change": True,
            "member_of": ["Everyone","Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test18"', 'err: Failed to create localuser') 

    @repeat_method(4)
    def test_02_add_access_rule(self):
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
            'user_included': {"group": "Trusted Users",},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Trusted Users"','err: access rules not updated.')


    def test_03_login(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method ui_user_change_pw ' + '-url ' + url + ' -user test18 -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)

        # check user status
        status = user_status.show_user_status_by_name('test18')
        ip1 = '13.0.0.3'
        ip2 = '13.0.0.2'
        ip3 = '13.0.0.4'
        if ip1 or ip2 or ip3 in json.dumps(status):
            res = True
        Assertion.assert_equal(res, True, "failed to get user status")

    # logout user
    def test_04_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_05_delete_user(self):
        resp = local_user.delete_local_user_no_domain('test18')
        resp1 = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test18"', 'err: Failed to create localuser')

class TC26_LocalUsers(Test):

    uuid = "SOSAIOT-TC-75545"
    description = show_testcase_info(Parameter.TESTPLAN, '1969006', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1969006')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")
        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.65')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
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
                'distinguished_name': 'test',
                'bind_password': 'password',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.65"', "failed to config ldap server")
            Assertion.assert_regular(json.dumps(resp), '"bind": {"distinguished_name": "test"}', "failed to config bind")

    def test_03_login(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method add_ldap_user_to_group ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        resp1 = local_user.show_local_group_by_name('SonicWALL Administrators')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"All LDAP Users"', 'err: Failed to import ldap user')

    # logout user
    def test_04_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

class TC27_LocalUsers(Test):
    jira = 'GEN8-11365'
    uuid = "SOSAIOT-TC-75527"
    description = show_testcase_info(Parameter.TESTPLAN, '1514445', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514445')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_vpn_access_for_all_ldap_users(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_TP26_ui/lib/ui_user.py -method adding_vpn_access_for_ldap_user ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"
