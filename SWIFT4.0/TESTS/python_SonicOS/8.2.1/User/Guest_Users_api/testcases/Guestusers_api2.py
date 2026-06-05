import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Users_api')

from definition.settings import *

class TC05_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47816"
    description = show_testcase_info(Parameter.TESTPLAN2, '05', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN2, '05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 
    def test_get_GuestProfile_byName(self): 
                
        response_get=guest_user.show_user_guest_profile_by_name('Default')                
        logger.info(response_get) 
        Assertion.assert_regular(json.dumps(response_get), '"name": "Default"', 'err: Failed to get guest profile') 


class TC09_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47817"
    description = show_testcase_info(Parameter.TESTPLAN2, '09', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN2, '09')
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
          'acco_lifetime': 1,
          'acco_lifetype': 'hours',
          'prune_on_expiry': True
          
          }
        response=guest_user.user_guest_account(**add_guestuser_account)                
        logger.info(response)
        response_get=guest_user.show_user_guest_account_by_name('guest1')                 
        Assertion.assert_regular(json.dumps(response_get), '"name": "guest1"', 'err: Failed to create guest users account') 
                
    def test_get_Guest_acccount_byName(self): 
                
        response_get=guest_user.show_user_guest_account_by_name('guest1')                
        logger.info(response_get) 
        Assertion.assert_regular(json.dumps(response_get), '"name": "guest1"', 'err: Failed to get guest user account') 

class TC21_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47821"
    description = show_testcase_info(Parameter.TESTPLAN2, '21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN2, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 
    def test_edit_nonexist_guestuser_profile(self): 
        edit_guestuser_profile = {
          'action': 'edit',
          'profilename': 'invalid profile'
          }
        response=guest_user.user_guest_profile(**edit_guestuser_profile)                
        logger.info(response)
        response_get=guest_user.show_user_guest_profile_by_name('invalid profile')                 
        Assertion.assert_not_regular(json.dumps(response_get), '"Command show user guest profile invalid does not match"', 'err: Failed to edit guest users profile') 
        
class TC22_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47819"
    description = show_testcase_info(Parameter.TESTPLAN2, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN2, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 
    def test_edit_nonexist_guestuser_account(self): 
        add_guestuser_account = {
          'action': 'edit',
          'accountname': 'invalid account',
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
        response_get=guest_user.show_user_guest_account_by_name('invalid account')                 
        Assertion.assert_not_regular(json.dumps(response_get), '"Command show user guest user invalid does not match"', 'err: Failed to create guest users account') 


class TC11_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47820"
    description = show_testcase_info(Parameter.TESTPLAN2, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN2, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 

    def test_get_guest_user_byUUID(self):
        resp = guest_user.get_user_guest_account_uuid('guest1')
        
        response_get = guest_user.show_user_guest_account_by_uuid(resp) 
        logger.info(response_get)
        Assertion.assert_regular(json.dumps(response_get), '"name": "guest1"', 'err: Failed to get guest user per uuid') 
        
class TC12_GuestUsers(Test):
    uuid = "SOSAIOT-TC-47818"
    description = show_testcase_info(Parameter.TESTPLAN2, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN2, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 

    def test_edit_guest_user_account_byUUID(self):
    
        resp = guest_user.get_user_guest_account_uuid('guest1')
        
        uuid_json = {
          'uuid': resp,
          'accountname': 'guest1',
          'password': "password",
          'activate_on_login': True,
          'enable_guest_service_privilege': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 2,
          'acco_lifetype': 'hours',
          'prune_on_expiry': True
            }              
        response = guest_user.edit_guest_user_account_by_uuid(**uuid_json)
        logger.info(response) 
        response_get = guest_user.show_user_guest_account_by_uuid(resp) 
        Assertion.assert_regular(json.dumps(response_get), '"account_lifetime": {"hours": 2}', 'err: Failed to edit guest user per uuid') 
        




