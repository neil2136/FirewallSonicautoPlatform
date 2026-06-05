import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Users_api')

from definition.settings import *


class TC01_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47809"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_get_GuestUser_settings(self): 
                
        response_get=guest_user.show_user_guest_settings()                
        logger.info(response_get) 
        Assertion.assert_regular(json.dumps(response_get), '"show_guest_status_window": true', 'err: Failed to get guest users settings') 

class TC02_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47810"
    description = show_testcase_info(Parameter.TESTPLAN, '02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_create_guestuser_profile(self): 
        add_guestuser_profile = {
          'action': 'add',
          'profilename': 'guest123',
          'generate': True,
          'generatename': True,
          'generatepassword': False,
          'activate_on_login': True,
          'enable_account': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 2,
          'acco_lifetype': 'days'
          }
        response=guest_user.user_guest_profile(**add_guestuser_profile)                
        logger.info(response)
        response_get=guest_user.show_user_guest_profile()                 
        Assertion.assert_regular(json.dumps(response_get), '"name": "guest123"', 'err: Failed to create guest users profile') 

class TC04_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47811"
    description = show_testcase_info(Parameter.TESTPLAN, '04', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_guestuser_profile(self): 
        edit_guestuser_profile = {
          'action': 'edit',
          'profilename': 'guest123',
          'generate': True,
          'generatename': True,
          'generatepassword': True,
          'activate_on_login': True,
          'enable_account': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 2,
          'acco_lifetype': 'hours'
          }
        response=guest_user.user_guest_profile(**edit_guestuser_profile)                
        logger.info(response)
        response_get=guest_user.show_user_guest_profile()                 
        Assertion.assert_regular(json.dumps(response_get), '"account_lifetime": {"hours": 2}', 'err: Failed to edit guest users profile') 
        
class TC06_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47812"
    description = show_testcase_info(Parameter.TESTPLAN, '06', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_add_guestuser_account(self): 
        add_guestuser_account = {
          'action': 'add',
          'accountname': 'guest1',
          'password': "password",
          'activate_on_login': True,
          'enable_guest_service_privilege': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 3,
          'acco_lifetype': 'days',
          'prune_on_expiry': True
          
          }
        response=guest_user.user_guest_account(**add_guestuser_account)                
        logger.info(response)
        response_get=guest_user.show_user_guest_account()                 
        Assertion.assert_regular(json.dumps(response_get), '"name": "guest1"', 'err: Failed to create guest users account') 
                
class TC10_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47813"
    description = show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 
    
    def test_edit_guestuser_accountByName(self):
        response_get=guest_user.show_user_guest_account_by_name('guest1')
                         
        edit_guestuser_account = {
          'action': 'edit',
          'accountname': 'guest1',
          'password': "password",
          'activate_on_login': True,
          'enable_guest_service_privilege': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 1,
          'acco_lifetype': 'hours',
          'prune_on_expiry': True
          
          }
        response=guest_user.user_guest_account(**edit_guestuser_account)                
        logger.info(response)
        response_get=guest_user.show_user_guest_account_by_name('guest1')                 
        Assertion.assert_regular(json.dumps(response_get), '"account_lifetime": {"hours": 1}', 'err: Failed to edit guest users account') 
                
class TC17_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47814"
    description = show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_post_guestuser_profile(self): 
        add_guestuser_profile = {
          'action': 'add',
          'profilename': 'guest1',
          'generate': True,
          'generatename': True,
          'generatepassword': False,
          'activate_on_login': True,
          'enable_account': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 1,
          'acco_lifetype': 'hours'
          }
        response=guest_user.user_guest_profile(**add_guestuser_profile)                
        logger.info(response)
        response_get=guest_user.show_user_guest_profile()                 
        Assertion.assert_regular(json.dumps(response_get), '"name": "guest1"', 'err: Failed to create guest users profile') 
                
    def test_post_duplicate_guestuser_profile(self): 
        duplicate_guestuser_profile = {
          'action': 'add',
          'profilename': 'guest1',
          'generate': True,
          'generatename': True,
          'generatepassword': False,
          'activate_on_login': True,
          'enable_account': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 1,
          'acco_lifetype': 'hours'
          }
        response=guest_user.user_guest_profile(**duplicate_guestuser_profile)                
        logger.info(response)
        response_get=guest_user.show_user_guest_profile()                 
        Assertion.assert_not_regular(json.dumps(response_get), 'Already exists.', 'err: Failed to duplicate guest users profile') 
                        
        
class TC18_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47815"
    description = show_testcase_info(Parameter.TESTPLAN, '18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 
    
    def test_create_guestuser_account(self): 
        add_guestuser_account = {
          'action': 'add',
          'accountname': 'guest2',
          'password': "password",
          'activate_on_login': True,
          'enable_guest_service_privilege': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 1,
          'acco_lifetype': 'hours',
          'prune_on_expiry': True
          
          }
        response=guest_user.user_guest_account(**add_guestuser_account)                
        logger.info(response)
        response_get=guest_user.show_user_guest_account_by_name('guest2')                 
        Assertion.assert_regular(json.dumps(response_get), '"name": "guest2"', 'err: Failed to create guest users account') 
                        
    def test_duplicate_guestuser_account(self): 
        duplicate_guestuser_account = {
          'action': 'add',
          'accountname': 'guest2',
          'password': "password",
          'activate_on_login': True,
          'enable_guest_service_privilege': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 1,
          'acco_lifetype': 'hours',
          'prune_on_expiry': True
          
          }
        response=guest_user.user_guest_account(**duplicate_guestuser_account)                
        logger.info(response)
        response_get=guest_user.show_user_guest_account_by_name('guest2')                 
        Assertion.assert_not_regular(json.dumps(response_get), 'Already exists.', 'err: Failed to duplicate guest users account') 
                                
        
        
        
        
          
