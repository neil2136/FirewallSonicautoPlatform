import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Local_Users_api')

from definition.settings import *

class TC001_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47889"
    description = show_testcase_info(Parameter.TESTPLAN, '1546919', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546919')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
 
          }
         
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test"', 'err: Failed to create localuser') 
                
class TC004_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47891"
    description = show_testcase_info(Parameter.TESTPLAN, '1546921', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546921')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_get_localuser_perName(self):      
        response_get=local_user.show_local_user_by_name('test')                
        logger.info(response_get) 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test"', 'err: Failed to get localuser by name') 
      
class TC005_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47892"
    description = show_testcase_info(Parameter.TESTPLAN, '1546922', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546922')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_put_localuser_per_name(self):
        response_get=local_user.show_local_user_by_name('test') 
                       
        put_localuser = {
            "action": "edit",
            "username": "test",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 10,
            "prune_on_expiry": True
 
          }
         
        response = local_user.local_user(**put_localuser)
        logger.info(response) 
        response_get = local_user.show_local_user_by_name("test") 
        Assertion.assert_regular(json.dumps(response_get), '"account_lifetime": {"minutes": 10}', 'err: Failed to edit localuser')
        Assertion.assert_regular(json.dumps(response_get), '"name": "Trusted Users"', 'err: Failed to edit localuser')  


class TC011_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47898"
    description = show_testcase_info(Parameter.TESTPLAN, '1546928', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546928')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_create_localuser_group(self):
        add_local_group = {
         "action": "add",
         "groupname": "local group",
         "grouptype": "locally_only"
          }
         
        response = local_user.local_group(**add_local_group )
        logger.info(response) 
        response_get = local_user.show_local_group_by_name('local group') 
        Assertion.assert_regular(json.dumps(response_get), '"name": "local group"', 'err: Failed to create local group') 
                
class TC012_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47899"
    description = show_testcase_info(Parameter.TESTPLAN, '1546929', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546929')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_get_localuser_group(self):
        
          
        response_get = local_user.show_local_groups() 
        logger.info(response_get)
        Assertion.assert_regular(json.dumps(response_get), '"name": .*', 'err: Failed to create user local group') 
                       
class TC013_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47900"
    description = show_testcase_info(Parameter.TESTPLAN, '1546930', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546930')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_localuser_group(self):
        edit_local_group = {
         "action": "edit",
         "groupname": "local group",
         "grouptype": "locally_only",
         "one_time_password": "otp"
          }
         
        response = local_user.local_group(**edit_local_group )
        logger.info(response) 
        response_get = local_user.show_local_groups() 
        Assertion.assert_regular(json.dumps(response_get), '"otp": true', 'err: Failed to create user local group') 
        
class TC017_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47904"
    description = show_testcase_info(Parameter.TESTPLAN, '1546934', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546934')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_get_localuser_group_byName(self):
        
          
        response_get = local_user.show_local_group_by_name('local group') 
        logger.info(response_get)
        Assertion.assert_regular(json.dumps(response_get), '"name": "local group"', 'err: Failed to get user local group by name') 
        
class TC018_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47905"
    description = show_testcase_info(Parameter.TESTPLAN, '1546935', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546935')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_put_localuser_group_perName(self):
    
        response_get = local_user.show_local_group_by_name('local group') 
        
        edit_local_group_perName = {
         "action": "edit",
         "groupname": "local group",
         "grouptype": "locally_only",
         "one_time_password": "totp",
          }
         
        response = local_user.local_group(**edit_local_group_perName)
        logger.info(response) 
        response_get = local_user.show_local_group_by_name('local group') 
        Assertion.assert_regular(json.dumps(response_get), '"totp": true', 'err: Failed to edit user local group by name') 
        
        
class TC019_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47906"
    description = show_testcase_info(Parameter.TESTPLAN, '1546936', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546936')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_get_localuser_settings(self):
        response_get = local_user.show_local_settings() 
        logger.info(response_get)
        Assertion.assert_regular(json.dumps(response_get), '"apply_password_constraints": true, "prune_on_expiry": true', 'err: Failed to get user local settings') 

class TC020_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47907"
    description = show_testcase_info(Parameter.TESTPLAN, '1546937', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546937')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_put_localuser_settings(self):
        edit_localuser_settings = {
         "apply_password_constraints": False,
         "prune_on_expiry": False
         }
        response = local_user.local_settings(**edit_localuser_settings)
        logger.info(response) 
        response_get = local_user.show_local_settings()                                                                
        Assertion.assert_regular(json.dumps(response_get), '"apply_password_constraints": false, "prune_on_expiry": false','err: Failed to edit user local settings') 
 
class TC022_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47909"
    description = show_testcase_info(Parameter.TESTPLAN, '1546939', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546939')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_add_user(self):
        add_user = {
            "action": "add",
            "username": "duplicate user",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
 
          }
         
        response = local_user.local_user(**add_user)
        logger.info(response) 
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "duplicate user"', 'err: Failed to create localuser') 
                         
    def test_add_duplicate_user(self):
        add_user = {
            "action": "add",
            "username": "duplicate user",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
 
          }
         
        response = local_user.local_user(**add_user)
        logger.info(response) 
        response_get = local_user.show_local_users() 
        Assertion.assert_not_regular(json.dumps(response_get), 'Already exists', 'err: Failed to attempt post') 

    def test_delete_duplicate_User(self):

        response = local_user.delete_local_user_no_domain('duplicate user')
        response_get = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "duplicate user"', 'err: user not deleted')
                
class TC024_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47911"
    description = show_testcase_info(Parameter.TESTPLAN, '1546941', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546941')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_put_non_existent_name(self):
        put_nonexistent_user = {
            "action": "edit",
            "username": "nonexistent",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users"],

          }
         
        response = local_user.local_user(**put_nonexistent_user)
        logger.info(response) 
        response_get = local_user.show_local_user_by_name('nonexistent') 
        Assertion.assert_not_regular(json.dumps(response_get), '"user nonexistent is not found"', 'err: Failed to edit user') 

class TC026_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47913"
    description = show_testcase_info(Parameter.TESTPLAN, '1546943', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546943')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_create_localuser_group(self):
        add_local_group = {
         "action": "add",
         "groupname": "duplicate user group",
         "grouptype": "locally_only"
          }
         
        response = local_user.local_group(**add_local_group )
        logger.info(response) 
        response_get = local_user.show_local_group_by_name('duplicate user group') 
        Assertion.assert_regular(json.dumps(response_get), '"name": "duplicate user group"', 'err: Failed to create local group') 

    def test_attempt_post_duplicate_group(self):
        duplicate_group = {
         "action": "add",
         "groupname": "duplicate user group",
         "grouptype": "locally_only"
          }
         
        response = local_user.local_group(**duplicate_group )
        logger.info(response) 
        response_get = local_user.show_local_group_by_name('duplicate user group') 
        Assertion.assert_not_regular(json.dumps(response_get), 'Already exists', 'err: Failed to attempt post')
                                                               
    def test_delete_duplicate_group(self):
        response = local_user.delete_local_group_no_domain('duplicate user group')
        resp1 = local_user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "duplicate user group"', 'err: group not deleted')                                                      
                         
class TC030_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47917"
    description = show_testcase_info(Parameter.TESTPLAN, '1546947', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546947')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_create_user(self):
       create_localuser = {
        "action": "add",
        "username": "user_object",
        "userpassword": "S0nic@uto",
        "member_of": ["Trusted Users","SonicWALL Administrators"]
          }
         
       response = local_user.local_user(**create_localuser)
       logger.info(response) 
       response_get = local_user.show_local_users() 
       Assertion.assert_regular(json.dumps(response_get), '"name": "user_object"', 'err: Failed to create localuser') 
                
    def test_remove_membership(self):
        member_json = {
            "groupname": "SonicWALL Administrators",
            "domain": "any",
            "members": ["user_object"]
        }
        response = local_user.delete_members_from_group(**member_json)
        response_get = local_user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "user_object"', 'err: group1 not removed')
 

class TC031_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47918"
    description = show_testcase_info(Parameter.TESTPLAN, '1546948', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546948')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_add_vpnaccess(self):
       add_user = {
            "action": "add",
            "username": "user_object1",
            "userpassword": "S0nic@uto",
            "vpn_client_access": ["All X1 Management IP", "LAN Subnets"]
        }
       response = local_user.add_user_vpn_client_access(**add_user)
       response_get = local_user.show_local_users()
       Assertion.assert_regular(json.dumps(response_get), '"name": "user_object1"', 'err:failed to create user')
                 
    def test_remove_vpnaccess(self):
       remove_vpnaccess = {
            "action": "delete",
            "username": "user_object1",
            "vpn_client_access": ["LAN Subnets"]
        }
       response = local_user.user_vpn_client_access(**remove_vpnaccess)
       response_get = local_user.show_local_user_by_name('user_object1')
       Assertion.assert_not_regular(json.dumps(response_get), '"group": "LAN Subnets"', 'err:failed to remove LAN subnets')
       
class TC032_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47919"
    description = show_testcase_info(Parameter.TESTPLAN, '1546949', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546949')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_create_group(self):
        add_group = {
         "action": "add",
         "groupname": "group1",
         "grouptype": "locally_only",
         "member_of": ["SonicWALL Administrators","SonicWALL Read-Only Admins"]  
          }
         
        response = local_user.group_member_of(**add_group)
        logger.info(response) 
        response_get = local_user.show_local_group_by_name('group1') 
        Assertion.assert_regular(json.dumps(response_get), '"name": "group1"', 'err: Failed to create local group') 
                
    def test_delete_membership(self):
        delete_group_membership = {
         "action": "delete",
         "groupname": "group1",
         "grouptype": "locally_only",
         "member_of": ["SonicWALL Administrators"]         
          }
         
        response = local_user.group_member_of(**delete_group_membership )
        logger.info(response) 
        response_get = local_user.show_local_group_by_name('group1') 
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "SonicWALL Administrators" ', 'err: Failed to delete membership') 
                           
class TC029_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47916"
    description = show_testcase_info(Parameter.TESTPLAN, '1546946', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546946')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_create_duplicate_group(self):
        create_group = {
         "action": "add",
         "groupname": "duplicate group",
         "grouptype": "locally_only"
          }
         
        response = local_user.local_group(**create_group )
        logger.info(response) 
        response_get = local_user.show_local_group_by_name('duplicate group') 
        Assertion.assert_regular(json.dumps(response_get), '"name": "duplicate group"', 'err: Failed to create local group') 
                
    def test_duplicate_group(self):
        add_duplicate_group = {
         "action": "add",
         "groupname": "duplicate group",
         "grouptype": "locally_only", 
          }
         
        response = local_user.local_group(**add_duplicate_group)
        logger.info(response) 
        response_get = local_user.show_local_group_by_name('duplicate group') 
        Assertion.assert_not_regular(json.dumps(response_get), 'Already exists.', 'err: Failed to duplicate local group') 
                        
class TC015_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47902"
    description = show_testcase_info(Parameter.TESTPLAN, '1546932', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546932')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    #create a user
    def test_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "testuuid",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
 
          }
         
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "testuuid"', 'err: Failed to create localuser') 
                    

    def test_get_local_account_perUUID(self):
        resp = local_user.get_local_user_uuid('testuuid')
        
        response_get = local_user.show_local_user_by_uuid(resp) 
        logger.info(response_get)
        Assertion.assert_regular(json.dumps(response_get), '"name": "testuuid"', 'err: Failed to get user per uuid') 

class TC016_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47903"
    description = show_testcase_info(Parameter.TESTPLAN, '1546933', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546933')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_edit_localuseraccount_per_UUID(self):
    
        resp = local_user.get_local_user_uuid('testuuid')
        
        uuid_json = {
            "uuid": resp,
            "username": "testuuid",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "hours",
            "accountlifetime": 1,
            "prune_on_expiry": True
            }              
        response = local_user.edit_local_user_by_uuid(**uuid_json)
        logger.info(response) 
        response_get = local_user.show_local_user_by_uuid(resp) 
        Assertion.assert_regular(json.dumps(response_get), '"account_lifetime": {"hours": 1}', 'err: Failed to edit localuser per uuid') 

class TC034_LocalUsers(Test):

    uuid = "SOSAIOT-TC-47921"
    description = show_testcase_info(Parameter.TESTPLAN, '1546951', description=True)['title']

    def test_00_show_testcase_info(self):
    
        show_testcase_info(Parameter.TESTPLAN, '1546951')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_get_local_group_perUUID(self):
        resp = local_user.get_local_group_uuid('Trusted Users')
        
        response_get = local_user.show_local_group_by_uuid(resp) 
        logger.info(response_get)
        Assertion.assert_regular(json.dumps(response_get), '"name": "Trusted Users"', 'err: Failed to get user per uuid') 
        
class TC033_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47920"
    description = show_testcase_info(Parameter.TESTPLAN, '1546950', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546950')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_add_vpnaccess_to_group(self):
        add_vpn_access = {
          "action": "add",
          "groupname": 'group2',
          "vpn_client_access": [{'group': 'LAN Subnets'}, {'group': 'WAN Subnets'}],
        }
        response = local_user.group_vpn_client_access(**add_vpn_access)
        logger.info(response) 
        response_get = local_user.show_local_group_by_name('group2') 
        Assertion.assert_regular(json.dumps(response_get), '{"group": "WAN Subnets"}, {"group": "LAN Subnets"}', 'err: Failed to create local group')
                
    def test_remove_vpnaccess_from_group(self):
        remove_vpnaccess = {
            "action": "delete",
            "groupname": "group2",
            "vpn_client_access": [{'group': 'LAN Subnets'}]
        }
        response = local_user.group_vpn_client_access(**remove_vpnaccess)
        response_get = local_user.show_local_group_by_name('group2')
        Assertion.assert_not_regular(json.dumps(response_get), '"group": "LAN Subnets"', 'err:failed to remove LAN subnets')

class TC02_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47890"
    description = show_testcase_info(Parameter.TESTPLAN, '1546920', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546920')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_get_local_users(self):
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "testuuid"', 'err: Failed to create localuser') 
                

class TC05_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47893"
    description = show_testcase_info(Parameter.TESTPLAN, '1546923', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546923')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test_user1",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
        }
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test_user1"', 'err: Failed to create localuser') 

    def test_edit_user_by_name(self):
        edit_user = {
            "username": "test_name",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "hours",
            "accountlifetime": 2,
            "prune_on_expiry": True
        }
        response = local_user.edit_local_user_by_name('test_user1',**edit_user)
        logger.info(response) 
        response_get = local_user.show_local_user_by_name("test_name") 
        Assertion.assert_regular(json.dumps(response_get), '"account_lifetime": {"hours": 2}', 'err: Failed to edit localuser per name') 
        Assertion.assert_regular(json.dumps(response_get), '"name": "SonicWALL Administrators"', 'err: Failed to edit localuser per name') 


class TC06_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47894"  
    description = show_testcase_info(Parameter.TESTPLAN, '1546924', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546924')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed") 
    
    def test_01_add_localuser(self):
        add_localuser1 = {
            "action": "add",
            "username": "test_check1",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
        }
        add_localuser2 = {
            "action": "add",
            "username": "test_check2",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 20,
            "prune_on_expiry": True
        }
        response = local_user.local_user(**add_localuser1)
        response = local_user.local_user(**add_localuser2)
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test_check1"', 'err: Failed to create localuser') 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test_check2"', 'err: Failed to create localuser') 
   
    def test_02_edit_local_users(self):
        edit_user1 = {
            "username": "test_edit_check1",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "hours",
            "accountlifetime": 3,
            "prune_on_expiry": True
        }
        edit_user2 = {
            "username": "test_edit_check2",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "hours",
            "accountlifetime": 1,
            "prune_on_expiry": True
        }
        response = local_user.edit_local_user_by_name('test_check1',**edit_user1)
        response = local_user.edit_local_user_by_name('test_check2',**edit_user2)
        logger.info(response) 
        response_get = local_user.show_local_user_by_name("test_edit_check1") 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test_edit_check1"', 'err: Failed to edit localuser per name') 
        response_get = local_user.show_local_user_by_name("test_edit_check2") 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test_edit_check2"', 'err: Failed to edit localuser per name') 

class TC07_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47895" 
    description = show_testcase_info(Parameter.TESTPLAN, '1546925', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546925')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_delete_user(self):
        resp = local_user.delete_local_user_no_domain("test_edit_check2")
        response_get = local_user.show_local_user_by_name("test_edit_check2") 
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "test_edit_check2"', 'err: Failed to edit localuser per name') 
        
class TC08_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47896"
    description = show_testcase_info(Parameter.TESTPLAN, '1546926', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546926')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "user_test1",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users","SonicWALL Administrators"],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 10,
            "prune_on_expiry": True
        }
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "user_test1"', 'err: Failed to create localuser') 
 
        output = diagnostic.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            flag = True if re.search(r'user_test1', doc) else False
            Assertion.assert_equal(flag, True, "ERR: group1 config is incorrect")
            os.remove('/tmp/techSupport')

class TC13_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47901"   
    description = show_testcase_info(Parameter.TESTPLAN, '1546931', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546931')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
        }
        resp = local_user.local_group(**group_json)
        resp1 = local_user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

     
    def test_delete_user_by_name(self):
        resp = local_user.delete_local_group_no_domain("group1")
        response_get = local_user.show_local_user_by_name("group1") 
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "group1"', 'err: Failed to edit localuser per name') 

class TC20_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47908"
    description = show_testcase_info(Parameter.TESTPLAN, '1546938', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546938')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    
    def test_09_config_local(self):
        user_auth = {
            "auth_method": "local",
            "sso_agent": True,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                "ERR:LOCALs method is not selected successfully")
        Assertion.assert_regular(json.dumps(resp), '"sso_agent": True',
                                "ERR:LOCALs method is not selected successfully")
        

class TC22_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47910" 
    description = show_testcase_info(Parameter.TESTPLAN, '1546940', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546940')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_delete_user(self):
        resp = local_user.delete_local_user_no_domain("test_edit_check2")
        response_get = local_user.show_local_user_by_name("test_edit_check2") 
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "test_edit_check2"', 'err: Failed to edit localuser per name') 

class TC26_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47914" 
    description = show_testcase_info(Parameter.TESTPLAN, '1546944', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546944')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
class TC27_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47915"   
    description = show_testcase_info(Parameter.TESTPLAN, '1546945', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546945')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_delete_user_by_name(self):
        resp = local_user.delete_local_group_no_domain("SonicWALL Administrators")
        response_get = local_user.show_local_user_by_name("SonicWALL Administrators") 
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "SonicWALL Administrators"', 'err: Failed to edit localuser per name') 

class TC09_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47897"
    description = show_testcase_info(Parameter.TESTPLAN, '1546927', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546927')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_delete_user_uuid(self):
        uuid = local_user.get_local_user_uuid('user_test1')
        resp = local_user.delete_local_user_uuid("user_test1")
        response_get = local_user.show_local_user_by_name("user_test1") 
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "user2"', 'err: Failed to edit localuser per name') 

class TC24_LocalUsers(Test):
    uuid = "SOSAIOT-TC-47912"
    description = show_testcase_info(Parameter.TESTPLAN, '1546942', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1546942')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_delete_user_uuid(self):
        response_get = local_user.show_local_user_by_name("user_test1") 
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "user_test1"', 'err: Failed to edit localuser per name') 
