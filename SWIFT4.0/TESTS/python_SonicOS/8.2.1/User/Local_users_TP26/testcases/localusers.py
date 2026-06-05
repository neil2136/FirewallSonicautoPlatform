import sys
import os
import json
import re

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_users_TP26')

from definition.initial_parameter import *

class Local_UserConfig(Test):
    uuid = 'NonTC'

    # creating expired and pruned user
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'Everyone','SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 1,
            "prune_on_expiry": True
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

        #creating expired but not pruned user
    def test_02_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test2',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'Everyone', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 1,
            "prune_on_expiry": False


        }
        resp =local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test2"', 'err: Failed to create localuser')
     #creating local user
    def test_03_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test123',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'Everyone'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
        }

        resp =local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test123"', 'err: Failed to create localuser')




    


class TC26_Enable_prune_expired_user_Accounts(Test):

    uuid = "SOSAIOT-TC-75611"
    description = show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_enable_prune_on_expiry(self):
        stage_description = 'Enable Prune expired user accounts'
        logger.info(stage_description)
        user={

                    "apply_password_constraints": True,
                    "prune_on_expiry": True

        }
        resp = local_user.local_settings(**user)
        resp1 = local_user.show_local_settings()
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"prune_on_expiry": true', 'err: Failed to enable prune on expiry')

class TC27_Disable_prune_expired_user_Accounts(Test):

    uuid = "SOSAIOT-TC-75629"
    description = show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_disable_prune_on_expiry(self):
        stage_description = 'Disable Prune expired user accounts'
        logger.info(stage_description)
        user={

                    "apply_password_constraints": True,
                    "prune_on_expiry": False

        }
        resp = local_user.local_settings(**user)
        resp1 = local_user.show_local_settings()
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"prune_on_expiry": false', 'err: Failed to disable prune on expiry')

class TC28_Enable_Apply_Password_constraints(Test):

    uuid = "SOSAIOT-TC-75612"
    description = show_testcase_info(Parameter.TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_Enable_Apply_Password_constraints(self):
        stage_description = 'Enable Apply Password constraints'
        logger.info(stage_description)
        user={

                    "apply_password_constraints": True,
                    "prune_on_expiry": False

        }
        resp = local_user.local_settings(**user)
        resp1 =local_user.show_local_settings()
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"apply_password_constraints": true', 'err: Failed to  enable password constraints')

class TC29_Disable_Apply_Password_constraints(Test):

    uuid = "SOSAIOT-TC-75630"
    description = show_testcase_info(Parameter.TESTPLAN, '29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_Disable_Apply_Password_constraints(self):
        stage_description = 'Disable Apply Password constraints'
        logger.info(stage_description)
        user={

                    "apply_password_constraints": False,
                    "prune_on_expiry": False

        }
        resp =local_user.local_settings(**user)
        resp1 = local_user.show_local_settings()
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"apply_password_constraints": false', 'err: Failed to disable password constraints')

class TC30_AccountLifetime_never_expires(Test):
    uuid = "SOSAIOT-TC-75613"
    description = show_testcase_info(Parameter.TESTPLAN, '30', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_AccountLifetime_never_expires(self):
        user = {
            "action":"edit",
            "username":"test123", 
            "userpassword":"S0nic@uto",
            "account_lifetime" : False
        }
        
        resp = local_user.local_user(**user)
        resp1 = local_user.show_local_users()
        time.sleep(10)
        user_data = json.dumps(resp1)
        Assertion.assert_regular(user_data, '"name": "test123"', 'err: User test123 not found')
        Assertion.assert_regular(json.dumps(resp1), '"account_lifetime": {}', 'err: Account lifetime never expires failed')

class TC31_AccountLifetime_byMinutes_pruneAccountUnchecked(Test):
    uuid = "SOSAIOT-TC-75631"
    description = show_testcase_info(Parameter.TESTPLAN, '31', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_AccountLifetime_byMinutes_pruneAccountUnchecked(self):
        stage_description = 'Verify AccountLifetime by Minutes with Prune account upon expiration unchecked'
        logger.info(stage_description)

        user = {
            "action":"edit",
            "username":"test123",
            "userpassword":"S0nic@uto",
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
           }

                                  
           


        
        resp =local_user.local_user(**user)
        resp1 =local_user.show_local_users()
       
        Assertion.assert_regular(json.dumps(resp1), '"account_lifetime": {"minutes": 30}', 'err: Account lifetime never expires failed')
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"prune_on_expiry": false','err: Account lifetime never expires failed')


class TC32_AccountLifetime_byMinutes_pruneAccountChecked(Test):
    uuid = "SOSAIOT-TC-75614"
    description = show_testcase_info(Parameter.TESTPLAN, '32', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_AccountLifetime_byMinutes_pruneAccountChecked(self):
        stage_description = 'Verify AccountLifetime by Minutes with Prune account upon expiration checked'
        logger.info(stage_description)

        user = {
            "action": "edit",
            "username": "test123",
            "userpassword": "S0nic@uto",
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
        }

        resp = local_user.local_user(**user)
        resp1 = local_user.show_local_users()
      
        Assertion.assert_regular(json.dumps(resp1), '"account_lifetime": {"minutes": 30}','err: Account lifetime never expires failed')
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"prune_on_expiry": true','err: Account lifetime never expires failed')



class TC33_AccountLifetime_byHours_pruneAccountUnChecked(Test):
    uuid = "SOSAIOT-TC-75615"
    description = show_testcase_info(Parameter.TESTPLAN, '33', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_AccountLifetime_byHours_pruneAccountUnChecked(self):
        stage_description = 'Verify AccountLifetime by Hours with Prune account upon expiration checked'
        logger.info(stage_description)

        user = {
            "action": "edit",
            "username": "test123",
            "userpassword": "S0nic@uto",
            "account_lifetime": True,
            "lifetype": "hours",
            "accountlifetime": 2,
            "prune_on_expiry": False
        }

        resp = local_user.local_user(**user)
        resp1 = local_user.show_local_users()
      
        Assertion.assert_regular(json.dumps(resp1), '"account_lifetime": {"hours": 2}','err: Account lifetime never expires failed')
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"prune_on_expiry": false','err: Account lifetime never expires failed')

class TC34_AccountLifetime_byHours_pruneAccountChecked(Test):
    uuid = "SOSAIOT-TC-75632"
    description = show_testcase_info(Parameter.TESTPLAN, '34', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_AccountLifetime_byHours_pruneAccountChecked(self):
        stage_description = 'Verify AccountLifetime by Hours with Prune account upon expiration checked'
        logger.info(stage_description)

        user = {
            "action": "edit",
            "username": "test123",
            "userpassword": "S0nic@uto",
            "account_lifetime": True,
            "lifetype": "hours",
            "accountlifetime": 2,
            "prune_on_expiry": True
        }

        resp = local_user.local_user(**user)
        resp1 = local_user.show_local_users()
       
        Assertion.assert_regular(json.dumps(resp1), '"account_lifetime": {"hours": 2}','err: Account lifetime never expires failed')
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"prune_on_expiry": true','err: Account lifetime never expires failed')

class TC35_AccountLifetime_byDays_pruneAccountUnChecked(Test):
    uuid = "SOSAIOT-TC-75616"
    description = show_testcase_info(Parameter.TESTPLAN, '35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_AccountLifetime_byDays_pruneAccountUnChecked(self):
        stage_description = 'Verify AccountLifetime by Days with Prune account upon expiration unchecked'
        logger.info(stage_description)

        user = {
            "action": "edit",
            "username": "test123",
            "userpassword": "S0nic@uto",
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 2,
            "prune_on_expiry": False
        }

        resp = local_user.local_user(**user)
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"account_lifetime": {"days": 2}','err: Account lifetime never expires failed')
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"prune_on_expiry": false','err: Account lifetime never expires failed')



class TC36_AccountLifetime_byDays_pruneAccountChecked(Test):
    uuid = "SOSAIOT-TC-75633"
    description = show_testcase_info(Parameter.TESTPLAN, '36', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_AccountLifetime_byDays_pruneAccountChecked(self):
        stage_description = 'Verify AccountLifetime by Days with Prune account upon expiration checked'
        logger.info(stage_description)

        user = {
            "action": "edit",
            "username": "test123",
            "userpassword": "S0nic@uto",
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 2,
            "prune_on_expiry": True
        }

        resp = local_user.local_user(**user)
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"account_lifetime": {"days": 2}','err: Account lifetime never expires failed')
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"prune_on_expiry": true','err: Account lifetime never expires failed')


class TC37_AccountLifetime_BoundaryCheck(Test):
    uuid = "SOSAIOT-TC-75622"
    description = show_testcase_info(Parameter.TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_AccountLifetime_BoundaryCheck(self):
        stage_description = 'Account Lifetime: Boundary check with invalid Days value'
        logger.info(stage_description)

        user = {
            "action": "edit",
            "username": "test123",
            "userpassword": "S0nic@uto",
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 12303,
            "prune_on_expiry": True
        }

        resp = local_user.local_user(**user, msg=True)
        time.sleep(10)
        Assertion.assert_regular(resp[1]['status']['info'][0]['message'], "out of bounds", "err: failed to throw error")

class TC38_AccountLifetime_NegativeCheck(Test):
    uuid = "SOSAIOT-TC-75623"
    description = show_testcase_info(Parameter.TESTPLAN, '38', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_AccountLifetime_NegativeCheck(self):
        stage_description = 'Account Lifetime: negetive test with aphabetic and symbolic characters'
        logger.info(stage_description)

        user = {
            "action": "edit",
            "username": "test123",
            "userpassword": "S0nic@uto",
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": "@31345",
            "prune_on_expiry": True
        }

        resp = local_user.local_user(**user, msg=True)
        time.sleep(10)
        Assertion.assert_regular(resp[1]['status']['info'][0]['message'], "Schema validation error", "err: failed to throw error")


class TC39_Login_with_expired_not_pruned_user(Test):
    uuid = "SOSAIOT-TC-75624"
    description = show_testcase_info(Parameter.TESTPLAN, '39', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    


    @repeat_method(3)
    def test_03_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Local_users_TP26/definition/ui_user.py ' + '-url ' + url + ' -user test2 -pwd S0nic@uto'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "test2"', "failed to get user status")

    def test_04_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")


class TC40_Login_with_expired_and_pruned_user(Test):
    uuid = "SOSAIOT-TC-75625"
    description = show_testcase_info(Parameter.TESTPLAN, '40', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '40')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    @repeat_method(3)
    def test_03_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Local_users_TP26/definition/ui_user.py ' + '-url ' + url + ' -user test1 -pwd S0nic@uto'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "test1"', "failed to get user status")

    def test_04_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

class TC41_Check_Account_lifetime_of_different_groups(Test):
    uuid = "SOSAIOT-TC-75626"
    description = show_testcase_info(Parameter.TESTPLAN, '41', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '41')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test6',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'Everyone', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
        }
        resp = local_user.local_user(**user_json)
        time.sleep(5)
        resp1 = local_user.show_local_user_by_name('test6')
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test6"', 'err: test6 not created')
        Assertion.assert_regular(json.dumps(resp1), 'account_lifetime','err: Failed to show account lifetime')

    def test_02_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)

        resp = local_user.delete_local_user_no_domain('test6')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test6"', 'err: user not deleted')


#check Remaining lifetime for user 'test123'
class TC42_Check_RemainingTime(Test):
    uuid = "SOSAIOT-TC-75617"
    description = show_testcase_info(Parameter.TESTPLAN, '42', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '42')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")



    def test_02_check_remaining_lifetime(self):
        resp = local_user.show_local_user_by_name('test123')
        Assertion.assert_regular(json.dumps(resp),'account_lifetime','err: Failed to show account lifetime')



class TC43_Edit_RemainingLifetime(Test):
    uuid = "SOSAIOT-TC-75618"
    description = show_testcase_info(Parameter.TESTPLAN, '43', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '43')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_02_edit_remaining_lifetime(self):
        user_json = {
            'action': 'edit',
            'username': 'test123',
            'userpassword': 'S0nic@uto',
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 2,
            "prune_on_expiry": True
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_user_by_name('test123')
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"account_lifetime": {"days": 2}', 'err: Failed to edit Remaining lifetime')




class TC48_Check_LocalUser_config_in_TSR(Test):
    uuid = "SOSAIOT-TC-75620"
    description = show_testcase_info(Parameter.TESTPLAN, '48', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '48')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_Check_LocalUser_config_in_TSR(self):


        resp1 = local_user.show_local_user_by_name('test123')
        Assertion.assert_regular(json.dumps(resp1), '"name": "test123"', 'err: Failed to show user test123')
        output = diagnostic.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            flag = True if re.search('test123', doc) else False
            Assertion.assert_equal(flag, True, "ERR: can't fine test123 config in tsr")
            os.remove('/tmp/techSupport')


class TC49_Check_LocalUser_logs(Test):
    uuid = "SOSAIOT-TC-75627"
    description = show_testcase_info(Parameter.TESTPLAN, '49', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '49')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_Check_LocalUser_logs(self):


        resp1=logs.get_log_categories_by_name('Users')
        time.sleep(5)
        Assertion.assert_regular(json.dumps(resp1), '"name": "Users"', 'err: User logs not found')


class TC52_Restart_firewall_and_check_remaining_time(Test):
    uuid = "SOSAIOT-TC-75621"
    description = show_testcase_info(Parameter.TESTPLAN, '52', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '52')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_restart_firewall(self):


        resp1=restart.restart_now()
        resp = local_user.show_local_user_by_name('test123')
        Assertion.assert_regular(json.dumps(resp), 'account_lifetime', 'err: Failed to show account lifetime')



class TC51_Check_PrunedAndExpired_user_removed(Test):
    uuid = "SOSAIOT-TC-75628"
    description = show_testcase_info(Parameter.TESTPLAN, '51', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '51')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_CheckUser_removed(self):
        time.sleep(5)
        resp1 = local_user.show_local_group_by_name('Trusted Users')
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: test2 not removed from Trusted User')
        resp2 = local_user.show_local_group_by_name('Everyone')
        Assertion.assert_not_regular(json.dumps(resp2), '"name": "test1"','err: test2 not removed from Everyone')
        resp3 = local_user.show_local_group_by_name('Guest Services')
        Assertion.assert_not_regular(json.dumps(resp3), '"name": "test1"','err: test2 not removed from Guest Services')






class TC45_delete_Localuser(Test):
    uuid = "SOSAIOT-TC-75619"
    description = show_testcase_info(Parameter.TESTPLAN, '45', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '45')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_delete_localUser(self):
        stage_description = 'Delete the user with account lifetime configured'
        logger.info(stage_description)

        resp =local_user.delete_local_user_no_domain('test123')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test123"', 'err: user not deleted')
        resp = local_user.delete_local_user_no_domain('test1')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test1"', 'err: user not deleted')
        resp = local_user.delete_local_user_no_domain('test2')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test2"', 'err: user not deleted')



