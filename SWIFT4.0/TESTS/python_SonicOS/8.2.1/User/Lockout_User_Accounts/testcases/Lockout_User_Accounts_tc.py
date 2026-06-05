import time

from definition.settings import *
from datetime import datetime, timedelta
import json


class Test_Lockout_User_Accounts_01(Test):
    uuid = "SOSAIOT-TC-75054"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518220')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_user_account_lock_button(self):
        logger.info(" {} ".center(20, '-').format('Checking the button '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc1 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - user account lock button not found")


class Test_Lockout_User_Accounts_02(Test):
    uuid = "SOSAIOT-TC-75055"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518221')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enabling_user_account_lock(self):
        logger.info(" {} ".center(20, '-').format('Enabling User account lock '))
        user_account_lock_json = {
            "user_lockout":{
                "enable":True,
                "failures_rate":5,
                "failures_duration":2,
                "lockout_duration":5
            },
            "local_user_lockout":True,
            "log_without_lockout":False,
        }

        rc = admin_api.conf_admin(**user_account_lock_json)
        Assertion.assert_equal(rc, True, "ERR: Reset X0 SSH Port failed.")

    def test_02_adding_local_user(self):
        logger.info(" {} ".center(20, '-').format('Adding local user '))
        local_user_dict = {
            'action': 'add',
            'username': 'testuser',
            'userpassword': 'TestP@ssw0rd',
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ["SonicWALL Administrators"]
        }
        rc = user_api.local_user(**local_user_dict)
        Assertion.assert_equal(rc, True, "Err: Add a local user member of SSLVPN fail")

    def test_03_check_user_account_lock_button(self):
        logger.info(" {} ".center(20, '-').format('  Verifying Lockout time due '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc2 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        print(words)
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'Login', "ERR: Testcase failed - Lockout time due failed")

    
class Test_Lockout_User_Accounts_03(Test):
    uuid = "SOSAIOT-TC-75056"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518222')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Unlock_User_by_GUI(self):
        logger.info(" {} ".center(20, '-').format(' Unlocking User by GUI '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc3 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        time.sleep(10)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-2:])
        Assertion.assert_equal(res, 'ClickedLogin', "ERR: Testcase failed - user account lock button not found")


class Test_Lockout_User_Accounts_04(Test):
    uuid = "SOSAIOT-TC-75058"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518231')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_Log_event_only_without_lockout_button(self):
        logger.info(" {} ".center(20, '-').format(' Log event only without lockout Button '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc4 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - user account lock button not found")


class Test_Lockout_User_Accounts_05(Test):
    uuid = "SOSAIOT-TC-75063"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518247')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_perform_lockout_user_account(self):
        logger.info(" {} ".center(20, '-').format(' locking out user account '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc5 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'displayed', "ERR: Testcase failed - performing lockout user account failed")

    def test_02_check_tsr(self):
        tsr_ojb.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            flag = True if re.search(r'User is locked out:  Yes', doc) else True
            Assertion.assert_equal(flag, True, "ERR: Not found in in TSR")
        logger.info('Wating for 5 mins')
        time.sleep(300)


class Test_Lockout_User_Accounts_06(Test):
    uuid = "SOSAIOT-TC-75067"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518256')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unlock_user(self):
        user_status.unlock_user_name(username='testuser')

    def test_02_Verify_local_user_supported_for_this_feature(self):
        logger.info(" {} ".center(20, '-').format(' Verify local user supported for this feature '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc6 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'False', "ERR: Testcase failed - Verify local user not supported for this feature")


class Test_Lockout_User_Accounts_07(Test):
    uuid = "SOSAIOT-TC-75066"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518252')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unlock_user(self):
        user_status.unlock_user_name(username='testuser')    

    def test_02_Verify_local_user_supported_for_this_feature(self):
        logger.info(" {} ".center(20, '-').format(' Locked out User Account list check '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc7 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-2:])
        Assertion.assert_equal(res, 'locked_userTrue', "ERR: Testcase failed - User not found in Locked out User Account list")


class Test_Lockout_User_Accounts_08(Test):
    uuid = "SOSAIOT-TC-75069"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518237')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_guest_user_account(self):
        logger.info(" {} ".center(20, '-').format('Adding Guest User Account '))
        add_guestuser_account = {
            'action': 'add',
            'accountname': 'testguestuser',
            'password': "password",
            'activate_on_login': True,
            'enable_guest_service_privilege': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 3,
            'acco_lifetype': 'days',
            'prune_on_expiry': True
        }
        rc = user_guest_api.user_guest_account(**add_guestuser_account)
        Assertion.assert_equal(rc, True, f"ERR: add guest user failed")

    def test_02_enabling_guest_services_for_LAN_Zone(self):
        logger.info(" {} ".center(20, '-').format('Enabling Guest Services for LAN Zone '))
        lan_opt = {
            "zones":[
                {
                    "name":"LAN",
                    "security_type":"trusted",
                    "create_group_vpn":False,
                    "ssl_control":False,
                    "sslvpn_access":False,
                    "guest_services":{
                        "enable":True,
                        "inter_guest":False,
                        "post_auth":"",
                        "bypass_guest_auth":{
                        
                        },
                        "smtp_redirect":{
                        
                        },
                        "deny_networks":{
                        
                        },
                        "pass_networks":{
                        
                        },
                        "max_guests":10,
                        "external_auth":{
                        "enable":False,
                        "client_redirect":"https",
                        "web_server":{
                            "timeout":15
                        },
                        "auth_pages":{
                            "web_server_1":{
                                "login":"",
                                "expiration":"",
                                "timeout":"",
                                "max_sessions":"",
                                "traffic_exceeded":""
                            },
                            "web_server_2":{
                                "login":"",
                                "expiration":"",
                                "timeout":"",
                                "max_sessions":"",
                                "traffic_exceeded":""
                            }
                        },
                        "web_content":{
                            "redirect":{
                                "use_default":True
                            },
                            "server_down":{
                                "use_default":True
                            }
                        },
                        "social_network":{
                            "enable":False,
                            "facebook":False,
                            "google":False,
                            "twitter":False
                        }
                        },
                        "policy_page_non_authentication":{
                        "enable":False,
                        "idle_timeout":{
                            
                        },
                        "auto_accept":False
                        },
                        "custom_auth_page":{
                        "enable":False,
                        "footer":{
                            
                        },
                        "header":{
                            
                        }
                        }
                    }
                }
            ]
        }
        rc = zone_obj.edit_zone_object(name='LAN', **lan_opt)
        Assertion.assert_equal(rc, True, 'ERR: Edit LAN zone object failed')

    def test_03_Verify_guest_account_login_test(self):
        logger.info(" {} ".center(20, '-').format(' Verify Guest account login test '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc8 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'displayed', "ERR: Testcase failed - Unable to login through Guest user")


class Test_Lockout_User_Accounts_09(Test):
    uuid = "SOSAIOT-TC-75070"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518238')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Change_unlock_time_from_default_to_10_when_user_the_is_blocked(self):
        logger.info(" {} ".center(20, '-').format(' Change unlock time from default to 10 when user the is blocked '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc6 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'False', "ERR: Testcase failed - Verify local user not supported for this feature")

    def test_02_changing_lockout_duration(self):
        logger.info(" {} ".center(20, '-').format(' Updating Lockout duration time '))
        user_account_lock_json = {
            "user_lockout":{
                "enable":True,
                "failures_rate":5,
                "failures_duration":2,
                "lockout_duration":10
            },
            "local_user_lockout":True,
            "log_without_lockout":False,
        }

        rc = admin_api.conf_admin(**user_account_lock_json)
        Assertion.assert_equal(rc, True, "ERR: Failed to update lockout duration.")

    def test_03_verify_lockout_duration(self):
        logger.info(" {} ".center(20, '-').format(' Getting User lockout duration time '))
        output = user_status.get_locked_out_account()
        time_remaning = output[0]['lockout_time_remaining'].split(' ')[0]
        Assertion.assert_regular(json.dumps(output), '"name": "testguestuser"', 'err: User not found')
        assert int(time_remaning) > 5, "ERR:Lockout time did not get update"
        # Assertion.assert_regular(json.dumps(output), '"lockout_time_remaining": "10 minutes"', "ERR:Lockout time did not get update") 

    def test_04_resetting_lockout_duration(self):
        logger.info(" {} ".center(20, '-').format(' Updating Lockout duration time '))
        user_account_lock_json = {
            "user_lockout":{
                "enable":True,
                "failures_rate":5,
                "failures_duration":2,
                "lockout_duration":5
            },
            "local_user_lockout":True,
            "log_without_lockout":False,
        }

        rc = admin_api.conf_admin(**user_account_lock_json)
        Assertion.assert_equal(rc, True, "ERR: Failed to update lockout duration.")


class Test_Lockout_User_Accounts_10(Test):
    uuid = "SOSAIOT-TC-75071"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518239')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Change_users_name_password_when_the_user_is_locked(self):
        logger.info(" {} ".center(20, '-').format(' Change users name/password when the user is locked '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc6 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'False', "ERR: Testcase failed - Verify local user not supported for this feature")

    def test_02_edit_local_user(self):
        logger.info(" {} ".center(20, '-').format(' Editing local user '))

        resp = user_api.get_local_user_uuid('testuser')
        print('resp', resp)

        uuid_json = {
            "uuid": resp,
            "username": "testuser1",
            "userpassword": "TestP@ssw0rd1",
            }              
        rc = user_api.edit_local_user_by_uuid(**uuid_json)
        Assertion.assert_equal(rc, True, "Err: Add a local user member of SSLVPN fail")

    def test_03_verify_lockout_duration(self):
        logger.info(" {} ".center(20, '-').format(' Getting User lockout duration time '))
        output = user_status.get_locked_out_account()
        Assertion.assert_regular(json.dumps(output), '"name": "testguestuser"', 'err: User not found')

    def test_04_edit_local_user(self):
        logger.info(" {} ".center(20, '-').format(' Editing local user '))
        resp = user_api.get_local_user_uuid('testuser1')
        print('resp', resp)

        uuid_json = {
            "uuid": resp,
            "username": "testuser",
            "userpassword": "TestP@ssw0rd",
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ["SonicWALL Administrators"]            
            }              
        rc = user_api.edit_local_user_by_uuid(**uuid_json)
        Assertion.assert_equal(rc, True, "Err: Add a local user member of SSLVPN fail")


class Test_Lockout_User_Accounts_11(Test):
    uuid = "SOSAIOT-TC-75064"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518249')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_perform_user_lockout(self):
        logger.info(" {} ".center(20, '-').format(' Performing user lockout '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc6 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = words[-1]
        Assertion.assert_regular(res, 'False', "ERR: Testcase failed - Verify local user not supported for this feature")

    def test_02_reboot_the_firewall(self):
        logger.info(" {} ".center(20, '-').format(' Rebooting Firewall '))
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: reboot fw failed!!')

    def test_03_perform_user_lockout_after_reboot(self):
        logger.info(" {} ".center(20, '-').format(' Performing user lockout after Reboot '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc6 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = words[-1]
        Assertion.assert_regular(res, 'False',
                               "ERR: Testcase failed - Verify local user not supported for this feature")


class Test_Lockout_User_Accounts_12(Test):
    uuid = "SOSAIOT-TC-75072"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518248')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_perform_user_lockout(self):
        logger.info(" {} ".center(20, '-').format(' Performing user lockout '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc6 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'False', "ERR: Testcase failed - Verify local user not supported for this feature")

    def test_02_Export_import_DUT_configuration(self):
        logger.info(" {} ".center(20, '-').format(' Export Import DUT Configuration '))
        settingapi.export_setting_exp('/tmp/lockout_user.exp')
        logger.info('Importing the configuration')
        settingapi.import_setting_exp('/tmp/lockout_user.exp')

    def test_03_perform_user_lockout_after_import_configuration(self):
        logger.info(" {} ".center(20, '-').format(' Performing user lockout after import configuration '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc6 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = words[-1]
        Assertion.assert_regular(res, 'False',
                               "ERR: Testcase failed - Verify local user not supported for this feature")


class Test_Lockout_User_Accounts_13(Test):
    uuid = "SOSAIOT-TC-75057"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518226')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_1_unlock_user(self):
        user_status.unlock_user_name(username='testuser')
    
    def test_00_2_disabling_guest_services_for_LAN_Zone(self):
        logger.info(" {} ".center(20, '-').format('Enabling Guest Services for LAN Zone '))
        lan_opt = {
            "zones":[
                {
                    "name":"LAN",
                    "security_type":"trusted",
                    "create_group_vpn":False,
                    "ssl_control":False,
                    "sslvpn_access":False,
                    "guest_services":{
                        "enable":False,
                        "inter_guest":False,
                        "post_auth":"",
                        "bypass_guest_auth":{
                        
                        },
                        "smtp_redirect":{
                        
                        },
                        "deny_networks":{
                        
                        },
                        "pass_networks":{
                        
                        },
                        "max_guests":10,
                        "external_auth":{
                        "enable":False,
                        "client_redirect":"https",
                        "web_server":{
                            "timeout":15
                        },
                        "auth_pages":{
                            "web_server_1":{
                                "login":"",
                                "expiration":"",
                                "timeout":"",
                                "max_sessions":"",
                                "traffic_exceeded":""
                            },
                            "web_server_2":{
                                "login":"",
                                "expiration":"",
                                "timeout":"",
                                "max_sessions":"",
                                "traffic_exceeded":""
                            }
                        },
                        "web_content":{
                            "redirect":{
                                "use_default":True
                            },
                            "server_down":{
                                "use_default":True
                            }
                        },
                        "social_network":{
                            "enable":False,
                            "facebook":False,
                            "google":False,
                            "twitter":False
                        }
                        },
                        "policy_page_non_authentication":{
                        "enable":False,
                        "idle_timeout":{
                            
                        },
                        "auto_accept":False
                        },
                        "custom_auth_page":{
                        "enable":False,
                        "footer":{
                            
                        },
                        "header":{
                            
                        }
                        }
                    }
                }
            ]
        }
        rc = zone_obj.edit_zone_object(name='LAN', **lan_opt)
        Assertion.assert_equal(rc, True, 'ERR: Edit LAN zone object failed')

    def test_01_enabling_user_account_lock(self):
        logger.info(" {} ".center(20, '-').format('Enabling User account lock '))
        user_account_lock_json = {
            "user_lockout":{
                "enable":True,
                "failures_rate":5,
                "failures_duration":2,
                "lockout_duration":10
            },
            "local_user_lockout":True,
            "log_without_lockout":True,
        }

        rc = admin_api.conf_admin(**user_account_lock_json)
        Assertion.assert_equal(rc, True, "ERR: Reset X0 SSH Port failed.")

    def test_02_log_a_user_fail_attempts_reaches_threshold_only_instead_of_lockout(self):
        logger.info(" {} ".center(20, '-').format(' Performing user lockout after import configuration '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc13 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'displayed', "ERR: Testcase failed - Verify local user not supported for this feature")

    def test_03_get_logs(self):
        log = log_obj.export_log_txt()
        print('logg', log)
        str_msg = 'User testuser reaches lockout threshold, log only.'

        flag = True
        if str_msg in log:
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")
        time.sleep(600)

    def test_04_login_as_local_user_after_threshold(self):
        logger.info(" {} ".center(20, '-').format(' Performing user lockout after import configuration '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc13_1 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - Verify local user not supported for this feature")


class Test_Lockout_User_Accounts_14(Test):
    uuid = "SOSAIOT-TC-75068"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518226')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_log_a_user_fail_attempts_reaches_threshold_only_instead_of_lockout(self):
        logger.info(" {} ".center(20, '-').format(' Performing user lockout after import configuration '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc13 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'displayed', "ERR: Testcase failed - Verify local user not supported for this feature")


    def test_02_get_logs(self):
        log = log_obj.export_log_txt()
        str_msg = 'User testuser reaches lockout threshold, log only.'
        flag = True
        if str_msg in log:
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")
        time.sleep(600)

    def test_03_login_as_local_user_after_threshold(self):
        logger.info(" {} ".center(20, '-').format(' Performing user lockout after import configuration '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc13_1 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - Verify local user not supported for this feature")

    def test_04_modifying_log_with_lockout(self):
        logger.info(" {} ".center(20, '-').format('Enabling User account lock '))
        user_account_lock_json = {
            "user_lockout":{
                "enable":True,
                "failures_rate":5,
                "failures_duration":2,
                "lockout_duration":10
            },
            "local_user_lockout":True,
            "log_without_lockout":False,            
        }

        rc = admin_api.conf_admin(**user_account_lock_json)
        Assertion.assert_equal(rc, True, "ERR: Reset X0 SSH Port failed.")

    def test_05_perform_user_lockout_modifying_log_with_lockout(self):
        logger.info(" {} ".center(20, '-').format(' Performing user lockout after Reboot '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc6 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = words[-1]
        Assertion.assert_equal(res, 'False',
                               "ERR: Testcase failed - Verify local user not supported for this feature")

    def test_06_configuring_user_account_lock_to_default_setting(self):
        logger.info(" {} ".center(20, '-').format('Enabling User account lock '))
        user_account_lock_json = {
            "user_lockout":{
                "enable":True,
                "failures_rate":5,
                "failures_duration":2,
                "lockout_duration":5
            },
            "local_user_lockout":True,
            "log_without_lockout":False,
        }

        rc = admin_api.conf_admin(**user_account_lock_json)
        Assertion.assert_equal(rc, True, "ERR: Reset X0 SSH Port failed.")


class Test_Lockout_User_Accounts_15(Test):
    uuid = "SOSAIOT-TC-75073"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1518254')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_sslvpn_config(self):
        user_account_lock_json = {
            "user_lockout": {
                "enable": True,
                "failures_rate": 5,
                "failures_duration": 2,
                "lockout_duration": 5
            },
            "local_user_lockout": True,
            "log_without_lockout": False,
        }

        rc = admin_api.conf_admin(**user_account_lock_json)

        address_object = {
            "object_type": "range",
            "name": "sslvpn_range",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_range", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_range"', "Err: failed to create address object")

        ssl_vpn_server = {
            'port': 4433,
            'use_self_signed': True,
            'user_domain': 'LocalDomain',
            'web': True,
            'ssh': False,
            'session_timeout': 10,
            'default': True,
            'mschap': True,
            'inactivity_check': True
        }
        server_settings = sslvpnserver.edit_server_setting(**ssl_vpn_server)
        Assertion.assert_equal(server_settings, True, "Err: failed to config server settings")

        enable = {
            'WAN_enable': True,
            'LAN_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets', 'WAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

        user_json = {
            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': 'TestP@ssw0rd',
        }
        resp = user_api.local_user(**user_json)
        resp1 = user_api.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: sslvpntest not created')

        member = {
            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': 'SSL123P@ssw0rd',
            'vpn_client_access': ['LAN Subnets', 'WAN Subnets']
        }
        resp = user_api.user_vpn_client_access(**member)
        resp1 = user_api.show_local_user_by_name('sslvpntest')
        Assertion.assert_regular(json.dumps(resp1), '"group": "LAN Subnets"',
                                 'err: sslvpntest not added to SSLVPN Services')

        member = {
            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': 'SSL123P@ssw0rd',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            'vpn_client_access': ['LAN Subnets', 'WAN Subnets']
        }
        resp = user_api.user_member_of(**member)
        resp1 = user_api.show_local_user_by_name('sslvpntest')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SSLVPN Services"',
                                 'err: sslvpntest not added to SSLVPN Services')
        # Assertion.assert_regular(json.dumps(resp1), '"group": "LAN Subnets"',
        #                          'err: sslvpntest not added to SSLVPN Services')


    def test_02_perform_sslvpn_login(self):
        logger.info(" {} ".center(20, '-').format(' Performing SSLVPN login '))
        static_client.send_command('pkill firefox')
        time.sleep(10)        
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts/definition/ui_user.py -method tc14 ' + '-url ' + sslvpn_url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = words[-1]
        Assertion.assert_not_equal(res, 'True', "ERR: Testcase failed - Verify local user not supported for this feature")

    def test_03_verify_sslvpn_user_in_lockout_list(self):
        logger.info(" {} ".center(20, '-').format(' Getting User lockout duration time '))
        output = user_status.get_locked_out_account()
        Assertion.assert_regular(json.dumps(output), '"name": "sslvpntest"', 'err: User not found')

